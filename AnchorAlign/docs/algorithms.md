# Algorithms

## Reconstruction
Reconstruction deterministically stitches aligned gaps and ordered anchors. Anchor sequences are preserved exactly. Boundary consistency is validated to detect overlaps or skipped regions. Gaps within aligned components are tracked and correctly rendered.

## Mutation Detection
The complete alignment is scanned column-by-column:
- **Substitution**: `ref_base != query_base` and neither is `-`.
- **Insertion**: `ref_base == '-'` and `query_base != '-'`.
- **Deletion**: `ref_base != '-'` and `query_base == '-'`.
Consecutive events of the same type are grouped into a single multi-base mutation event. Coordinates are zero-based, referring to the start of the event.

## Compound Clustering
Nearby raw mutation events are grouped into compound events if the reference coordinate distance between the end of the previous event and the start of the current event is `<= clustering_k`. `clustering_k` is configurable in `AnchorAlignConfig`.
