# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - Unreleased

### Added
- **Phase 0:** Project foundation, domain models (Anchor, Gap, AlignmentResult, PipelineResult).
- **Phase 1:** Exact anchor discovery using Knuth-Morris-Pratt and Rabin-Karp. Monotonic anchor resolution.
- **Phase 2:** Gap extraction, gap classification, and adaptive selector heuristic.
- **Phase 3:** Full alignment reconstruction, string integration, and structural variant mutation detection (insertions, deletions, substitutions, and compound clusters).
- **Phase 4 & 5:** Ground-truth baseline evaluation against classical Needleman-Wunsch Full DP. Boundary-aware retries and Full DP exact fallback logic.
- **Phase 6:** Research-grade interactive Streamlit UI for visual inspection of anchors, mutations, and decision trace metadata.
- **Phase 7:** Deterministic synthetic benchmark generator for scalability limits.
- **Phase 8:** Complete academic research paper, presentation script, reproducibility guide, and architecture diagrams.

### Validated Capabilities
- 128 passing regression integration and unit tests.
- 100x to 500x measured speedup on sequence lengths of 8,000 bp with high homology.
- 100% equivalence optimal-score fallback against DP baselines.
