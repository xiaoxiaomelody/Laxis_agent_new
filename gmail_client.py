from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from base64 import urlsafe_b64encode
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def build_gmail_service(token_json: dict):
    creds = Credentials(
        token=token_json["access_token"],
        refresh_token=token_json.get("refresh_token"),
        token_uri=token_json["token_uri"],
        client_id=token_json["client_id"],
        client_secret=token_json["client_secret"],
        scopes=token_json["scopes"],
    )
    return build("gmail", "v1", credentials=creds)

def list_messages(service, q="in:inbox -category:promotions", max_results=20):
    return service.users().messages().list(userId="me", q=q, maxResults=max_results).execute().get("messages", [])

def get_message_full(service, msg_id):
    return service.users().messages().get(userId="me", id=msg_id, format="full").execute()

def _make_raw(subject, to_addr, body_text=None, body_html=None, from_addr=None):
    msg = MIMEMultipart("alternative")
    if subject: msg["Subject"] = subject
    if from_addr: msg["From"] = from_addr
    if to_addr: msg["To"] = to_addr
    if body_text: msg.attach(MIMEText(body_text, "plain", "utf-8"))
    if body_html: msg.attach(MIMEText(body_html, "html", "utf-8"))
    return {"raw": urlsafe_b64encode(msg.as_bytes()).decode("utf-8")}

def create_draft(service, subject, to_addr, body_text=None, body_html=None, from_addr=None):
    raw = _make_raw(subject, to_addr, body_text, body_html, from_addr)
    return service.users().drafts().create(userId="me", body={"message": raw}).execute()

def send_message(service, subject, to_addr, body_text=None, body_html=None, from_addr=None):
    raw = _make_raw(subject, to_addr, body_text, body_html, from_addr)
    return service.users().messages().send(userId="me", body=raw).execute()
