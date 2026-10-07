# Phase 7 Plan: Advanced Validation, Scalability & Research Benchmarking

## 1. Existing Capabilities
- AlignX currently implements an anchor-driven DNA sequence alignment engine.
- Supports adaptive banding, fallback retries, and Full DP.
- Reconstructs original strings via gaps and detects structural variants.
- Currently validates via 123 passing Pytest checks.

## 2. Experimental Questions
- Under what sequence conditions does AlignX outperform Full DP?
- How does performance change as sequence length increases?
- How do substitutions, insertions, deletions, and mixed mutations affect correctness and runtime?
- How frequently does adaptive banding require retries or Full DP fallback?
- Does the anchor-based decomposition introduce measurable overhead for short or highly repetitive sequences?
- Which sequence characteristics cause the selector to make expensive or unnecessary decisions?
- What is the practical scalability limit of the current implementation?
- Which optimizations are justified by experimental evidence?

## 3. Benchmark Design
- Build a robust deterministic benchmark generator (`experiments/benchmark_generator.py`).
- Implement 6 families of sequences (A to F) exploring length, mutation types, repetitive structures, and stress conditions.
- Output benchmark inputs along with verifiable seed/ground-truth parameters.

## 4. Correctness Criteria
- **Exact alignment match**: Strings and score match exactly.
- **Equivalent optimal score**: Score matches, alignment shape is valid but gap placement differs (common in repetitive indels).
- **Valid but non-optimal alignment**: Valid shape, score differs.
- **Invalid reconstruction**: Fails round-trip gap reconstruction.

## 5. Measurement Methodology
- **Runtime**: Isolate pipeline components using CPU time (`time.perf_counter`).
- **Algorithmic work**: Use "processed gaps", "fallback counts", and "retry metrics" instead of literal Matrix cell multiplication.
- Conduct repeated runs where practical.

## 6. Planned Datasets & Scenarios
- **Family A (Easy)**: Identical or sparse substitutions.
- **Family B (Indel-heavy)**: Variable length indels, insertions, deletions.
- **Family C (Divergent)**: Mixed substitution and indel patterns.
- **Family D (Repetitive)**: Motifs that confound anchors.
- **Family E (Localized)**: Mutation hotspots surrounded by conserved domains.
- **Family F (Scaling)**: Ranging from 500 to 10,000 base pairs to establish baseline limits.

## 7. Expected Costs & Reproducibility
- O(N*M) runtime for baseline comparisons limits safe lengths to ~10-15k.
- Random seeds and dataset properties must be logged alongside CSV outputs.
