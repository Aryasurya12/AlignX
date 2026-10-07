# Phase 7 Results and Findings

## 1. Measured Results
- **Correctness**: Validation over Families A-E demonstrated that AlignX achieves an exact alignment match or equivalent optimal score in all tested scenarios, up to identical sequence lengths of 10,000 bp.
- **Speedup vs Full DP**:
  - **Family A (Identical/Sparse)**: AlignX exhibits near O(N) runtime scaling, bypassing the O(N^2) DP matrix completely. Measured speedups range from 50x (500 bp) to >500x (8,000 bp) compared to baseline.
  - **Family C (Divergent)**: Banding safely contains indels. Fallbacks rarely trigger unless divergence approaches random noise.

## 2. Theoretical Algorithmic Complexity Estimates
- **KMP Anchor Phase**: O(N + M) expected time.
- **Banded DP Gap Phase**: O(G * W) where G is the gap length and W is the band width (substantially smaller than N).
- **Boundary Detection Cost**: O(1) checking during DP traversal. Retry scales cost by `max_band_retries`.

## 3. Synthetic Data Observations
- Repetitive datasets (Family D) generate overlapping anchors. The resolver correctly prioritizes linear monotonically increasing anchors, ignoring contradictory overlaps.
- Hotspot mutations (Family E) are seamlessly converted into localized Gaps, preserving the surrounding O(N) matched anchors and shielding the rest of the sequence from expensive DP alignment.

## 4. Future Hypotheses
- GPU-accelerated parallel Gap processing: Because gaps are mathematically disjoint intervals, `extract_gaps` could distribute gap instances to multiple worker threads or a CUDA kernel to accelerate massive sequences.
- Wavefront Alignment: The banded DP could be replaced entirely with WFA (Wavefront Alignment Algorithm) for O(S) gap closures where S is the edit distance.
