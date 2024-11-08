processing_status = {}

def set_status(task_id: str, status: str):
    processing_status[task_id] = status

def get_status(task_id: str):
    return processing_status.get(task_id)

def delete_status(task_id: str):
    if task_id in processing_status:
        del processing_status[task_id]