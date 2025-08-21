# agents/orchestrator.py
from sqlalchemy.orm import Session
from models import EmailThread, EmailMessage, Outbox, Template
from nlp.preprocess import html_to_text, strip_quotes_and_signature
from nlp.ner import extract_entities
from nlp.intent import classify_intent
from agents.writer import render_template

class AgentOrchestrator:
    def __init__(self, db: Session, tenant, account, mail_client=None):
        self.db = db
        self.tenant = tenant        # Tenant 对象（含 profile）
        self.account = account      # OAuthAccount（知道发件邮箱/提供商）
        self.mail_client = mail_client

    def handle_incoming(self, provider_thread_id: str, provider_msg_id: str,
                        raw_html: str, from_addr: str, to_addr: str, subject: str):
        # 1) 预处理
        text = strip_quotes_and_signature(html_to_text(raw_html))
        ents = extract_entities(text)
        intent = classify_intent(text)

        # 2) 线程与消息入库
        thread = (self.db.query(EmailThread)
                  .filter_by(tenant_id=self.tenant.id, provider_thread_id=provider_thread_id)
                  .one_or_none())
        if not thread:
            thread = EmailThread(tenant_id=self.tenant.id, provider_thread_id=provider_thread_id, state={})
            self.db.add(thread); self.db.commit()

        msg = EmailMessage(thread_id=thread.id, provider_msg_id=provider_msg_id,
                           from_addr=from_addr, to_addr=to_addr, subject=subject,
                           raw_text=text, parsed_text=text, entities=ents)
        self.db.add(msg)
        thread.last_intent = intent
        self.db.commit()

        # 3) 选择模板
        tpl_row = self.db.query(Template).filter_by(key=intent).one_or_none()
        if not tpl_row:
            tpl_row = self.db.query(Template).filter_by(key="meeting_request").one()

        # 4) 渲染上下文
        ctx = {
            "subject": f"Re: {subject}",
            "candidate_name": ents["PERSON"][0] if ents["PERSON"] else "there",
            "meeting_time": ents["DATE"][0] if ents["DATE"] else "this week",
            # 从租户配置注入“动态签名”
            "customer_name": self.tenant.profile.get("name", "John"),
            "customer_title": self.tenant.profile.get("title", "HR Manager"),
            "customer_company": self.tenant.profile.get("company", "ACME Inc"),
        }
        rendered = render_template(tpl_row.jinja, ctx)

        # 5) 草稿入 Outbox（等待审批/发送）
        out = Outbox(
            tenant_id=self.tenant.id, provider=self.account.provider,
            from_email=self.account.email, to_email=from_addr,
            subject=rendered["subject"], body_text=rendered["body_text"],
            body_html=rendered["body_html"], status="pending",
            meta={"thread_id": thread.id, "intent": intent, "entities": ents},
        )
        self.db.add(out); self.db.commit()
        return out
