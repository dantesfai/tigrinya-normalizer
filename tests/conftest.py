import os
import pytest
from tigrinya_normalizer.normalizer import TigrinyaNormalizer

@pytest.fixture(scope="session")
def dict_path():
    """Returns absolute path to the dictionaries directory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(base_dir, "../tigrinya_normalizer/dictionaries"))

@pytest.fixture
def sample_dataset_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "sample_data.txt")


@pytest.fixture
def normalizer(dict_path, sample_dataset_path):
    return TigrinyaNormalizer(dict_path=dict_path, dataset_file=sample_dataset_path)