from fastapi import FastAPI, HTTPException, BackgroundTasks, Response
from models import SubtitleAdderDto
from utils import SubtitleAdder
import uvicorn

app = FastAPI()


def process_subtitle(dto: SubtitleAdderDto):
    adder = SubtitleAdder(dto.url)
    try:
        filename = adder.subtitleAdder()
        video_url = adder.save_to_s3(filename + ".mp4")
        adder.callback_request(dto.email, video_url, filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/extract-subtitle")
async def extract_subtitle(
    dto: SubtitleAdderDto, background_tasks: BackgroundTasks, response: Response
):
    background_tasks.add_task(process_subtitle, dto)
    response.status_code = 200
    return {"message": "Processing started"}


if __name__ == "__main__":
    uvicorn.run(app)
