import pytest
from anchoralign.anchors.kmp import build_lps, kmp_search

def test_lps():
    assert build_lps("AAAA") == [0, 1, 2, 3]
    assert build_lps("ABCDE") == [0, 0, 0, 0, 0]
    assert build_lps("AABAACAABAA") == [0, 1, 0, 1, 2, 0, 1, 2, 3, 4, 5]
    assert build_lps("AAACAAAAAC") == [0, 1, 2, 0, 1, 2, 3, 3, 3, 4]
    assert build_lps("AAABAAA") == [0, 1, 2, 0, 1, 2, 3]

def test_kmp_no_match():
    assert kmp_search("ACGT", "TGCA") == []

def test_kmp_one_match():
    assert kmp_search("ACGTACGT", "GTA") == [2]

def test_kmp_multiple_matches():
    assert kmp_search("ACGTACGT", "CGT") == [1, 5]

def test_kmp_overlapping_matches():
    assert kmp_search("AAAA", "AA") == [0, 1, 2]

def test_kmp_repeated_pattern():
    assert kmp_search("ATATATAT", "ATAT") == [0, 2, 4]

def test_kmp_single_char():
    assert kmp_search("ACGTACGT", "A") == [0, 4]

def test_kmp_pattern_longer():
    assert kmp_search("ACG", "ACGT") == []

def test_kmp_pattern_equal():
    assert kmp_search("ACGT", "ACGT") == [0]

def test_kmp_empty_input():
    assert kmp_search("ACGT", "") == []
    assert kmp_search("", "A") == []
