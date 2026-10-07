# AlignX Demonstration Guide

## Getting Started
AlignX provides a comprehensive research-grade UI built with Streamlit.

### Prerequisites
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Running Tests
To ensure the pipeline is mathematically exact and correctly implemented:
```bash
PYTHONPATH="src" pytest
```

### Launching the Interface
Start the application from the root directory:
```bash
streamlit run streamlit_app.py
```

## Exploring the Interface

### 1. Load an Example
Navigate to the **Run Alignment** tab. In the Presets dropdown, select `Long Indel (Requires adaptive band)` and click **Load Preset**. This populates the sequence input boxes with an example dataset designed to stress the adaptive band estimator and boundary logic.

### 2. Configure Parameters
Expand the **Alignment Configuration** section. Ensure that **Adaptive Band Enabled** is checked. If you check **Run Full DP Baseline**, the pipeline will also calculate the strict `O(N*M)` Needle-Wunsch alignment for mathematical comparison (this will take longer!).

### 3. Execute
Click **Run AlignX Pipeline**. A spinner will indicate progress.

### 4. Inspect Results
- **Overview & Export**: See the immediate speedups, alignment scores, and execution counts (e.g. how many retries occurred). You can export JSON execution reports here.
- **Alignment Visualization**: See the alignment chunks mapped out, highlighting match/mismatch density.
- **Anchor & Gap Analysis**: Look at how KMP/Rabin-Karp anchored the sequence, dividing the large string into gap problems.
- **Algorithm Decisions**: (Crucial!) Open this tab to see the exact trace. It will detail why the adaptive band estimated a specific boundary, whether it hit that boundary during traceback, and if it fell back to Full DP or scaled up the band.
- **Mutation Analysis**: A summary of biologically relevant structural variations based on the alignment results.
- **Baseline Comparison**: Verify that the AlignX fast approach produced exactly the same score and length as Full DP.
- **Experiment Explorer**: View pre-computed large-scale experiments stored in the repository.
