# Highlight Extractor

**Highlight-Extractor** is a service that extracts highlights by subtitle(scripts), resizing video for short-form(16:9) also adds subtitles to videos using **OpenAI** and **OpenAI's Whisper model** for subtitle extraction and **FFmpeg** for embedding subtitles into the video. The service is implemented with **FastAPI** to provide a API interface.

## Requirements

* Python 3.8 or greater

### GPU

Execution requires the following NVIDIA libraries to be installed:

* [cuBLAS for CUDA 12](https://developer.nvidia.com/cublas)
* [cuDNN for CUDA 12](https://developer.nvidia.com/cudnn)

## Installation
1. Clone the repository.
```bash
git clone https://github.com/Dockerel/highlight-extractor.git
cd highlight-extractor
```
2. Make virtual environment.
```bash
python -m venv .venv
source .venv/bin/activate
```
3. Set .env file.
```bash
SMTP_ID={YOUR_GOOGLE_SMTP_ID}
SMTP_PW={YOUR_GOOGLE_SMTP_PW}

OPENAI_API_KEY={YOUR_OPENAI_API_KEY}

AWS_ACCESS_KEY_ID={YOUR_AWS_ACCESS_KEY_ID}
AWS_SECRET_ACCESS_KEY={YOUR_AWS_SECRET_ACCESS_KEY}
AWS_BUCKET_NAME={YOUR_AWS_BUCKET_NAME}
```
4. Execute with command below

at local
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```
to deploy
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Paths
| Path   | Description                              |
| -------- | ---------------------------------------- |
| `POST` /extract-highlights    | Used to allocate a task for highlight extracting. |
| `GET` /task-status/{task_id}   | Used when checking status of tasks by task id. |
| `GET` /select-highlight/{task_id}  | Used to select favorite extracted highlight. |
| `GET` /clear-status    | Used to clear in-memory total process status. |

