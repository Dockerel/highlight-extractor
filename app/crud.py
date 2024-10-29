import requests, os
from .models import SubtitleAdderDto
from .util import UploadFailedException, print_log
from dotenv import load_dotenv

load_dotenv()


class CRUD:
    def __init__(self, filename, dto: SubtitleAdderDto):
        self.filename = filename
        self.dto = dto
        self.upload_video_url = os.getenv("UPLOAD_VIDEO_URL")

    def save_to_s3(self):
        try:
            # 파일을 multipart/form-data로 전송
            filepath = f"data/output/output-resize_{self.filename}.mp4"
            with open(filepath, "rb") as video_file:
                files = {
                    "file": (
                        "video.mp4",
                        video_file,
                        "video/mp4",
                    )  # 파일명, 파일 객체, MIME 타입
                }
                response = requests.post(
                    self.upload_video_url,
                    files=files,
                    data={
                        "title": self.dto.title,
                        "memberId": self.dto.memberId,
                        "categoryId": self.dto.categoryId,
                    },
                )
                if response.status_code != 200:
                    raise UploadFailedException(response.status_code)
            os.remove(filepath)
            print_log("Saved to s3 successfully.")
        except Exception as e:
            print_log(e, 1)
            raise Exception
