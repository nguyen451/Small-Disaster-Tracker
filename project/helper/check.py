import re
import unicodedata

def remove_accents(text : str):
    nfkd = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])

def normalize_text(text : str):
    text = re.sub(r"\s+", " ", text.strip())
    text = remove_accents(text)
    text = text.title()
    return text

print(normalize_text("Đăk   Nông"))
