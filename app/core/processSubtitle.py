from models import SubtitleAdderDto
from core.subtitleAdder import SubtitleAdder
from crud import save_to_s3
from fastapi import HTTPException
from util import smtp_callback
import os


def process_subtitle(dto: SubtitleAdderDto):
    adder = SubtitleAdder(dto.url)
    try:
        output_filename = adder.subtitleAdder()
        save_to_s3(output_filename, dto)
        os.remove("data/output/" + output_filename)
        smtp_callback(dto.email)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
