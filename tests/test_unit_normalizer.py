import pytest
import os
import pathlib
from tigrinya_normalizer.normalizer import TigrinyaNormalizer
from tigrinya_normalizer.utils import remove_extra_spaces

@pytest.fixture(scope="module")
def normalizer():
    base_dir = pathlib.Path(__file__).parent.parent.resolve()  # project root
    dict_path = base_dir / "tigrinya_normalizer" / "dictionaries"
    dataset_file = base_dir / "tests" / "data" / "sample_input.txt"
    output_dir = base_dir / "tests" / "output"
    
    return TigrinyaNormalizer(dict_path=str(dict_path), dataset_file=str(dataset_file), output_dir=str(output_dir))

def test_replace_clitic_dictionary(normalizer):
    text = "ሞ"
    result = normalizer.replace_clitic_dictionary(text)
    assert "እሞ" in result or result != text


def test_replace_shortened_words_with_dots(normalizer):
    text = "ሃ.ማ.መ.ተ.ኤ"
    result = normalizer.replace_shortened_words_with_dots(text)
    assert result != text


def test_replace_hyphenated_v1(normalizer):
    text = "ስነጥበብ ዓለም"
    result = normalizer.replace_hyphenated_v1(text)
    assert "ስነ ጥበብ" in result or result != text


def test_handle_hyphen(normalizer):
    word = "ስነ-ፍልጠት"
    result = normalizer._handle_hyphen(word)
    assert result != word


def test_handle_forward_slash(normalizer):
    word = "ቤ/ት"
    result = normalizer._handle_forward_slash(word)
    assert result != word


def test_handle_clitic(normalizer):
    word = "ሽሕ'ኳ"
    result = normalizer._handle_clitic(word)
    assert isinstance(result, str)
    assert len(result) > 0


def test_replace_improper_abbreviation(normalizer):
    text = "ሃማመተኤ ማን ዩናይትድ"
    result = normalizer.replace_improper_abbreviation(text)
    assert result != text


def test_normalize_clitic_variation(normalizer):
    text = "እዮም እውን"
    result = normalizer.normalize_clitic_variation(text)
    assert "ኢዮም" in result or "ውን" in result


def test_remove_extra_spaces():
    text = "  ሰላም  ሓወይ፥  እንታይ   ኣሎ    ሓድሽ"
    assert remove_extra_spaces(text) == "ሰላም ሓወይ፥ እንታይ ኣሎ ሓድሽ"


def test_normalize_pipeline(normalizer):
    text = "ሃ.ማ.መ.ተ.ኤ ቤ/ት ቀይሕባሕሪ ባህላዊ ምርኢት ከቕርቡ ናብ ደቀምሓረ ክኸዱ እዮም።"
    result = normalizer.normalize(text)
    assert isinstance(result, str)
    assert all(char not in result for char in ["/", "-", "."])  # ensure replacements applied


def test_normalize_and_save(normalizer, tmp_path):
    input_text = "ሃ.ብ. እሞ ቤት/ቤት እዮም"
    input_file = tmp_path / "input.txt"
    input_file.write_text(input_text, encoding="utf-8")

    output_file = "output.txt"
    normalizer.dataset = str(input_file)
    normalizer.output_dir = str(tmp_path)

    normalizer.normalize_and_save(output_file)

    output_path = tmp_path / output_file
    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "ሓበረ" in content or "እምዎ" in content or "ኢዮም" in content