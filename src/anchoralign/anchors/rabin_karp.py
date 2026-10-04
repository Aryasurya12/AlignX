from typing import List

def rabin_karp_search(text: str, pattern: str, base: int = 256, modulus: int = 101) -> List[int]:
    """
    Rabin-Karp algorithm for exact pattern matching using a rolling hash.
    Returns a list of start indices where the pattern occurs in the text.
    Handles overlapping matches.
    """
    if not pattern:
        return []
        
    n = len(text)
    m = len(pattern)
    if m > n:
        return []
        
    matches = []
    
    p_hash = 0
    t_hash = 0
    h = 1
    
    # Calculate h = pow(base, m-1) % modulus
    for _ in range(m - 1):
        h = (h * base) % modulus
        
    # Calculate initial hashes
    for i in range(m):
        p_hash = (base * p_hash + ord(pattern[i])) % modulus
        t_hash = (base * t_hash + ord(text[i])) % modulus
        
    for i in range(n - m + 1):
        # If hashes match, verify characters to avoid false positives from collisions
        if p_hash == t_hash:
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                matches.append(i)
                
        # Roll the hash
        if i < n - m:
            t_hash = (base * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % modulus
            if t_hash < 0:
                t_hash += modulus
                
    return matches
