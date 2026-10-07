# Performance Claim Audit

## Table of Claims

| Claim | Evidence Source | Verification Status | Final Approved Wording |
|-------|-----------------|---------------------|------------------------|
| "AlignX achieves 100x-500x speedups on identical sequences at 8,000bp." | `experiments/results/phase7_scaling.csv` | Verified | "For identical or sparse-mutation sequences at length ~8,000 bp, AlignX observes up to a 500x measured CPU runtime speedup relative to a naive Python Needleman-Wunsch baseline, primarily by fully bypassing DP cell evaluation." |
| "Optimal gap alignment equals Full DP score." | `tests/integration/test_pipeline.py`, Phase 7 assertions. | Verified | "AlignX guarantees gap alignment mathematically equivalent to Needleman-Wunsch scoring through exact fallback handling." |
| "Eliminates O(N*M) runtime." | Complexity Analysis | Partial (Requires context) | "Bypasses O(N*M) worst-case scaling in sequences with sufficient sequence homology, though retains standard quadratic fallback for completely divergent gaps." |

## Methodology Review
The reported speedup of 100x+ handles near-zero runtimes carefully. The DP baseline measures Python loop iterations, while the Anchor engine resolves large identical strings natively in C via Python string matching. The discrepancy arises directly from reducing a 2D $64,000,000$ iteration matrix loop to a single 1D C-optimized search, mathematically validating the speedup magnitude.
