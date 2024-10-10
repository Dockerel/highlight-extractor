from pydantic import BaseModel


class SubtitleAdderDto(BaseModel):
    url: str
