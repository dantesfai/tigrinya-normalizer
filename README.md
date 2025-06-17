# Tigrinya Normalizer

A Python package and command-line tool for normalizing Tigrinya text.  
It applies linguistic rules, dictionary-based replacements, and cleaning steps to standardize Tigrinya text data.

---

## Features

- Normalize clitics and abbreviations  
- Handle hyphenated and slash-separated words  
- Remove unwanted punctuation and extra spaces  
- Customizable punctuation preservation  
- Load dictionaries for enhanced normalization  
- Command-line interface (CLI) for easy use  

---

## Installation

### Requirements

- Python 3.7+  
- See `requirements.txt` for dependencies

### Install from source

```bash
git clone https://github.com/yourusername/tigrinya-normalizer.git
cd tigrinya-normalizer
pip install .
```

### Or install dependencies manually:
```bash
pip install -r requirements.txt
```

## Usage
### As a Python package

```python
from tigrinya_normalizer.normalizer import TigrinyaNormalizer

normalizer = TigrinyaNormalizer(dataset_file="path/to/input.txt")

normalized_text = normalizer.normalize("ቛንቋ ትግርኛ")
print(normalized_text)
```
### As a CLI Tool

```bash
python cli.py -i path/to/input.txt -o normalized_output.txt
```

CLI Options:

| Argument               | Description                              | Default                 |
| ---------------------- | ---------------------------------------- | ----------------------- |
| `-i` / `--input`       | Path to input dataset file (required)    | -                       |
| `-o` / `--output`      | Output filename                          | `normalized_output.txt` |
| `-p` / `--punctuation` | Punctuation marks to preserve (optional) | None                    |


### Example: Preserve Punctuation

```bash
python cli.py -i input.txt -o output.txt -p "።፧?"
```

### Project Structure
```
tigrinya-normalizer/
├── tigrinya_normalizer/
│   ├── __init__.py
│   ├── normalizer.py          # Main normalization logic
│   ├── utils.py               # Utility functions
|   ├──dictionary_generator.py # Dictionary generator module
│   ├── dictionaries/          # Clitic/abbreviation mappings
│   └── data/
│       └── tigrinya_cleaned_sentences.txt
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_unit_normalizer.py
│   ├── test_integration_normalizer.py
│   └── test_utils.py
├── cli.py                     # Command-line interface
├── requirements.txt           # Project dependencies
├── setup.py                   # Packaging configuration
└── README.md                  # Project documentation

```

### Dictionaries

The normalizer uses dictionaries located in the dictionaries/ folder for:

- Clitic replacements

- Hyphenated words

- Abbreviations

- Other language-specific mappings

You can extend or customize these dictionaries to improve normalization accuracy.

## Tigrinya Dictionary Generator

This module is part of the `tigrinya_normalizer` package and is responsible for generating normalization dictionaries from raw Tigrinya text. These dictionaries are used to normalize clitics, hyphenated words, shortened forms, and other non-standard variations.

### Features

- Extracts and normalizes:
  - Clitic contractions (e.g., ተዳልዩ'ዩ → ተዳልዩ ኢዩ)
  - Forward-slash contractions (e.g., ቤ/ት → ቤት ትምህርቲ)
  - Dotted abbreviations (e.g., ኤ.ኤ.ም → ኤኤም)
  - Hyphenated forms (e.g., ስነጥበብ ስነ-ጥበብ → ስነ ጥበብ )
- Generates multiple dictionary files in JSON format
- Supports CLI usage for batch processing

---

###  Manual Corrections

After dictionary generation, the following files have undergone **manual correction** to improve accuracy:

- `clitic_dict.txt`
- `words_with_fwd_slash.txt`
- `words_with_dots.txt`
- `clitic_bind_dic.txt`
- `cliticize_improper_words.txt`

These changes include:

- Fixing incorrect automatic splits or mappings
- Removing irrelevant or noisy entries
- Expanding manually verified abbreviations

###  Important

Please **do not overwrite these files** without reviewing them. If you regenerate dictionaries using the CLI:

1. Backup the current dictionary files.
2. Use a file comparison tool (e.g., `diff`, `meld`, or VSCode's diff viewer) to inspect changes.
3. Apply previous manual corrections again as needed.

---

### Installation

```bash
pip install .
```


## Testing
You can run all tests using pytest from the root directory:

```bash
pytest tests/
```
Or Simply 

```bash
pytest
```
<code>pytest</code> will discover the tests in the tests/ folder automatically.

### Example conftest.py

If you want to share fixtures or setup/teardown logic between your test files, place them in tests/conftest.py. For example:

```python
import pytest
from tigrinya_normalizer.normalizer import TigrinyaNormalizer

@pytest.fixture
def sample_normalizer():
    return TigrinyaNormalizer(dataset_file="tests/sample_data.txt")

```
** Test File Naming Convention **

- test_unit_*.py — for unit tests of individual methods/classes

- test_integration_*.py — for integration tests involving multiple components

- test_utils.py — for utility functions

## Contributing

Contributions are welcome! Please open issues or pull requests for improvements or bug fixes.

## License
MIT License. See LICENSE for details.

## Contact

Daniel Tesfai d202361017@xs.ustb.edu.cn
Project Link: https://github.com/dantesfai/tigrinya-normalizer