# Phase 7 Correctness Protocol

## Principles
An alignment is a mapping between two sequences, introducing gaps to maximize a scoring function. Anchor-driven adaptive banding may place gaps differently than a standard Needleman-Wunsch fallback matrix when multiple optimal paths exist (e.g., inside homopolymers or tandem repeats). 
Therefore, exact string equality is an overly strict definition of correctness for biological sequence alignment.

## Correctness Classification
1. **Exact alignment match**: 
   - The reconstructed strings match exactly. 
   - The scores match exactly.
2. **Equivalent optimal score**: 
   - The scores match exactly.
   - The reconstructed strings differ, meaning the algorithms found alternative optimal paths through the DP matrix.
3. **Valid but non-optimal alignment**: 
   - The round-trip reconstruction strings match the original reference and query (removing gaps yields originals).
   - The score is strictly less than the baseline Full DP score.
   - Indicates adaptive banding was too tight and bounded the optimal path.
4. **Invalid reconstruction**: 
   - Removing gaps from the aligned strings fails to produce the original unaligned reference or query.
   - Indicates a severe bug in reconstruction or gap slicing.
5. **Incorrect mutation coordinates**: 
   - The mutation detector outputs variants that do not map back to the aligned string indices properly.

## Validation Procedure
1. Execute `full_sequence_align(ref, query)` to get `baseline_ref_aln`, `baseline_query_aln`, `baseline_score`.
2. Execute `run_pipeline(ref, query)` to get `alignx_res`.
3. Check reconstruction:
   - `alignx_res.final_alignment.aligned_reference.replace('-', '') == ref`
   - `alignx_res.final_alignment.aligned_query.replace('-', '') == query`
   - If False -> **Invalid reconstruction**
4. Check score:
   - If `alignx_res.final_alignment.score == baseline_score`:
     - If strings match -> **Exact alignment match**
     - If strings differ -> **Equivalent optimal score**
   - If `alignx_res.final_alignment.score < baseline_score`:
     - -> **Valid but non-optimal alignment**
   - If `alignx_res.final_alignment.score > baseline_score`:
     - (Should be mathematically impossible under exact DP) -> **Invalid score calculation**
5. Verify mutation coordinates:
   - (Implemented via structural unit tests on coordinate extraction).
