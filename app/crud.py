import requests, os
from models import SubtitleAdderDto
from util import UploadFailedException, print_log

upload_video_url = os.getenv("UPLOAD_VIDEO_URL")


def save_to_s3(filename, dto: SubtitleAdderDto):
    try:
        # 파일을 multipart/form-data로 전송
        filepath = f"data/output/{filename}"
        # with open(filepath, "rb") as video_file:
        #     files = {
        #         "file": (
        #             "video.mp4",
        #             video_file,
        #             "video/mp4",
        #         )  # 파일명, 파일 객체, MIME 타입
        #     }
        #     response = requests.post(
        #         upload_video_url,
        #         files=files,
        #         data={
        #             "title": dto.title,
        #             "memberId": dto.memberId,
        #             "categoryId": dto.categoryId,
        #         },
        #     )
        #     if response.status_code != 200:
        #         raise UploadFailedException(response.status_code)
        os.remove(filepath)
        print_log("Saved to s3 successfully.")
    except Exception as e:
        print_log(e, 1)
        raise Exception
