from gmail_client import build_gmail_service, list_messages, get_message_full
from db import SessionLocal
from models import EmailMessage, EmailThread
from nlp.intent import classify_intent
from nlp.ner import extract_entities
from utils import clean_text  # 你可以写一个简单的邮件清洗函数
import base64

def fetch_and_store_emails(oauth_token: dict, tenant_id: int):
    service = build_gmail_service(oauth_token)
    messages = list_messages(service)

    db = SessionLocal()

    for m in messages:
        full_msg = get_message_full(service, m["id"])
        payload = full_msg.get("payload", {})
        headers = {h["name"]: h["value"] for h in payload.get("headers", [])}
        subject = headers.get("Subject", "")
        from_addr = headers.get("From", "")
        to_addr = headers.get("To", "")
        body = ""

        # 获取正文（这里只是处理 plain text 的情况）
        if "parts" in payload:
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain":
                    body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
        elif "body" in payload and "data" in payload["body"]:
            body = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")

        parsed_text = clean_text(body)
        intent = classify_intent(subject + "\n" + parsed_text)
        entities = extract_entities(parsed_text)

        # Step 1: 如果 thread 没有就创建
        thread = EmailThread(
            tenant_id=tenant_id,
            provider_thread_id=full_msg["threadId"],
            last_intent=intent,
        )
        db.add(thread); db.commit()

        # Step 2: 存储这封邮件
        msg = EmailMessage(
            thread_id=thread.id,
            provider_msg_id=m["id"],
            from_addr=from_addr,
            to_addr=to_addr,
            subject=subject,
            raw_text=body,
            parsed_text=parsed_text,
            entities=entities
        )
        db.add(msg)

    db.commit()
    db.close()
