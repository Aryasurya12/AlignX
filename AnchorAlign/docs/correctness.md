# Correctness

## Reconstruction Invariants
- `len(aligned_reference) == len(aligned_query)`
- Removing gap characters from `aligned_reference` strictly reproduces the original `reference`.
- Removing gap characters from `aligned_query` strictly reproduces the original `query`.
- Anchor sequences appear exactly in the reconstructed alignment without duplication or omission.

## Mutation Validation
Mutation coordinates are tracked simultaneously with alignment columns. 
A warning (`boundary_touched`) is propagated if Banded DP reaches its evaluation edge, as it may indicate an optimal path outside the band.

## Banded-DP Warning Propagation
Phase 3 perfectly propagates the `boundary_touched` flag as a warning in the `FinalResult`. The alignment is presented as-is without false claims of global optimality in such cases.
