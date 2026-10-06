# Phase 5 Selector Analysis

## 1. Audit of Phase 4 Results

From the generated Phase 4 results (`similarity_results.csv`, `band_width_results.csv`, `lmin_results.csv`, `anchor_coverage_results.csv`, `scaling_results.csv`), several key observations emerge:

- **Correctness Dependency on Band Width**: When the fixed band width falls below the difference between the reference gap length and query gap length, the optimal path is clipped (boundary touched). In Phase 4, a safety fallback to Full DP was necessary for `band_width=0`.
- **Runtime and Gap Count**: High similarity scenarios (e.g., 99%) result in many anchors but very small gaps, where a fixed large band width is computationally wasteful. Conversely, low similarity introduces large gaps where Banded DP without adaptive scaling might falsely clip optimal indels, resulting in boundary warnings and Full DP fallbacks.
- **Unnecessary Full DP Selection**: The gap classifier (`gap_classifier.py`) in Phase 4 uses a static `gap_length_threshold` (default 50) and `gap_mismatch_threshold` (0.2). This means that *any* gap longer than 50 bases falls back to Full DP, even if its reference and query lengths are identical and it requires only a narrow band! This is a massive missed opportunity for speedup in medium-to-long sequence alignments with long but similar gaps.

## 2. Current Selector Behavior

**Current Decision Logic**:
The gap is classified by `gap_classifier.py`:
1. `is_short = gap.reference_length <= config.gap_length_threshold and gap.query_length <= config.gap_length_threshold`
2. `is_matched = gap.mismatch_ratio <= config.gap_mismatch_threshold`

If both are true, it assigns `short_length_matched`.
Then `selector.py` chooses:
- `banded_dp` for `short_length_matched` with a static `config.band_width` (default 100).
- `full_dp` for all others.

**Features Available**:
For every gap, we can compute:
- `reference_gap_length`: length of reference gap slice.
- `query_gap_length`: length of query gap slice.
- `length_difference`: `abs(reference_gap_length - query_gap_length)` (direct minimum bound for indel magnitude).
- `length_ratio`: `min(r, q) / max(r, q)` if `max(r, q) > 0`.
- `mismatch_ratio`: Existing feature `abs(r - q) / max(r, q, 1)`.

## 3. Identified Weaknesses
- **Static Gap Length Threshold**: Abandons Banded DP on long gaps, forcing $O(r \times q)$ even when length difference is 0.
- **Static Band Width**: Uses a massive 100-base band width on a 5-base gap, doing unnecessary computations. Or, uses a 100-base band width on a gap where length difference is 200, guaranteeing failure.
- **Binary Classification**: Only chooses fixed banded or full DP.

## 4. Path to Phase 5 Optimization
We will transform the selector to an evidence-based model:
1. **Adaptive Selection**: Instead of a strict length limit, allow Banded DP for *any* gap where the length difference and sequence context suggests the optimal path stays near the diagonal.
2. **Adaptive Band Estimation**: Rather than fixed `band_width=100`, estimate required band: `estimated_band = length_difference + band_safety_margin`.
3. **Boundary-Aware Retry**: If a gap alignment touches the boundary, it doesn't immediately default to Full DP. We can exponentially grow the band (up to a limit) to find the path, ultimately falling back to Full DP if safety is not met.
