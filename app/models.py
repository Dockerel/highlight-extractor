from pydantic import BaseModel


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
