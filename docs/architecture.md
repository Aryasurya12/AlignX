# Architecture

## 4. Pipeline Architecture
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
Gap Features
        ↓
Adaptive Selector
        ↓
Adaptive Band Estimation
        ↓
Banded DP
        ↓
Boundary Check
        ↓
Retry / Wider Band
        ↓
Full DP Fallback
        ↓
Reconstruction
        ↓
Mutation Detection
        ↓
Compound Clustering
        ↓
Evaluation
