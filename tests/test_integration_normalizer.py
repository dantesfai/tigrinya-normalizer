import pytest
from tigrinya_normalizer.normalizer import TigrinyaNormalizer
from unittest import mock

@pytest.fixture(scope="module")
def full_normalizer():
    # Use real dictionary path
    return TigrinyaNormalizer(dict_path="dictionaries")


# Test 1: Integration — .normalize()
def test_normalize_full_text(full_normalizer):
    text = "ሃ.ማ.መ.ተ.ኤ ቤ/ት ቀይሕ-ባሕሪ ባህላዊ ምርኢት ከቕርቡ ናብ ደቀምሓረ ክኸዱ እዮም ።"
    expected_keywords = ["ሃገራዊ ማሕበር መንእሰያትን ተማሃሮን ኤርትራ", "ቤት ትምህርቲ", "ቀይሕ ባሕሪ", "ኢዮም", "።"]

    result = full_normalizer.normalize(text)

    for word in expected_keywords:
        assert word in result
    assert isinstance(result, str)  # punctuation removed unless specified


# Test 2: Integration — .normalize() with punctuation kept
def test_normalize_keep_punctuation(full_normalizer):
    text = "ቤ/ት ስነ-ኪነት ማይ-ሓባር ብዙሓት ተማሃሮ ኣመሪቓ።"
    result = full_normalizer.normalize(text, punctuation_to_keep="።")
    assert "።" in result
    assert "ቤት ትምህርቲ" in result


# Test 3: Integration — .normalize_and_save() with temporary file
def test_normalize_and_save_with_tempfile(full_normalizer, tmp_path):
    input_text = "ሃ.ማ.መ.ተ.ኤ ቤ/ት ቀይሕ-ባሕሪ ባህላዊ ምርኢት ከቕርቡ ናብ ደቀምሓረ ክኸዱ እዮም።"
    input_file = tmp_path / "input.txt"
    input_file.write_text(input_text, encoding="utf-8")

    output_file = tmp_path / "normalized.txt"

    full_normalizer.dataset = str(input_file)
    full_normalizer.output_dir = str(tmp_path)
    full_normalizer.normalize_and_save("normalized.txt", punctuation_to_keep="።፧")

    assert output_file.exists()
    output_text = output_file.read_text(encoding="utf-8")

    assert "ሃገራዊ ማሕበር መንእሰያትን ተማሃሮን ኤርትራ" in output_text
    assert "።" in output_text
    assert "ኢዮም" in output_text
