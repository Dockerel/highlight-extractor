from pydantic import BaseModel


class SubtitleAdderDto(BaseModel):
    url: str
    email: str


class GetPresignedUrlToUpload(BaseModel):
    url: str


class SubtitleAdderCallbackResponse(BaseModel):
    email: str
    url: str
    filename: str
