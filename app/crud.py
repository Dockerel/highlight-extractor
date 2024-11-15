import requests, os, boto3
from botocore.exceptions import NoCredentialsError
from .models import HighlightExtractorDto
from .core.status_manager import add_urls
from .util import UploadFailedException, print_log
from dotenv import load_dotenv

load_dotenv()


class CRUD:
    def __init__(self, filename, index=0):
        self.filename = filename
        self.task_id = filename
        self.index = index
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
    
    def delete_from_s3(self):
        print_log("Deleting from s3 started.")
        try:
            s3 = boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key
            )

            for i in range(5):
                if i==self.index:
                    continue
                video_filename = f"{self.filename}_{i}.mp4"
                s3.delete_object(Bucket=self.aws_bucket_name, Key=video_filename)
                
                thumbnail_filename = f"thumbnails/{self.filename}_{i}.jpg"
                s3.delete_object(Bucket=self.aws_bucket_name, Key=thumbnail_filename)

        except NoCredentialsError:
            raise Exception("Credentials not available")
        except Exception as e:
            raise Exception(e)