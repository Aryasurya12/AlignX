# AlignX Research Reproducibility Package

## Environment Setup
AlignX requires **Python 3.11 or 3.12**.
```bash
pip install -r requirements.txt
# Requirements: streamlit, pandas, matplotlib, pytest
```

## Running the Automated Test Suite
To verify the engine correctness before generating experimental results:
```bash
PYTHONPATH="src" pytest
```

## Running Benchmarks (Phase 7)
The deterministic benchmark generator ensures repeatable results on standard sequences.
To run the fast Smoke Test (lengths up to 500):
```bash
PYTHONPATH="src" python -m experiments.run_phase7 --smoke
```

To run the Full Scaling experiments (lengths up to 8,000):
*Note: Due to the quadratic complexity of the DP baseline, this may take a few minutes.*
```bash
PYTHONPATH="src" python -m experiments.run_phase7 --scale
```

**Output Files Generated:**
- `experiments/results/phase7_smoke.csv`
- `experiments/results/phase7_correctness.csv`
- `experiments/results/phase7_scaling.csv`
- `experiments/plots/phase7_scaling_runtime.png`

## Reproducing UI Results
After running benchmarks, launch the Streamlit visualization:
```bash
streamlit run streamlit_app.py
```
Navigate to the **Phase 7 Evaluation** tab to visualize the CSV metrics in tabular format.
