# Phase 8 Evidence Audit

## Verification Table

| Claim | Evidence Source | Verification Status | Specific Action |
|-------|-----------------|---------------------|-----------------|
| Anchor-guided decomposition works correctly | `tests/unit/test_kmp.py`, `test_rabin_karp.py`, `test_anchor_resolver.py` | Verified | None |
| Adaptive banding reduces DP cells | `tests/integration/test_adaptive_phase5.py`, Phase 7 scaling logs | Verified | None |
| Boundary retries prevent suboptimal alignment | `tests/integration/test_adaptive_phase5.py`, Phase 7 logs | Verified | None |
| Exact Full DP fallback acts as safety net | `src/anchoralign/reconstruction/interfaces.py`, `tests/integration/test_pipeline.py` | Verified | None |
| 100x-500x Speedup on identical sequences | `experiments/results/phase7_scaling.csv` | Verified | Present as synthetic benchmark result, note overhead limitations on divergent sequences. |
| O(N*M) runtime complexity in divergent cases | `experiments/results/phase7_scaling.csv`, algorithm analysis | Verified | State explicitly that Fallback limits large sequence alignment. |
| Memory scaling | `docs/phase7_scalability.md` | Partial (Theoretical) | Note that actual peak memory bounds in Python were not measured natively, only inferred. |
| UI limits inputs to 10k bases | `streamlit_app.py:101` | Verified | None |

## Missing Information
- Peak RSS memory footprint during 8,000 bp divergent alignment. We explicitly report this as theoretical/unmeasured.
- Biological accuracy against standard reference tools (e.g. BLAST/BWA). We explicitly constrain claims to exact Needleman-Wunsch equivalence, rather than biological truth.
