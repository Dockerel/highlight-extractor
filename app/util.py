import requests, boto3, time
from datetime import datetime
from pytz import timezone
from .models import HighlightExtractorDto


class UploadFailedException(Exception):
    def __init__(self, status_code, message="Failed to upload video to s3"):
        self.status_code = status_code
        self.message = f"{message}. Status code: {status_code}"
        super().__init__(self.message)


def download_video(filename, url):
    try:
        r = requests.get(url)
        with open(f"data/video/{filename}.mp4", "wb") as outfile:
            outfile.write(r.content)
        print_log("Video downloaded successfully.")
    except Exception as e:
        print_log(e, 1)
        raise Exception


def print_log(content, mode=0):
    seoul_time = datetime.now(timezone('Asia/Seoul'))
    
    if mode == 1:
        print("\033[91mError\033[0m: ", end="")
    else:
        print("\033[92mINFO\033[0m: ", end="")
    
    print(f'{seoul_time.strftime("%Y.%m.%d %I:%M:%S")} | {content}')

def video_making_request_sending(filename, dto:HighlightExtractorDto):
    retry = 5
    url = "http://ec2-43-202-1-31.ap-northeast-2.compute.amazonaws.com:8080/api/videos/create"

    data = {
        "title": dto.title,
        "member_id": dto.memberId,
        "category_id": dto.categoryId,
        "file_name": filename
    }
    
    error_msg=""
    while retries>0:
        try:
            response = requests.post(url, json=data)
            response_data = response.json()
            video_id = response_data["video_id"]
            return video_id
        except Exception as e:
            error_msg=e
            retries -= 1
            time.sleep(1)
    if retries==0:
        raise Exception(error_msg)