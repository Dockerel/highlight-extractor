import requests, os, boto3
from botocore.exceptions import NoCredentialsError
from .models import HighlightExtractorDto
from .core.status_manager import add_urls
from .util import UploadFailedException, print_log
from dotenv import load_dotenv

load_dotenv()


class CRUD:
    def __init__(self, filename):
        self.filename = filename
        self.task_id = filename
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_bucket_name = os.getenv("AWS_BUCKET_NAME")

    def save_to_s3(self):
        print_log("Saving to s3 started.")
        try:
            s3 = boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key
            )

            for i in range(5):
                video_filepath = f"data/output/{self.filename}_{i}.mp4"
                video_filename = video_filepath.split('/')[-1]
                s3.upload_file(video_filepath, self.aws_bucket_name, video_filename)

                file_url = f"https://{self.aws_bucket_name}.s3.ap-southeast-2.amazonaws.com/{video_filename}"
                add_urls(self.task_id, file_url)

                thumbnail_filepath = f"data/thumbnail/{self.filename}_{i}.jpg"
                thumbnail_filename = "thumbnails/"+thumbnail_filepath.split('/')[-1]
                s3.upload_file(thumbnail_filepath, self.aws_bucket_name, thumbnail_filename)

            print_log("Saved to s3 successfully.")
        except FileNotFoundError:
            raise Exception("The file was not found")
        except NoCredentialsError:
            raise Exception("Credentials not available")
        except Exception as e:
            raise Exception(e)

    # def save_to_s3(self):
    #     print_log("Saving to s3 started.")
    #     try:
    #         for i in range(5):
    #             # 파일을 multipart/form-data로 전송
    #             filepath = f"data/output/{self.filename}_{i}.mp4"
    #             with open(filepath, "rb") as video_file:
    #                 files = {
    #                     "file": (
    #                         f"{self.filename}_{i}.mp4",
    #                         video_file,
    #                         "video/mp4",
    #                     )  # 파일명, 파일 객체, MIME 타입
    #                 }
    #                 response = requests.post(
    #                     self.upload_video_url,
    #                     files=files
    #                 )
    #                 print(response.text)
    #                 if response.status_code != 200:
    #                     print("error")
    #                     raise UploadFailedException(response.status_code)
    #                 response_data = response.json()
    #                 url = response_data.get("url")
    #                 add_urls(self.task_id, url)
    #             break
    #         print_log("Saved to s3 successfully.")
    #     except Exception as e:
    #         raise Exception(e)
