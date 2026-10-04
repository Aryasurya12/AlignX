from typing import List

def build_lps(pattern: str) -> List[int]:
    """
    Builds the Longest Proper Prefix which is also Suffix (LPS) array for KMP.
    """
    m = len(pattern)
    lps = [0] * m
    if m == 0:
        return lps
    
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text: str, pattern: str) -> List[int]:
    """
    Knuth-Morris-Pratt algorithm for exact pattern matching.
    Returns a list of start indices where the pattern occurs in the text.
    Handles overlapping matches.
    """
    if not pattern:
        return []
    
    n = len(text)
    m = len(pattern)
    if m > n:
        return []
        
    lps = build_lps(pattern)
    matches = []
    
    i = 0  # index for text
    j = 0  # index for pattern
    
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
            
        if j == m:
            matches.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
                
    return matches
