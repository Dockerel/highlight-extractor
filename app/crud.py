import requests, os
from models import SubtitleAdderDto, VideoUploadRequest
from util import UploadFailedException

upload_video_url = os.getenv("UPLOAD_VIDEO_URL")


def save_to_s3(filename, dto: SubtitleAdderDto):
    # 파일을 multipart/form-data로 전송
    filepath = f"data/output/{filename}"
    with open(filepath, "rb") as video_file:
        files = {
            "file": (
                "video.mp4",
                video_file,
                "video/mp4",
            )  # 파일명, 파일 객체, MIME 타입
        }
        response = requests.post(
            upload_video_url,
            files=files,
            data=VideoUploadRequest(dto.title, dto.memberId, dto.categoryId),
        )
        if response.status_code != 200:
            raise UploadFailedException(response.status_code)
