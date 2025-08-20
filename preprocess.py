from bs4 import BeautifulSoup
import re

def html_to_text(html: str) -> str:
    return BeautifulSoup(html or "", "html.parser").get_text("\n")

def strip_quotes_and_signature(text: str) -> str:
    if not text: return ""
    text = re.split(r"\nOn .*wrote:\n", text)[0]
    text = re.split(r"\n--+\n", text)[0]        
    return text.strip()
