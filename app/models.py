from pydantic import BaseModel


class SubtitleAdderDto(BaseModel):
    url: str
    email: str


class GetPresignedUrlToUpload(BaseModel):
    url: str
