# Phase 10: UI Redesign & Dashboard Refactoring Plan

## 1. Existing Interface Audit
Currently, `streamlit_app.py` is a monolithic 444-line script containing 10 tabs rendered dynamically. The tabs manage Sequence Input, Export, Visualization, Analysis, Mutation, Baseline, Benchmarks, and About logic. 

**Issues with current architecture:**
- The monolithic structure makes maintainability poor.
- Render logic is mixed with state management.
- Hardcoded CSS and colors limit the professional "Research Studio" aesthetic.
- Reruns re-evaluate the entire monolith.

## 2. Proposed Page Architecture
We will restructure the application using a Modular Multipage App (MPA) format, moving UI rendering into a dedicated `anchoralign/ui/` subpackage. 

**Main Entrypoint:** `streamlit_app.py`
This will configure the Streamlit page, initialize session states, set up sidebar navigation, and route to specific pages.

**UI Modules (`src/anchoralign/ui/`):**
- `theme.py`: Custom CSS injecting the dark-first scientific palette and custom typography.
- `components.py`: Reusable cards, metric blocks, and utility widgets.
- `pages/overview.py`: Landing dashboard, workflow diagrams, session metrics.
- `pages/alignment.py`: Core sequence alignment inputs, configuration, and execution.
- `pages/explorer.py`: Sequence alignment visualization (Anchors, Gaps).
- `pages/mutations.py`: Detected structural variants.
- `pages/insights.py`: Explainable decision traces for gap alignments.
- `pages/benchmarks.py`: CSV exploration and metric plotting.
- `pages/export.py`: Reproducible download generation.

## 3. Reusable Components & Dependencies
- We will rely purely on `streamlit`, `pandas`, `matplotlib`, and standard Python libraries (no external heavyweight React components needed).
- Custom HTML/CSS strings will provide gradient headers and metric card styling without relying on external plugins.

## 4. Implementation Sequence
1. Create `src/anchoralign/ui` directory structure.
2. Implement `theme.py` with custom CSS mapping the `#0B1020` to `#8B5CF6` palette.
3. Migrate execution and state logic out of monolithic UI.
4. Port existing tabs into isolated `pages/*.py`.
5. Replace `streamlit_app.py` with a lightweight sidebar navigator.
6. Verify functional equivalency by running the pipeline and inspecting results.
7. Write and run regression tests.
