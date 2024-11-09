import requests, os
from .models import HighlightExtractorDto
from .util import UploadFailedException, print_log
from dotenv import load_dotenv

load_dotenv()


class CRUD:
    def __init__(self, filename, dto: HighlightExtractorDto):
        self.filename = filename
        self.dto = dto
        self.upload_video_url = os.getenv("UPLOAD_VIDEO_URL")

    def save_to_s3(self):
        print_log("Saving to s3 started.")
        try:
            for i in range(5):
                # 파일을 multipart/form-data로 전송
                filepath = f"data/output/{self.filename}_{i}.mp4"
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
            print_log("Saved to s3 successfully.")
        except Exception as e:
            raise Exception(e)
