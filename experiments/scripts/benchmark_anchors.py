import time
from anchoralign.anchors.kmp import kmp_search
from anchoralign.anchors.rabin_karp import rabin_karp_search

def run_benchmark():
    text = "ACGT" * 10000 + "AAAA" + "ACGT" * 10000
    pattern = "AAAA"
    
    print("Benchmarking KMP vs Rabin-Karp")
    print(f"Text length: {len(text)}")
    print(f"Pattern length: {len(pattern)}")
    
    # KMP
    start = time.perf_counter()
    kmp_matches = kmp_search(text, pattern)
    kmp_time = time.perf_counter() - start
    
    # RK
    start = time.perf_counter()
    rk_matches = rabin_karp_search(text, pattern)
    rk_time = time.perf_counter() - start
    
    assert len(kmp_matches) == len(rk_matches)
    
    print(f"Matches found: {len(kmp_matches)}")
    print(f"KMP time: {kmp_time:.5f}s")
    print(f"Rabin-Karp time: {rk_time:.5f}s")

if __name__ == "__main__":
    run_benchmark()
