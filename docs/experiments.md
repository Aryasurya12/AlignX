# Phase 4 Experimental Methodology

## 1. Research Question
Does AnchorAlign actually reduce computational work compared with full-sequence dynamic programming while preserving correctness under the tested conditions?

## 2. Baseline
The primary computational baseline is a full-sequence, unbanded global Dynamic Programming (Needleman-Wunsch) alignment. It operates over the entire reference and query sequences to find the optimal global alignment score.

## 3. Synthetic Data Generation
We developed a synthetic ground truth generator that creates controlled reference and query sequence pairs. Mutations are introduced probabilistically from right to left (to avoid coordinate shifting during generation).

## 4. Similarity Levels
The experiments sweep across target similarities: 99%, 95%, 90%, 85%, and 80%. Actual similarities are computed after generation.

## 5. Sequence Lengths
The scaling experiment evaluates performance across sequence lengths of 500, 1000, 2000, and 5000 base pairs to study the asymptotic behavior of both approaches.

## 6. Mutation Model
The synthetic mutation generator introduces substitutions, insertions, and deletions with predefined probabilities (Sub: 0.6, Ins: 0.2, Del: 0.2).

## 7. L_min
The L_min parameter is swept across values (5, 8, 10, 15, 20) to study the trade-off between the number of anchors and gap sizes.

## 8. Band Widths
We evaluate various band widths (0, 1, 2, 4, 8, 16, 32) to determine the threshold at which Banded DP becomes reliable for the tested synthetic data without clipping the optimal alignment path.

## 9. Clustering k
The clustering parameter `k` is swept (0, 1, 2, 3, 5, 10) to study its effect on grouping consecutive small mutations into compound events.

## 10. Runtime Methodology
We use `time.perf_counter()` to measure the wall-clock execution time of the full sequence alignment. The measurements are taken over multiple repetitions with deterministic random seeds to ensure stable comparisons.

## 11. Memory Methodology
Peak memory tracking is stubbed but reserved for future implementation using `tracemalloc`. 

## 12. Correctness Criteria
Correctness is strictly defined as an exact match of the optimal alignment score between the AnchorAlign adaptive pipeline and the Full-DP baseline. 

## 13. Reproducibility
All experiments are saved with corresponding configurations in JSON format (including the random seed, generation parameters, and algorithm configuration). This ensures that every result point can be deterministically reproduced.

## 14. Limitations
The synthetic ground truth data models independent random mutations, which may not accurately reflect true biological mutation distributions (e.g. mutation hotspots, large structural variations). The results presented are strictly empirical measurements of this implementation under these specific synthetic conditions.
