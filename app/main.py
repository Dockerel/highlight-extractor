from fastapi import FastAPI, BackgroundTasks, Response
from fastapi.middleware.cors import CORSMiddleware
from models import SubtitleAdderDto
from core.processSubtitle import process_subtitle
import uvicorn

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
    background_tasks.add_task(process_subtitle, dto)
    response.status_code = 200
    return {"message": "Processing started"}


if __name__ == "__main__":
    uvicorn.run(app)
