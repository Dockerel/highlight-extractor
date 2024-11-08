# main.py
from fastapi import FastAPI, BackgroundTasks, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import SubtitleAdderDto
from .core.processSubtitle import SubtitleProcessor
from .core.status_manager import set_status, get_status
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

@app.post("/extract-subtitle")
async def extract_subtitle(
    dto: SubtitleAdderDto, background_tasks: BackgroundTasks, response: Response
):
    task_id = str(uuid.uuid4())
    set_status(task_id, "processing started")
    processor = SubtitleProcessor(dto, task_id)
    background_tasks.add_task(processor.process)
    response.status_code = 200
    return {"message": "Processing started", "task_id": task_id}

@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    status = get_status(task_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task_id, "status": status}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)