from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import Base, engine, Outbox
from workflow.approval import approve

app = FastAPI(title="Laxis AI SDR Agent")
Base.metadata.create_all(bind=engine)

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/outbox")
def list_outbox(db: Session = Depends(get_db)):
    return db.query(Outbox).order_by(Outbox.created_at.desc()).all()

@app.post("/approve/{outbox_id}")
def approve_one(outbox_id: int, db: Session = Depends(get_db)):
    out = approve(outbox_id, db)
    return {"status": out.status if out else "not_found", "id": outbox_id}
