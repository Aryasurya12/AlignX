# AlignX Final Presentation

## Slide 1: Title and Team
**Title:** AlignX: Anchor-Guided DNA Sequence Alignment  
**Main Message:** Introducing an exact, adaptive sequence aligner.  
**Talking Points:** 
- AlignX bridges heuristic speeds and mathematically exact DP guarantees.

## Slide 2: Problem Statement
**Title:** The O(N^2) Bottleneck  
**Main Message:** Classical DP alignment memory and time scale quadratically.  
**Talking Points:** 
- Needleman-Wunsch is unscalable for large genomic strings, calculating millions of matrix cells that represent unreachable evolutionary paths.

## Slide 3: Proposed Architecture
**Title:** Anchor-Guided Decomposition  
**Main Message:** Divide and Conquer.  
**Suggested Visual:** Reference to Figure 1 (Architecture).  
**Talking Points:** 
- Use fast linear search (KMP) to isolate exact matches (Anchors).
- The space between anchors (Gaps) becomes a set of isolated, smaller alignment problems.

## Slide 4: Adaptive Banding & Fallback
**Title:** Evidence-Based Gap Alignment  
**Main Message:** Dynamically size DP matrices.  
**Talking Points:**
- If a gap is divergent, we expand the DP band. 
- If the traceback algorithm hits the band boundary, we discard and retry, ensuring we never miss the true optimal path.

## Slide 5: Performance Results
**Title:** Empirical Evaluation  
**Main Message:** 100x - 500x Speedup on similar sequences.  
**Suggested Visual:** Plot of Runtime vs. Sequence Length.  
**Talking Points:** 
- Identical and sparse-mutation sequences bypass DP scaling limits.
- Exact fallback preserves correctness without approximation.

## Slide 6: Demonstration
**Title:** Streamlit UI  
**Main Message:** Interactive visualization of structural variants.  
**Talking Points:** 
- Load preset datasets.
- Inspect the selector's decision trace in real-time.

## Slide 7: Conclusion
**Title:** Summary and Future Work  
**Main Message:** A safe, explainable algorithmic pipeline.  
**Talking Points:** 
- Resolves the quadratic scaling limit for high-homology strings.
- Future work: GPU batch processing for disjoint gaps.
