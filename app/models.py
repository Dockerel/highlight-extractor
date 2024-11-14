from pydantic import BaseModel
from typing import List

class HighlightExtractorDto(BaseModel):
    url: str
    email: str
    title: str
    memberId: int
    categoryId: int


class GetPresignedUrlToUploadResponse(BaseModel):
    url: str


class GetPresignedUrlToUploadRequest(BaseModel):
    filename: str


class VideoUploadRequest(BaseModel):
    title: str
    memberId: int
    categoryId: int

class ExtractHighlightsAsyncResponse(BaseModel):
    message: str
    task_id: str

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str

class SelectHighlightResponse(BaseModel):
    urls: List[str]
    dto: HighlightExtractorDto

class ClearProcessStatusResponse(BaseModel):
    message: str