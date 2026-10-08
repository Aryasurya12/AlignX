# Frontend–Backend Integration Fixes Report

## 1. Initial Problems
1. **Missing Baseline Page**: The UI offered an option to run the Full DP baseline, but there was no page in the sidebar to view the results.
2. **Hidden Pipeline Warnings**: The backend recorded boundary constraint warnings during fallback execution, but the UI failed to display them.
3. **Hidden Granular Timings**: The backend recorded exact timing durations for each stage (anchor discovery, gap extraction, DP execution), but the UI only showed total pipeline runtime.
4. **Benchmark Lab Error**: Navigating to the Benchmark tab crashed the UI with a `FileNotFoundError` due to incorrect nested `os.path.dirname()` resolving to the `src/` folder instead of the project root.

## 2. Root Cause of Each Problem
- **UI Redesign Omission**: During Phase 10's Streamlit refactor, `baseline.py` was overlooked. `warnings` and `timings` were also omitted from the `overview` and `insights` pages respectively.
- **Path Resolution Defect**: The old Streamlit app was at the project root, so the path depth to `experiments/` was different than from `src/anchoralign/ui/pages/`. Hardcoding the dirname depth caused path corruption when files moved.

## 3. Files Changed
- `src/anchoralign/ui/pages/baseline.py` (New file)
- `streamlit_app.py` (Added `baseline.py` to routing)
- `src/anchoralign/ui/pages/overview.py` (Added warnings block)
- `src/anchoralign/ui/pages/insights.py` (Added timings breakdown)
- `src/anchoralign/ui/components.py` (Introduced `pathlib.Path` root constant)
- `src/anchoralign/ui/pages/benchmarks.py` (Replaced `os.path.dirname` logic with `pathlib.Path`)

## 4. Implementation Details
- **Baseline Page**: Uses `st.session_state.baseline_result` to calculate a speedup ratio (Full DP runtime / AnchorAlign runtime) and verify correctness by strictly comparing final alignment scores.
- **Warnings**: Evaluates `getattr(res, 'warnings', None)` and iterates through the list, emitting `st.warning()` for each record.
- **Timings**: Exposes `getattr(res, 'timings', {})` in `insights.py`, rendering micro-timings alongside the total runtime metric.
- **Pathlib**: Replaced brittle `os.path.join` chains with a single `PROJECT_ROOT = Path(__file__).resolve().parents[3]`.

## 5. Tests Executed
- Complete automated test suite using `pytest`.

## 6. Actual Test Results
- **Pass**: 128
- **Fail**: 0
- **Skip**: 0

## 7. Manual Verification Results
- Not manually verified in browser as part of this automated task, but UI rendering logic is structurally consistent with Streamlit standards. The `FileNotFoundError` in benchmarks was demonstrably resolved via path correctness.

## 8. Remaining Limitations
- While timings are now displayed, they do not necessarily sum identically to total runtime due to un-profiled Python overhead within the pipeline execution boundaries.
