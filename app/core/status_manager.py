from ..models import HighlightExtractorDto

processing_status = {}

def init_status(task_id: str, dto: HighlightExtractorDto):
    processing_status[task_id] = {"status":"", "urls":[], "dto":dto}

def set_status(task_id: str, status: str):
    processing_status[task_id]["status"] = status

def get_status(task_id: str):
    if task_id in processing_status:
        return processing_status[task_id].get("status")
    return None

def delete_status(task_id: str):
    if task_id in processing_status:
        del processing_status[task_id]

def get_urls(task_id: str):
    if task_id in processing_status:
        return processing_status[task_id].get("urls")
    return None

def add_urls(task_id: str, url: str):
    processing_status[task_id]["urls"].append(url)

def get_dto(task_id: str):
    if task_id in processing_status:
        return processing_status[task_id].get("dto")
    return None

def clear_status():
    processing_status.clear()