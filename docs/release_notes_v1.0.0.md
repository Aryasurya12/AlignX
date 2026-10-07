# AlignX v1.0.0 Release Notes

We are thrilled to announce the v1.0.0 release of **AlignX**, a modular DNA sequence alignment framework that bridges the gap between fast heuristic approximations and the strict mathematical guarantees of Needleman-Wunsch Dynamic Programming.

## Project Purpose and Major Capabilities
AlignX divides the $O(N \cdot M)$ alignment problem into a series of smaller bounding boxes. It utilizes an anchor-based alignment workflow (via KMP or Rabin-Karp) to isolate exact matches. Unmatched gaps are evaluated via an adaptive gap-alignment selector, dynamically computing a bounded DP band size to capture indels. 
AlignX reconstructs the final global sequence, detecting and clustering structural mutations (substitutions, insertions, deletions) deterministically.

## Verification & Limitations
- **Test Status**: 128 tests verify the mathematical optimality of fallback handling and algorithmic correctness.
- **Speedup Claims**: We report speedups of 100x to 500x. **Note:** This is a best-case observed result on highly homologous sequences up to 8,000 bp. It is not a universal performance guarantee; highly divergent sequences will gracefully fall back to $O(N \cdot M)$ full DP.
- **Evaluation**: The included reproducibility assets use a synthetic benchmark generator to precisely model mutation rates. 
- **Missing Metrics**: Absolute peak-memory (RSS) footprint is analyzed via algorithmic complexity rather than direct heap tracking, and standard Python string slicing acts as a constant-factor bottleneck on high-frequency micro-gaps.

## Licensing
*(Currently Unlicensed / All Rights Reserved pending owner decision).*
