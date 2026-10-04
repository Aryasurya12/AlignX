import pytest
from anchoralign.mutations.mutation_detector import detect_mutations_engine

def test_no_mutations():
    muts = detect_mutations_engine("ACGT", "ACGT")
    assert len(muts) == 0

def test_substitution():
    muts = detect_mutations_engine("ACGT", "ACAT")
    assert len(muts) == 1
    assert muts[0].type == "substitution"
    assert muts[0].reference_sequence == "G"
    assert muts[0].query_sequence == "A"
    assert muts[0].reference_position == 2
    assert muts[0].query_position == 2

def test_insertion():
    muts = detect_mutations_engine("AC-GT", "ACAGT")
    assert len(muts) == 1
    assert muts[0].type == "insertion"
    assert muts[0].reference_sequence == ""
    assert muts[0].query_sequence == "A"
    assert muts[0].reference_position == 2
    assert muts[0].query_position == 2

def test_deletion():
    muts = detect_mutations_engine("ACAGT", "AC-GT")
    assert len(muts) == 1
    assert muts[0].type == "deletion"
    assert muts[0].reference_sequence == "A"
    assert muts[0].query_sequence == ""
    assert muts[0].reference_position == 2
    assert muts[0].query_position == 2

def test_multiple_base_events():
    muts = detect_mutations_engine("AC---GT", "ACAAAGT")
    assert len(muts) == 1
    assert muts[0].type == "insertion"
    assert muts[0].query_sequence == "AAA"
    
    muts2 = detect_mutations_engine("ACGGGT", "AC---T")
    assert len(muts2) == 1
    assert muts2[0].type == "deletion"
    assert muts2[0].reference_sequence == "GGG"

def test_consecutive_different_events():
    muts = detect_mutations_engine("AC-GT", "ACT-T")
    assert len(muts) == 2
    assert muts[0].type == "insertion"
    assert muts[1].type == "deletion"
