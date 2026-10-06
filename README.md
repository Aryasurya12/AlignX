# AnchorAlign

Adaptive Anchor-Guided DNA Sequence Alignment

## Problem Statement
Traditional sequence alignment algorithms like Full Dynamic Programming (DP) are computationally expensive and do not scale well for long DNA sequences with high similarity.

## Core Idea
Identify long exact matching regions called ANCHORS and perform expensive dynamic-programming alignment only inside the remaining GAPS.

## Architecture
Reference + Query
        ↓
Preprocessing
        ↓
Anchor Engine
        ↓
Ordered Anchors
        ↓
Gap Extraction
        ↓
Gap Classification
        ↓
Adaptive Selector
        ↓
Banded DP / Full DP
        ↓
Alignment Reconstruction
        ↓
Mutation Detection
        ↓
Compound Clustering
        ↓
FinalResult

## Technology Stack
- Python 3.11+
- pytest

## Current Development Status
- Phase 0 — Foundation       ✅
- Phase 1 — Anchor Engine    ✅
- Phase 2 — Adaptive Align   ✅
- Phase 3 — Reconstruction   ✅
- Phase 4 — Evaluation       ✅
- Phase 5 — Optimization     🚧 / current

## Research Contribution
AnchorAlign demonstrates that dynamic programming boundaries (band widths) do not need to be static. By leveraging anchor-derived gap length disparities and mismatch ratios, AnchorAlign can adaptively scale its DP band for each independent gap. Coupled with a boundary-aware retry and Full DP fallback, this evidence-based selector approach significantly reduces unnecessary DP matrix computations without sacrificing optimality.
