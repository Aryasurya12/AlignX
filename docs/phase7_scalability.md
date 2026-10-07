# Phase 7 Scalability and Failure-Mode Analysis

## 1. Sequence-Length Scaling
- Full DP memory footprint scales at O(N*M). For sequences of length N=10,000, Full DP evaluates 100,000,000 cells.
- AlignX circumvents this quadratic barrier by resolving identical anchors. The time complexity drops to near O(N) in highly similar sequences.

## 2. Anchor-Density Scaling
- High density of microscopic gaps introduces slicing overhead. Python's string slicing `[start:end]` involves memory copies, making extremely fragmented alignments sub-optimal.
- Extremely low anchor density delegates the burden to Adaptive Banding. If divergence is high, banded width expands, eventually defaulting to Full DP.

## 3. Indel-Drift Stress
- **Long insertions near gap boundaries:** KMP correctly anchors adjacent matching blocks, but large indels push the adaptive band estimator to its limits. The `drift_factor` scales the band to contain the indel, meaning the penalty is O(L * W) where W grows with L.

## 4. Resource Safety Limitations
- The UI caps inputs at ~10,000 bases to prevent DOM/React component crashing when rendering `chunked` alignments.
- The theoretical maximum in Python memory is bounded by the recursion limit or array allocations inside `Full DP`. To exceed this, users must disable UI visualization and run purely via API.
