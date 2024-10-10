from fastapi import FastAPI, HTTPException
from models import SubtitleAdderDto
from utils import SubtitleAdder
import uvicorn

app = FastAPI()


@app.post("/extract-subtitle")
def extract_subtitle(dto: SubtitleAdderDto):
    url = dto.url
    adder = SubtitleAdder(url)
    try:
        adder.subtitleAdder()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app)
