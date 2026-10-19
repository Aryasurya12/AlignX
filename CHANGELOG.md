# Changelog

All notable changes to the AlignX project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-19

### Added
- **FASTA Parser Module (`anchoralign.preprocessing.fasta_parser`):** Full multi-record FASTA reader/writer, comment support, multiline unwrapping, and polymorphic string/file loaders.
- **Curated Biological Sequences (`data/samples/`):** Real-world benchmark sequences from NCBI: Human vs Chimp HBB beta globin CDS, SARS-CoV-2 Wuhan vs Omicron Spike RBD, and TP53 oncogenic hotspot mutant.
- **Algorithm Complexity Visualizer (`ui/pages/complexity.py` & `analysis/complexity.py`):** Interactive Big-O theoretical vs empirical comparison, logarithmic scaling simulator, matrix memory footprint analyzer, and work-saved donut chart.
- **DP Cell Evaluation Counter:** Exact cell counter instrumented in `banded_dp.py` and `full_dp.py`, quantifying matrix operations avoided (>99% work saved on high homology).
- **Pipeline Stage Timings & Tracemalloc Profiling (`pipeline.timing`):** Nanosecond-resolution per-stage execution timers and peak RAM allocation tracking.
- **Standalone Terminal Demo (`demo_full.py`):** Complete headless verification suite demonstrating biological HBB alignment, synthetic indels, memory profiling, and complexity work elimination.
- **CI/CD Pipeline (`.github/workflows/test.yml`):** Multi-version Python (3.11, 3.12) automated GitHub Actions test matrix with `pytest-cov` coverage reporting.
- **Project Governance & Polish:** Official MIT License, `.editorconfig`, comprehensive README with AoA design paradigms, and completed final project report.

### Changed
- **Default Configuration:** `adaptive_band_enabled` is now enabled by default (`True`) in `AnchorAlignConfig`.
- **UI Navigation:** Added "Algorithm Complexity" analysis page to Streamlit sidebar; enhanced Overview page with live architecture diagram and project metrics.
- **Export Capabilities:** JSON execution reports now include granular per-stage timings, memory stats, and DP cell evaluation counts.

### Validated Capabilities
- **144 Passing Tests:** 100% green unit and integration test suite across all modules.
- **100% Score Equivalence:** Verified against classical Needleman-Wunsch baseline.
- **100x–500x Measured Speedup:** Validated on sequence lengths up to 10,000 bp.
