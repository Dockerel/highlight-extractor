# main.py
from fastapi import FastAPI, BackgroundTasks, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import HighlightExtractorDto, ExtractHighlightsAsyncResponse, TaskStatusResponse, SelectHighlightResponse, ClearProcessStatusResponse, HighlightSelectionRequest
from .crud import CRUD
from .util import video_making_request_sending
from .core.processHighlight import HighlightProcessor
from .core.status_manager import init_status, set_status, get_status, delete_status, get_urls, get_dto, clear_status
import uvicorn
import uuid

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract-highlights", response_model = ExtractHighlightsAsyncResponse)
async def extract_highlights(
    dto: HighlightExtractorDto, background_tasks: BackgroundTasks, response: Response
):
    task_id = str(uuid.uuid4())
    init_status(task_id, dto)
    set_status(task_id, "processing started")
    processor = HighlightProcessor(dto, task_id)
    background_tasks.add_task(processor.process)
    response.status_code = 200
    return {"message": "Processing started", "task_id": task_id}

@app.get("/task-status/{task_id}", response_model = TaskStatusResponse)
async def get_task_status(task_id: str):
    status = get_status(task_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Task not found")
    # if status == "failed":
    #     delete_status(task_id)
    return {"task_id": task_id, "status": status}

@app.get("/select-highlight/{task_id}", response_model = SelectHighlightResponse)
async def select_highlight(task_id: str):
    urls = get_urls(task_id)
    dto = get_dto(task_id)
    if urls is None or dto is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"urls": urls, "dto": dto}

@app.post("/select-highlight")
async def delete_unselected_files(req: HighlightSelectionRequest):
    try:
        task_id = req.task_id
        executor = CRUD(task_id, req.index)
        executor.delete_from_s3()
        # video object making request
        dto = get_dto(task_id)
        video_id = video_making_request_sending(task_id, dto)
        # delete_status(task_id)
        return {"video_id": video_id}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Task not found")

@app.get("/clear-status", response_model = ClearProcessStatusResponse)
async def clear_process_status():
    clear_status()
    return {"message": "Processes successfully cleared"}


if __name__ == "__main__":
    uvicorn.run(app)