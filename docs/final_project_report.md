# Final Project Report: AlignX

**Project Title:** AlignX: Adaptive Anchor-Guided DNA Sequence Alignment
**Institution:** Placeholder University
**Department:** Department of Computer Science / Bioinformatics
**Student:** Aryasurya12
**Supervisor:** Placeholder

## 1. Problem Statement
Global DNA sequence alignment via Dynamic Programming guarantees mathematically optimal alignments but scales at $O(N^2)$ memory and time. This project aims to drastically reduce the matrix evaluation space while strictly preserving the optimality guarantees.

## 2. Objectives and Scope
To build a Python-based pipeline that:
1. Discovers exact anchors using KMP/Rabin-Karp.
2. Extracts and evaluates gaps.
3. Dynamically selects Banded DP or Full DP.
4. Asserts correctness through round-trip gap reconstruction.
5. Provides a Streamlit UI for visual inspection and research validation.

## 3. System Architecture
The system employs a heavily separated architecture. `src/anchoralign` contains purely algorithmic, stateless classes operating on data models (`result.py`, `gap.py`, `anchor.py`). The presentation layer is decoupled into `streamlit_app.py`, mapping pipeline results directly to tabular metrics.

## 4. Implementation Details
The codebase uses standard library features extensively, minimizing external dependencies (only `streamlit`, `pandas`, and `pytest` are used). The `PipelineResult` object captures detailed execution metadata, including `retry_count` and `fallback_used`, exposing the internal decision logic to the UI's Decision Inspector.

## 5. Experimental Evaluation
Evaluation was conducted deterministically. A `BenchmarkGenerator` synthesized 6 Families of datasets, capturing substitutions, indels, and repetitive patterns. 
Measurements confirmed mathematical correctness against standard Needleman-Wunsch, validating the `boundary_touched` hypothesis.

## 6. Limitations
AlignX retains an $O(N \cdot M)$ worst-case cost. If sequences share zero sequence similarity, zero anchors are discovered. The adaptive banding fails to find a safe narrow width, forcing a Full DP fallback. This represents a safe degradation rather than a pipeline failure.

## 7. Conclusion
The AlignX project successfully implements a modular, research-grade, explainable DNA alignment framework. It is structurally prepared for publication or academic review.
