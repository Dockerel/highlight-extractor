from models import SubtitleAdderDto
from core.subtitleAdder import SubtitleAdder
from crud import save_to_s3
from fastapi import HTTPException


def process_subtitle(dto: SubtitleAdderDto):
    adder = SubtitleAdder(dto.url)
    try:
        output_filename = adder.subtitleAdder()
        video_url = save_to_s3(output_filename)
        adder.callback_request(dto.email, video_url, output_filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
