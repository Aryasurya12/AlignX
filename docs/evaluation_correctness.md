# Phase 4 Evaluation Correctness

## Full DP usage
Full-sequence Dynamic Programming (Full DP) serves as the mathematical ground truth. It is guaranteed to find an alignment with the optimal global score given a set of penalties.

## Agreement
The primary criterion for agreement is matching the optimal alignment score computed by Full DP. The AnchorAlign pipeline is deemed correct on a synthetic case if its final reconstructed alignment achieves the exact same score as Full DP.

## Score vs Alignment Equivalence
Different optimal alignments can exist with identical scores. For example, a deletion followed by a substitution might score the same as a substitution followed by a deletion if both paths incur the same penalty. Therefore, we do not require the reconstructed strings to be character-for-character identical to the baseline, provided the scores match.

## Mutation Equivalence
Because the alignment string may vary slightly between two optimal paths, the exact coordinates and interpretation of mutations (e.g. adjacent INDELs vs substitutions) might differ. We evaluate correctness at the score level to abstract away these mathematically equivalent variations.

## Narrow-band Warnings
When Banded DP touches its boundary `|i - j| == band_width`, it flags a warning. If the optimal path drifted outside the band, the score might be suboptimal. In extreme cases (like `band_width=0` with length differences), the adaptive selector now falls back to Full DP to preserve correctness.

## Limitations of Synthetic Ground Truth
While synthetic generation provides expected mutations, the actual optimal mathematical alignment might discover a different path that scores higher (or equal) due to sequence context. Thus, comparing against the synthetic generative expectation is useful for profiling, but comparing against Full DP is required for mathematical correctness.
