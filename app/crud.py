import requests, os
from models import GetPresignedUrlToUpload, SubtitleAdderDto


get_presigned_url = os.getenv("GET_PRESIGNED_URL")


def save_to_s3(filename):
    response = requests.get(get_presigned_url)
    data = GetPresignedUrlToUpload.model_validate(response.json())
    presigned_url = data.url

    # 파일을 열고 presigned URL로 PUT 요청을 통해 업로드
    with open("data/video/" + filename, "rb") as file:
        upload_response = requests.put(presigned_url, data=file)

        # 업로드 결과 확인
        if upload_response.status_code == 200:
            # 성공 콜백
            data = SubtitleAdderDto.model_validate(upload_response.json())
            return data.url
        else:
            # 실패 콜백
            raise Exception(
                f"File upload failed with status code: {upload_response.status_code}"
            )
