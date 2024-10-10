from fastapi import FastAPI, HTTPException, BackgroundTasks, Response
from models import SubtitleAdderDto
from utils import SubtitleAdder
import uvicorn

app = FastAPI()


def process_subtitle(dto: SubtitleAdderDto):
    adder = SubtitleAdder(dto.url)
    try:
        adder.subtitleAdder()
        print("Processing finished")
        return {"message": "Processing finished"}
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
