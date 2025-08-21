# workflow/approval.py
from models import Outbox

def approve(outbox_id: int, db):
    out = db.get(Outbox, outbox_id)
    if not out: return None
    out.status = "approved"; db.commit()
    # 这里先简化为“立即发送成功”，第二阶段再接入真正的发送 & 重试
    out.status = "sent"; db.commit()
    return out
