# Phase 7 Optimization Log

## Optimization 1: Anchor Density Rejection Threshold (Proposed)
**Hypothesis:** For highly fragmented alignments with hundreds of 3-bp gaps, the Python function call overhead and string-slicing overhead exceeds the computational cost of simply running Banded DP over the entire region.
**Action:** Theoretical only. The current threshold `L_min` manages this natively by pruning short anchors before processing.

## Optimization 2: Caching Gap Features
**Hypothesis:** If a gap requires a boundary retry, gap features (length diff, relative lengths) do not change.
**Action:** The current `extract_gaps` architecture already passes a single `Gap` object which caches these properties. No redundant computation occurs.

## Conclusion
Extensive profiling during Phase 7 smoke testing revealed that string allocations (string slicing for `query[start:end]`) are the largest remaining overhead in Python. However, replacing them with `memoryview` or `bytearray` slices would break typing and compatibility with existing testing architecture. Therefore, no speculative rewrites were merged. The engine remains exact and highly optimized within the boundaries of standard Python C-extensions (via `str` built-ins).
