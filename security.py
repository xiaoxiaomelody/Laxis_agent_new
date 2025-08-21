# utils/security.py
from cryptography.fernet import Fernet
import json, os

KEY_PATH = ".secret_key"

def _load_key():
    if not os.path.exists(KEY_PATH):
        with open(KEY_PATH, "wb") as f: f.write(Fernet.generate_key())
    return open(KEY_PATH, "rb").read()

def encrypt_token(token_json: dict) -> str:
    f = Fernet(_load_key())
    return f.encrypt(json.dumps(token_json).encode()).decode()

def decrypt_token(token_encrypted: str) -> dict:
    f = Fernet(_load_key())
    return json.loads(f.decrypt(token_encrypted.encode()).decode())
