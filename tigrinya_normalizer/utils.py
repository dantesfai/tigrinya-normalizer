# utils.py
import re
import unicodedata
import json

def normalize_unicode(text):
    """
    Normalize Unicode characters (e.g., NFKC or NFKD).
    Useful for removing diacritical marks or canonicalizing text.
    """
    return unicodedata.normalize('NFKC', text)

def remove_diacritics(text):
    """
    Remove diacritical marks from the given Unicode text.
    """
    normalized = unicodedata.normalize('NFD', text)
    return ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')

def clean_text(text):
    """
    General-purpose text cleaning: removes non-word characters and multiple spaces.
    """
    text = re.sub(r"[^\w\s፧።?!]", " ", text, flags=re.UNICODE)
    text = re.sub(r"\s+", " ", text, flags=re.UNICODE)
    return text.strip()

def sentence_split(text):
    """
    Splits text into sentences using Tigrinya-specific punctuation.
    """
    return re.split(r'(?<=[።፧?!]) +', text.strip())

def is_tigrinya(text):
    """
    Checks if the input text contains Tigrinya characters.
    """
    return bool(re.search(r'[\u1200-\u137F]', text))

def save_text_to_file(text, file_path):
    """
    Save the given text to a file.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text if isinstance(text, str) else "\n".join(text))

def load_json(filepath, default=None):
    """
    Load a JSON file and return its contents. 
    Returns `default` if the file is missing or malformed.
    """
    default = default if default is not None else {}
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Could not load {filepath}. Error: {e}")
        return default


def remove_extra_spaces(text):
    """
    Removes extra spaces: collapses multiple spaces and strips leading/trailing spaces.
    """
    return re.sub(r'\s+', ' ', text).strip()