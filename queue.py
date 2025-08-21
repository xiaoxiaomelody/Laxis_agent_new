# workflow/queue.py
# 预留 Celery/RQ 等队列实现的占位，便于后续把 approve->send 放到后台任务
def enqueue_send(outbox_id: int):
    # TODO: push to Celery/RQ
    pass
