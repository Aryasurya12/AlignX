import pytest
from anchoralign.anchors.rabin_karp import rabin_karp_search

def test_rk_no_match():
    assert rabin_karp_search("ACGT", "TGCA") == []

def test_rk_one_match():
    assert rabin_karp_search("ACGTACGT", "GTA") == [2]

def test_rk_multiple_matches():
    assert rabin_karp_search("ACGTACGT", "CGT") == [1, 5]

def test_rk_overlapping_matches():
    assert rabin_karp_search("AAAA", "AA") == [0, 1, 2]

def test_rk_repeated_pattern():
    assert rabin_karp_search("ATATATAT", "ATAT") == [0, 2, 4]

def test_rk_single_char():
    assert rabin_karp_search("ACGTACGT", "A") == [0, 4]

def test_rk_pattern_longer():
    assert rabin_karp_search("ACG", "ACGT") == []

def test_rk_pattern_equal():
    assert rabin_karp_search("ACGT", "ACGT") == [0]

def test_rk_hash_collision():
    # Construct strings that might collide with a small modulus
    # Let's use a very small modulus and see if character verification works
    # Using base=10, mod=5. "A" (65) % 5 = 0. "F" (70) % 5 = 0. 
    # Hash for A is 0, F is 0.
    text = "A F A F"
    pattern = "F"
    matches = rabin_karp_search(text, pattern, base=10, modulus=5)
    # The actual matches for F should be at indices 2 and 6.
    assert matches == [2, 6]

def test_rk_configurable_base_modulus():
    assert rabin_karp_search("ACGT", "CG", base=256, modulus=101) == [1]
