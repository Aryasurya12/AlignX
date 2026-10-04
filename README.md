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
- Phase 0 ✅
- Phase 1 ✅
- Phase 2 ✅
- Phase 3 ✅
- Phase 4 🚧 / in progress
