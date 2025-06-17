import os
import json
import tempfile
import pytest
from tigrinya_normalizer.utils import load_json, remove_extra_spaces

# --- Fixtures ---

@pytest.fixture
def json_file():
    data = {"key1": "value1", "key2": "value2"}
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w', encoding='utf-8') as f:
        json.dump(data, f)
        return f.name, data

@pytest.fixture
def txt_file():
    content = "key1 value1\nkey2 value2\n"
    expected = {"key1": "value1", "key2": "value2"}
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding='utf-8') as f:
        f.write(content)
        return f.name, expected

@pytest.fixture
def malformed_txt_file():
    content = "key1\nkey2 value2\n"
    expected = {"key2": "value2"}
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding='utf-8') as f:
        f.write(content)
        return f.name, expected

# --- Tests ---

def test_remove_extra_spaces():
    input_text = "This   is\t a test\nstring.  "
    expected = "This is a test string."
    assert remove_extra_spaces(input_text) == expected

def test_remove_extra_spaces_empty():
    assert remove_extra_spaces("   \n\t ") == ""

def test_remove_extra_spaces_no_change():
    assert remove_extra_spaces("Clean string.") == "Clean string."
