# normalizer.py
import re
import os
from .utils import load_json, remove_extra_spaces

base_dir = os.path.dirname(os.path.abspath(__file__))

def resolve_path(path, default_relative_path):
    if path is None:
        path = default_relative_path
    if not os.path.isabs(path):
        path = os.path.join(base_dir, path)
    return path

class TigrinyaNormalizer:
    def __init__(self, files=None, dict_path=None, dataset_file=None, output_dir=None):
        
        self.dict_root_path = resolve_path(dict_path, 'dictionaries')
        self.dataset = resolve_path(dataset_file, 'data/cleaned_text.txt')
        self.output_dir = resolve_path(output_dir, 'data')

        self.dict_files = files or {
            'clitic_dict': 'clitic_dict.txt',
            'clitic_bind_dic': 'clitic_bind_dic.txt',
            'cliticize_improper_words': 'cliticize_improper_words.txt',
            'words_with_fwd_slash': 'words_with_fwd_slash.txt',
            'words_with_dots': 'words_with_dots.txt',
            'hyphenated_words_v1': 'hyphenated_words_v1.txt',
            'hyphenated_words_v2': 'hyphenated_words_v2.txt',
            'improper_abbreviations': 'improper_abbreviations.txt',
            'filtered_space_abbreviations': 'filtered_space_abbreviations.json',
            'filtered_single_abbreviations': 'filtered_single_abbreviations.json'
        }

        self.dictionaries = {}
        self.read_dictionaries()

        self.patterns = {
            "punctuation": re.compile(r"[^\w\s\u1367\u1362?!]", re.UNICODE),
            "multi_spaces": re.compile(r"\s+", re.UNICODE),
            "shortened_words": re.compile(r"(?<!\w)([\w\u1200-\u137F]{1,3}\.)+", re.UNICODE)
        }

    def read_dictionaries(self):
        for key, filename in self.dict_files.items():
            file_path = os.path.join(self.dict_root_path, filename)
            self.dictionaries[key] = load_json(file_path)

    def normalize(self, text, punctuation_to_keep=None):
        text = self.replace_clitic_dictionary(text)
        text = self.replace_shortened_words_with_dots(text)
        text = self.replace_hyphenated_v1(text)
        text = self.normalize_clitic_variation(text)
        text = self.replace_improper_abbreviation(text)

        words = text.split()
        normalized_words = [self._handle_word(word) for word in words]

        if punctuation_to_keep:
            pattern = re.compile(rf"[^\w\s{re.escape(punctuation_to_keep)}]", re.UNICODE)
        else:
            pattern = self.patterns["punctuation"]

        cleaned_text = pattern.sub(" ", " ".join(normalized_words)).strip()
        return remove_extra_spaces(cleaned_text)

    def _handle_word(self, word):
        if "-" in word:
            return self._handle_hyphen(word)
        if "/" in word:
            return self._handle_forward_slash(word)
        if any(c in word for c in ["'", "`", "’"]):
            return self._handle_clitic(word)
        return word

    def _handle_hyphen(self, word):
        return self.dictionaries.get("hyphenated_words_v2", {}).get(word, word)

    def _handle_forward_slash(self, word):
        return self.dictionaries.get("words_with_fwd_slash", {}).get(word, word)

    def _handle_clitic(self, word):
        token = re.split(r"[`’']", word)
        bind_token = "".join(token[:2])

        if bind_token in self.dictionaries.get("cliticize_improper_words", {}):
            return bind_token
        if len(token) > 1 and token[1] in self.dictionaries.get("clitic_dict", {}):
            token[1] = self.dictionaries["clitic_dict"][token[1]]

        return " ".join(token).strip()

    def replace_abbreviations(self, text):
        abbr_dict = self.dictionaries.get("improper_abbreviations", {})
        sorted_replacements = sorted(abbr_dict.items(), key=lambda x: len(x[0]), reverse=True)
        pattern = re.compile(r'(' + r'|'.join(re.escape(word) for word, _ in sorted_replacements) + r')')
        return pattern.sub(lambda m: abbr_dict[m.group()], text)

    def replace_shortened_words_with_dots(self, text):
        short_dict = self.dictionaries.get("words_with_dots", {})
        pattern = re.compile(r'(?<!\S)(?:[\w\u1200-\u137F]+(?:\.[\w\u1200-\u137F]+)*\.?)(?!\S)', re.UNICODE)
        return pattern.sub(lambda m: short_dict.get(m.group(0), m.group(0)), text)

    def replace_hyphenated_v1(self, text):
        words = re.split(r"(\W+)", text, flags=re.UNICODE)
        hyphen_dict = self.dictionaries.get("hyphenated_words_v1", {})
        return "".join([hyphen_dict.get(word, word) for word in words])

    def replace_clitic_dictionary(self, text):
        clitic_dict = self.dictionaries.get("clitic_dict", {})
        pattern = re.compile(r'(^|\s)([\w\u1200-\u137F]+)(?=\s|$)', re.UNICODE)
        return pattern.sub(lambda m: m.group(1) + clitic_dict.get(m.group(2), m.group(2)), text)

    def normalize_clitic_variation(self, text):
        replacements = {
            "ኢየ": "እየ", "እዩ": "ኢዩ", "እያ": "ኢያ", "እየን": "ኢየን",
            "እዮም": "ኢዮም", "ዓመት ምሕረት": "ዓመት ምህረት", "እውን": "ውን"
        }
        pattern = re.compile(r'(' + r'|'.join(map(re.escape, replacements.keys())) + r')')
        return pattern.sub(lambda m: replacements[m.group()], text)

    def replace_improper_abbreviation(self, text):
        space_dict = self.dictionaries.get("filtered_space_abbreviations", {})
        single_dict = self.dictionaries.get("filtered_single_abbreviations", {})

        space_pat = re.compile(r'\b(?:' + '|'.join(map(re.escape, space_dict.keys())) + r')\b')
        single_pat = re.compile(r'\b(?:' + '|'.join(map(re.escape, single_dict.keys())) + r')\b')

        text = space_pat.sub(lambda m: space_dict[m.group()], text)
        return single_pat.sub(lambda m: single_dict[m.group()], text)

    def normalize_and_save(self, output_file, punctuation_to_keep=None):
        if not self.dataset:
            raise FileNotFoundError("Dataset file not specified.")

        os.makedirs(self.output_dir, exist_ok=True)
        output_path = os.path.join(self.output_dir, output_file)

        with open(self.dataset, 'r', encoding='utf-8') as f:
            raw_text = f.read()

        normalized_text = self.normalize(raw_text, punctuation_to_keep)
        sentences = re.split(r'(?<=[።፧?!]) +', remove_extra_spaces(normalized_text.strip()))

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(sentences) + "\n")
