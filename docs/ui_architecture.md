# UI Architecture

The AlignX UI is separated conceptually from the scientific pipeline. The Streamlit layer acts as an interactive visualization suite calling into the python API.

## Layer Separation
- **Core (`src/anchoralign`)**: Stateless python modules responsible for exact alignment, feature generation, mutation scanning, and gap processing. It does not import any UI dependencies.
- **Evaluation (`experiments/`)**: Tools to mass-execute pipeline results and plot CSVs.
- **UI (`streamlit_app.py`)**: A single-page, multi-tab layout that handles state serialization, config instantiation, and rendering.

## Tab Layout
1. **Run Alignment**: Handles form inputs, sequence normalization, preset loading, and pipeline invocation. Stores results in `st.session_state`.
2. **Overview & Export**: Summarizes execution, aggregates metrics into a payload dictionary, and uses `st.download_button` for reproducibility.
3. **Alignment Visualization**: Performs chunked string formatting to render the reconstructed alignment arrays without massive DOM blowup.
4. **Anchor & Gap Analysis**: Casts `result.anchors` and `result.gaps` to Pandas DataFrames for sortable tables.
5. **Algorithm Decisions**: Iterates `result.alignments` metadata to recreate the selector execution trace.
6. **Mutation Analysis**: Maps Mutation and CompoundMutation dataclasses to readable tabular structures.
7. **Baseline Comparison**: Conditionally executes `full_sequence_align` if requested and diffs the score and string lengths.
8. **Experiment Explorer**: Reads static CSV/PNG assets from `experiments/`.

## Data Management
- No user sequences are cached globally across sessions.
- Input validation sanitizes non-nucleotide characters to ensure pipeline stability.
- Streamlit's `st.session_state` preserves the active alignment across tab navigation to prevent unnecessary re-computations.
