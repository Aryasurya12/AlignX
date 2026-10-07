# Phase 6 Plan: Research-Grade Interface, End-to-End Demonstration & Final Validation

## 1. Current Architecture
AlignX is structured as a modular pipeline:
- `anchoralign.pipeline.orchestrator.run_pipeline` is the primary entry point.
- Models in `anchoralign.models` define configuration, anchors, gaps, alignments, mutations, and the `PipelineResult`.
- Existing UI (`streamlit_app.py`) is rudimentary, only covering Phase 1 (Anchors).

## 2. Reusable Components
- **Core Pipeline**: `run_pipeline(ref, query, config)` returns a full `PipelineResult` with anchors, gaps, alignments, and mutations.
- **Baseline**: `anchoralign.evaluation.baseline.full_sequence_align` computes Full DP ground truth.
- **Metrics**: `anchoralign.evaluation.metrics` can compute speedups, correctness, and anchor coverage.
- **Experiments**: `experiments/results` and `experiments/plots` hold Phase 4 and 5 data.

## 3. Existing UI Limitations
The current `streamlit_app.py`:
- Only exposes anchor algorithm parameters.
- Does not show gaps, alignments, mutations, or selector decisions.
- Lacks comparison against Full DP.
- Lacks export capabilities.
- Lacks experiment browsing.

## 4. Planned Implementation Steps

### Phase 6B: Professional UI
- Rewrite `streamlit_app.py` as a multipage-style application using `st.tabs` or sidebar navigation.
- Main sections: Overview, Sequence Input, Alignment, Anchor/Gap Analysis, Mutations, Decision Inspector, Baseline Comparison, Experiments, Export.

### Phase 6C: Alignment Visualization
- Create a chunked or wrapped text representation of the aligned sequence strings to visualize matches, mismatches, and gaps.

### Phase 6D: Anchor and Gap Analysis
- Tabulate anchors and gaps.
- Show gap intervals, lengths, and disparity.

### Phase 6E: Mutation Analysis
- Summarize mutations with start/end positions and reference/query alleles.

### Phase 6F: Explainable Decision Inspector
- Utilize `Gap.decision_metadata`, `AlignmentResult.strategy`, and `AlignmentResult.decision_metadata` to reconstruct the decision trace.

### Phase 6G: Full DP Baseline Comparison
- Run `full_sequence_align` from the baseline module alongside the pipeline and compare scores, string identity, and runtime.

### Phase 6H: Experiment Explorer
- Read CSVs from `experiments/results/` and display tables/plots.

### Phase 6I: Reproducible Export
- Provide JSON/CSV download buttons for pipeline outputs.

### Phase 6J & 6K: Demonstration & Safety
- Include sample sequences as presets.
- Add `docs/demo_guide.md`.
- Gracefully handle large inputs, errors, and missing files.

### Phase 6L & 6M: Testing and Documentation
- Write `tests/integration/test_ui_exports.py` or similar to validate export payloads.
- Update `README.md` and architecture documentation.

## 5. Baseline Test Results
- Baseline tests successfully passed (117 / 117).
- No regressions found.
