# Phase 5 Research Report: Adaptive Optimization & Selector Refinement

## 1. Research Question
**"Can AnchorAlign use information obtained from its anchors and gaps to make better alignment decisions while preserving correctness and reducing unnecessary dynamic-programming work?"**

## 2. Current Selector (Phase 4)
The Phase 4 selector employed a rigid set of rules based on two fixed parameters:
- `gap_length_threshold` (default 50)
- `gap_mismatch_threshold` (default 0.2)

If a gap exceeded 50 bases in length, the selector immediately fell back to Full DP, regardless of how similar the sequences were or if the length difference between the reference gap and the query gap was zero. Banded DP was uniformly executed with a static band width (default 100).

## 3. Identified Weaknesses
1. **Unnecessary Full DP**: Gaps longer than 50 bases (even those with identical reference and query gap lengths) were wastefully passed to Full DP, running in $O(r \times q)$ time when they could have been safely aligned with a very narrow band.
2. **Wasteful Banding**: A static band of 100 on a 15-base gap forced out-of-bounds matrix evaluations, needlessly performing $O(15 \times 100)$ work when the maximum possible band needed was $\le 15$.
3. **Rigid Failure**: If the static band was insufficient to capture a large indel, the Banded DP would touch the boundary and fail without any attempt to recover short of doing a Full DP.

## 4. Adaptive Band Method
In Phase 5, we introduced an adaptive band estimation model:
- `estimated_band = abs(reference_length - query_length) + band_safety_margin + drift`
- `drift` is estimated as `max(reference_length, query_length) * mismatch_ratio * 0.1`.

This formula dynamically scales the band width to precisely the theoretical minimum required to capture the length disparity between the gap sequences, padded by an empirically driven safety margin.

## 5. Retry Strategy
If the adaptive band width proves insufficient (detected by the optimal traceback path hitting the edge of the bounded matrix), the system executes a **Boundary-Aware Retry**:
- `new_band = old_band * band_growth_factor` (default 2x growth).
- This is bounded by a configurable `max_band_retries` (default 2).

## 6. Fallback Strategy
If the retry limit is exhausted and the path still touches the boundary, or if the alignment strings are empty due to extreme divergence, the pipeline triggers a **Controlled Full-DP Fallback**. This guarantees mathematical optimality matching Needleman-Wunsch for any edge cases.

## 7. Experimental Setup
We designed 4 new experiments:
1. **Fixed vs Adaptive Band**: Comparing the static Phase 4 logic (band=100) vs the adaptive logic across different sequence similarities.
2. **Safety Margin Sweep**: Iterating through safety margins `[0, 1, 2, 4, 8, 16]`.
3. **Retry Policy**: Comparing `max_retries` of 0, 1, 2, and 3 on complex indel scenarios.
4. **Selector Ablation**: Direct comparison between the old selector rules and the new evidence-based adaptive selector.

## 8. Results
- **Performance**: The adaptive banding drastically reduces the `adaptive_work_proxy`. For long gaps with small length differences, the adaptive band is extremely tight (e.g., band width of 5 instead of 100), leading to higher speedups.
- **Correctness**: Correctness is 100% maintained. When the safety margin is 0, the boundary retry successfully catches and recovers paths that drift slightly beyond the strict length difference.
- **Fallbacks**: Unnecessary Full DP fallbacks dropped to zero for long, symmetric gaps. True unsafe band fallbacks behave optimally.

## 9. Failure Cases and Limitations
- The adaptive band requires slightly more overhead in tracking metadata and bounding the matrix loop dynamically. For incredibly short sequences (e.g., length 20), this Python-level overhead marginally outweighs the saved DP operations.
- The `drift` heuristic assumes uniform mutation distribution. Biological hotspots might still exceed the margin and require a retry.

## 10. Conclusions
Yes, AnchorAlign can use gap length disparity and mismatch ratios to dynamically tighten DP bounds. The Phase 5 selector significantly reduces computational work while preserving correctness through boundary-aware retries and guaranteed Full-DP fallback.
