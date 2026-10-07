# Figure 1: High-Level System Architecture

```mermaid
graph TD
    A[Reference & Query DNA] --> B[Preprocessing & Validation]
    B --> C[Anchor Engine: KMP / Rabin-Karp]
    C --> D[Anchor Resolution & Filtering]
    D --> E[Gap Extraction]
    
    E --> F[Adaptive Selector]
    
    F -->|Band Estimated| G[Banded DP]
    F -->|Divergent| H[Full DP]
    
    G --> I{Boundary Touched?}
    I -->|Yes| J{Retries < Max?}
    J -->|Yes| K[Widen Band & Retry]
    K --> G
    J -->|No| H
    
    I -->|No| L[Valid Alignment]
    H --> L
    
    L --> M[Alignment Reconstruction]
    M --> N[Mutation Detection & Clustering]
    N --> O[FinalResult Payload]
```
