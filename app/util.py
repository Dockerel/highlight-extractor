import requests
from datetime import datetime
from pytz import timezone


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
