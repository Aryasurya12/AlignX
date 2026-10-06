# Complexity Analysis

## KMP
- **Time:** `O(n + m)` where `n` is reference length and `m` is query length.
- **Space:** `O(m)` to store the partial match table.

## Rabin-Karp
- **Average/Expected Time:** `O(n + m)` with a good hash function.
- **Worst-case Time:** `O(n * m)` if hash collisions are frequent (e.g. highly repetitive sequences).
- **Space:** `O(1)` for rolling hash.

## Full DP (Needleman-Wunsch)
- **Time:** `O(r * q)` where `r` is the length of the reference sequence/gap and `q` is the length of the query sequence/gap.
- **Space:** `O(r * q)` for the full matrix.

## Banded DP
- **Fixed-Band Strategy:** Uses a rigid boundary `b` for all gaps.
- **Adaptive-Band Strategy:** Calculates the exact necessary boundary for each gap independently `b = length_difference + safety_margin + drift`. 
- **Time:** Approximately `O(g * b)` where `g` is the max gap length and `b` is the dynamically estimated or statically provided `band_width`.
- **Space:** `O(g * q)` currently, though could be optimized to `O(q * b)`.
- **Note on Adaptive Band:** Adaptive banding does not change the theoretical worst-case complexity of Full DP (`O(r * q)`). If sequences have massive indels or zero homology, the adaptive retries exhaust and fall back to Full DP. The objective of adaptive banding is to reduce the *practical* dynamic programming work matrix evaluated for gaps by fitting the bounds tightly to the required indel limits.

## Reconstruction
- **Time:** `O(aligned_length)` as it iterates sequentially over anchors and aligned gaps to build the final string.
- **Space:** `O(aligned_length)` to store the reconstructed alignment arrays.

## Mutation Scanning
- **Time:** `O(aligned_length)` by sweeping left to right through the final reconstructed alignment string.
- **Space:** `O(mutations)` to store the list of extracted Mutation objects.

## Clustering
- **Time:** `O(m)` where `m` is the number of detected raw mutations. The implementation sweeps through the ordered list of mutations in a single pass.
- **Space:** `O(c)` where `c` is the number of compound events formed.

## Adaptive Pipeline Overall
The asymptotic runtime depends heavily on the sequence lengths, anchor coverage, and number/size of gaps. 
If anchor coverage is high (e.g. highly similar sequences) and gaps are small enough to trigger Banded DP, the runtime is bounded closer to `O(n + m + Σ(g_i * b))`, offering a massive speedup over `O(n * m)`.
If anchor coverage is low or gap sizes exceed thresholds (or band width falls short), the pipeline falls back to Full DP, resulting in `O(n * m)` complexity. There is no universal asymptotic improvement; it is an empirical speedup under biological/synthetic conditions of similarity.
