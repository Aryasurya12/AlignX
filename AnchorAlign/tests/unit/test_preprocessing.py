import pytest
from anchoralign.preprocessing.sequence import preprocess_sequence

def test_uppercase_conversion():
    assert preprocess_sequence("acgt") == "ACGT"

def test_valid_dna():
    assert preprocess_sequence("ACGTN") == "ACGTN"

def test_invalid_dna():
    with pytest.raises(ValueError):
        preprocess_sequence("ACGTX")

def test_empty_sequence():
    assert preprocess_sequence("") == ""
