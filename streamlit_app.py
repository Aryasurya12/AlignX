import streamlit as st
import pandas as pd
import time
import os
import json
import matplotlib.pyplot as plt
from anchoralign.pipeline.orchestrator import run_pipeline
from anchoralign.config import AnchorAlignConfig
from anchoralign.evaluation.baseline import full_sequence_align

st.set_page_config(page_title="AlignX", layout="wide")

# Helper function to get valid experiment files
def get_experiment_files():
    results_dir = os.path.join(os.path.dirname(__file__), 'experiments', 'results')
    if not os.path.exists(results_dir):
        return []
    return [f for f in os.listdir(results_dir) if f.endswith('.csv')]

def get_plot_files():
    plots_dir = os.path.join(os.path.dirname(__file__), 'experiments', 'plots')
    if not os.path.exists(plots_dir):
        return []
    return [f for f in os.listdir(plots_dir) if f.endswith('.png')]

def validate_dna(seq):
    seq = seq.upper().replace(" ", "").replace("\n", "")
    valid_chars = set("ACGTN")
    if not set(seq).issubset(valid_chars):
        return None, "Sequence contains invalid characters. Only A, C, G, T, N are supported."
    return seq, None

# State initialization
if 'pipeline_result' not in st.session_state:
    st.session_state.pipeline_result = None
if 'baseline_result' not in st.session_state:
    st.session_state.baseline_result = None
if 'config' not in st.session_state:
    st.session_state.config = None
if 'runtimes' not in st.session_state:
    st.session_state.runtimes = {}

st.title("AlignX: Adaptive Anchor-Guided DNA Sequence Alignment")
st.markdown("A research-grade framework combining anchor-based decomposition, adaptive gap alignment, boundary-aware retries, and Full DP fallback.")

tabs = st.tabs([
    "Run Alignment",
    "Overview & Export",
    "Alignment Visualization",
    "Anchor & Gap Analysis",
    "Algorithm Decisions",
    "Mutation Analysis",
    "Baseline Comparison",
    "Experiment Explorer",
    "Phase 7 Evaluation",
    "About"
])

# ----------------- 1. Run Alignment -----------------
with tabs[0]:
    st.header("Sequence Input & Configuration")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Reference Sequence")
        ref_input = st.text_area("Input Reference DNA (FASTA or Plain Text)", height=150, key="ref_in")
    with col2:
        st.subheader("Query Sequence")
        query_input = st.text_area("Input Query DNA (FASTA or Plain Text)", height=150, key="query_in")

    st.markdown("### Presets")
    preset = st.selectbox("Load an example dataset", ["None", "Identical Sequences", "Substitution", "Insertion", "Long Indel (Requires adaptive band)", "Complex (Anchors & Mutations)"])
    if st.button("Load Preset"):
        if preset == "Identical Sequences":
            st.session_state.ref_in = "ATGCGATCGATCGATCGATC" * 10
            st.session_state.query_in = "ATGCGATCGATCGATCGATC" * 10
        elif preset == "Substitution":
            st.session_state.ref_in = "ATGCGATCGATCGATCGATC" * 10
            st.session_state.query_in = "ATGCGATCG" + "T" + "TCGATCGATC" + "ATGCGATCGATCGATCGATC" * 9
        elif preset == "Insertion":
            st.session_state.ref_in = "A"*50 + "C"*50 + "G"*50 + "T"*50
            st.session_state.query_in = "A"*50 + "C"*50 + "AAAAA" + "G"*50 + "T"*50
        elif preset == "Long Indel (Requires adaptive band)":
            st.session_state.ref_in = "A" * 100 + "G" * 50
            st.session_state.query_in = "A" * 10 + "T" * 80 + "A" * 90 + "G" * 50
        elif preset == "Complex (Anchors & Mutations)":
            st.session_state.ref_in = "ACGT" * 20 + "TGCA" * 20
            st.session_state.query_in = "ACGT" * 5 + "AAAAA" + "ACGT" * 5 + "G" + "ACGT" * 9 + "TGCA" * 20
        st.rerun()

    with st.expander("Alignment Configuration", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            l_min = st.number_input("Minimum Anchor Length (L_min)", min_value=3, value=10)
            algo = st.selectbox("Anchor Algorithm", ["kmp", "rabin-karp"])
            merge_thresh = st.number_input("Anchor Merge Threshold", min_value=0, value=5)
        with c2:
            match_score = st.number_input("Match Score", value=1.0)
            mismatch_pen = st.number_input("Mismatch Penalty", value=-1.0)
            gap_pen = st.number_input("Gap Penalty", value=-1.0)
            clustering_k = st.number_input("Mutation Clustering Parameter (k)", value=3)
        with c3:
            adaptive_enabled = st.checkbox("Adaptive Band Enabled", value=True)
            band_width = st.number_input("Fixed Band Width (if not adaptive)", value=100)
            band_margin = st.number_input("Adaptive Safety Margin", value=5)
            max_retries = st.number_input("Max Band Retries", value=2)
            growth_factor = st.number_input("Band Growth Factor", value=2.0)

    run_baseline = st.checkbox("Run Full DP Baseline for Comparison (Warning: O(N*M) Time/Memory)", value=False)

    if st.button("Run AlignX Pipeline", type="primary"):
        if not ref_input or not query_input:
            st.error("Please provide both sequences.")
        else:
            # Parse FASTA if present
            ref_lines = [l for l in ref_input.split('\n') if not l.startswith('>')]
            query_lines = [l for l in query_input.split('\n') if not l.startswith('>')]
            ref_clean, err1 = validate_dna("".join(ref_lines))
            query_clean, err2 = validate_dna("".join(query_lines))

            if err1 or err2:
                st.error(err1 or err2)
            elif len(ref_clean) > 10000 or len(query_clean) > 10000:
                st.warning("Sequences exceed 10,000 bases. This interface limits sequence size to preserve memory.")
            else:
                cfg = AnchorAlignConfig(
                    L_min=l_min,
                    anchor_algorithm=algo,
                    anchor_merge_threshold=merge_thresh,
                    match_score=match_score,
                    mismatch_penalty=mismatch_pen,
                    gap_penalty=gap_pen,
                    adaptive_band_enabled=adaptive_enabled,
                    band_width=band_width,
                    band_safety_margin=band_margin,
                    max_band_retries=max_retries,
                    band_growth_factor=growth_factor,
                    clustering_k=clustering_k
                )
                st.session_state.config = cfg

                with st.spinner("Executing AlignX Pipeline..."):
                    start = time.perf_counter()
                    try:
                        res = run_pipeline(ref_clean, query_clean, cfg)
                        end = time.perf_counter()
                        st.session_state.pipeline_result = res
                        st.session_state.runtimes['pipeline'] = end - start

                        if run_baseline:
                            st.info("Running Full DP Baseline...")
                            b_start = time.perf_counter()
                            b_ref, b_query, b_score, b_runtime, b_muts = full_sequence_align(ref_clean, query_clean, cfg)
                            b_end = time.perf_counter()
                            st.session_state.baseline_result = {
                                'aligned_reference': b_ref,
                                'aligned_query': b_query,
                                'score': b_score,
                                'runtime': b_runtime,
                                'mutations': len(b_muts)
                            }
                            st.session_state.runtimes['baseline'] = b_end - b_start
                        else:
                            st.session_state.baseline_result = None

                        st.success("Pipeline Execution Complete!")
                    except Exception as e:
                        st.error(f"Execution Error: {e}")

# ----------------- 2. Overview & Export -----------------
with tabs[1]:
    st.header("Execution Overview")
    if st.session_state.pipeline_result:
        res = st.session_state.pipeline_result
        cfg = st.session_state.config

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Reference Length", res.reference_length)
        c2.metric("Query Length", res.query_length)
        c3.metric("Alignment Score", round(res.final_alignment.score, 2))
        c4.metric("Pipeline Runtime", f"{st.session_state.runtimes['pipeline']:.4f}s")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Anchors Found", len(res.anchors))
        c2.metric("Gaps Processed", len(res.gaps))
        c3.metric("Mutations Detected", len(res.mutations))
        c4.metric("Compound Events", len(res.compound_events))

        banded_count = sum(1 for a in res.alignments if a.strategy == "banded_dp")
        full_dp_count = sum(1 for a in res.alignments if a.strategy == "full_dp_fallback" or a.strategy == "full_dp")
        retries = sum(a.decision_metadata.get("retry_count", 0) for a in res.alignments if a.decision_metadata)

        st.subheader("Algorithm Breakdown")
        bc1, bc2, bc3 = st.columns(3)
        bc1.metric("Banded DP Alignments", banded_count)
        bc2.metric("Full DP Alignments (Fallback/Direct)", full_dp_count)
        bc3.metric("Total Boundary Retries", retries)

        st.divider()
        st.header("Reproducible Export")

        export_data = {
            "config": cfg.__dict__,
            "metrics": {
                "reference_length": res.reference_length,
                "query_length": res.query_length,
                "score": res.final_alignment.score,
                "anchors": len(res.anchors),
                "gaps": len(res.gaps),
                "mutations": len(res.mutations),
                "banded_count": banded_count,
                "full_dp_count": full_dp_count,
                "retries": retries,
                "runtime": st.session_state.runtimes['pipeline']
            }
        }

        st.download_button("Download Execution Report (JSON)", data=json.dumps(export_data, indent=2), file_name="alignx_report.json", mime="application/json")
        st.download_button("Download Alignment (FASTA)", data=f">Reference\n{res.final_alignment.aligned_reference}\n>Query\n{res.final_alignment.aligned_query}", file_name="alignment.fasta", mime="text/plain")

    else:
        st.info("Run an alignment to see the overview.")

# ----------------- 3. Alignment Visualization -----------------
with tabs[2]:
    st.header("Final Alignment")
    if st.session_state.pipeline_result:
        res = st.session_state.pipeline_result
        ref_aln = res.final_alignment.aligned_reference
        query_aln = res.final_alignment.aligned_query

        matches = sum(1 for r, q in zip(ref_aln, query_aln) if r == q and r != '-')
        mismatches = sum(1 for r, q in zip(ref_aln, query_aln) if r != q and r != '-' and q != '-')
        insertions = query_aln.count('-')
        deletions = ref_aln.count('-')
        identity = matches / max(len(ref_aln), 1) * 100

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Matches", matches)
        c2.metric("Mismatches", mismatches)
        c3.metric("Insertions (Query gaps)", insertions)
        c4.metric("Deletions (Ref gaps)", deletions)
        st.metric("Sequence Identity", f"{identity:.2f}%")

        st.subheader("Alignment Viewer")
        chunk_size = 100
        for i in range(0, len(ref_aln), chunk_size):
            end = min(i + chunk_size, len(ref_aln))
            r_chunk = ref_aln[i:end]
            q_chunk = query_aln[i:end]
            match_str = "".join('|' if r == q and r != '-' else ' ' for r, q in zip(r_chunk, q_chunk))

            st.code(f"Ref  [{i:04d}]: {r_chunk}\n          {' '*len(str(i))}{match_str}\nQry  [{i:04d}]: {q_chunk}", language="text")

    else:
        st.info("Run an alignment to visualize results.")

# ----------------- 4. Anchor & Gap Analysis -----------------
with tabs[3]:
    st.header("Anchor & Gap Analysis")
    if st.session_state.pipeline_result:
        res = st.session_state.pipeline_result

        st.subheader("Anchors")
        if res.anchors:
            df_anchors = pd.DataFrame([{
                "Ref Start": a.reference_start,
                "Ref End": a.reference_end,
                "Qry Start": a.query_start,
                "Qry End": a.query_end,
                "Length": a.length,
                "Algo": a.source_algorithm
            } for a in res.anchors])
            st.dataframe(df_anchors, use_container_width=True)
        else:
            st.write("No anchors found.")

        st.subheader("Gaps")
        if res.gaps:
            df_gaps = pd.DataFrame([{
                "Ref Start": g.reference_start,
                "Ref End": g.reference_end,
                "Ref Length": g.reference_end - g.reference_start,
                "Qry Length": g.query_end - g.query_start,
                "Len Diff": abs((g.reference_end - g.reference_start) - (g.query_end - g.query_start))
            } for g in res.gaps])
            st.dataframe(df_gaps, use_container_width=True)
        else:
            st.write("No gaps extracted (sequences are fully anchored).")
    else:
        st.info("Run an alignment to see anchors and gaps.")

# ----------------- 5. Algorithm Decisions -----------------
with tabs[4]:
    st.header("Explainable Algorithm Decision Inspector")
    if st.session_state.pipeline_result:
        res = st.session_state.pipeline_result
        if not res.gaps:
            st.info("No gaps to inspect.")
        else:
            for i, (gap, align) in enumerate(zip(res.gaps, res.alignments)):
                with st.expander(f"Gap {i+1}: Ref [{gap.reference_start}:{gap.reference_end}] vs Qry [{gap.query_start}:{gap.query_end}]"):
                    md = align.decision_metadata or {}

                    st.markdown("**Gap Features:**")
                    st.write(f"- Length Difference: {abs((gap.reference_end - gap.reference_start) - (gap.query_end - gap.query_start))}")

                    st.markdown("**Decision Trace:**")
                    st.write(f"1. **Initial Strategy**: `{md.get('decision_reason', 'N/A')}`")
                    st.write(f"2. **Selected Band Width**: {align.band_width}")
                    st.write(f"3. **Retries Executed**: {md.get('retry_count', 0)}")
                    st.write(f"4. **Boundary Touched**: {align.boundary_touched}")
                    st.write(f"5. **Full DP Fallback Triggered**: {md.get('fallback_used', False)}")
                    st.write(f"6. **Final Executed Strategy**: `{align.strategy}`")

                    st.markdown("**Alignment Result:**")
                    st.code(f"Ref: {align.aligned_reference}\nQry: {align.aligned_query}")
    else:
        st.info("Run an alignment to inspect decisions.")

# ----------------- 6. Mutation Analysis -----------------
with tabs[5]:
    st.header("Mutation Analysis")
    if st.session_state.pipeline_result:
        res = st.session_state.pipeline_result

        st.subheader("Raw Mutations")
        if res.mutations:
            df_mut = pd.DataFrame([{
                "Type": m.type,
                "Ref Start": m.reference_start,
                "Ref End": m.reference_end,
                "Qry Start": m.query_start,
                "Qry End": m.query_end,
                "Ref Allele": m.reference_allele,
                "Qry Allele": m.query_allele
            } for m in res.mutations])
            st.dataframe(df_mut, use_container_width=True)

            st.download_button("Export Mutations (CSV)", df_mut.to_csv(index=False), "mutations.csv", "text/csv")
        else:
            st.write("No mutations detected.")

        st.subheader("Compound Mutation Events")
        if res.compound_events:
            df_comp = pd.DataFrame([{
                "Event Type": c.event_type,
                "Sub-mutations": len(c.mutations),
                "Ref Range": f"{c.reference_start}-{c.reference_end}",
                "Qry Range": f"{c.query_start}-{c.query_end}"
            } for c in res.compound_events])
            st.dataframe(df_comp, use_container_width=True)
        else:
            st.write("No compound events detected.")

    else:
        st.info("Run an alignment to analyze mutations.")

# ----------------- 7. Baseline Comparison -----------------
with tabs[6]:
    st.header("AlignX vs Full DP Baseline")
    if st.session_state.baseline_result and st.session_state.pipeline_result:
        res = st.session_state.pipeline_result
        b_res = st.session_state.baseline_result

        c1, c2, c3 = st.columns(3)
        c1.metric("AlignX Score", res.final_alignment.score)
        c2.metric("Baseline Score", b_res['score'])
        c3.metric("Correctness", "PASS" if res.final_alignment.score == b_res['score'] else "FAIL")

        c1, c2 = st.columns(2)
        c1.metric("AlignX Runtime (s)", f"{st.session_state.runtimes['pipeline']:.5f}")
        c2.metric("Baseline Runtime (s)", f"{st.session_state.runtimes['baseline']:.5f}")

        st.subheader("Speedup")
        speedup = b_res['runtime'] / max(st.session_state.runtimes['pipeline'], 1e-9)
        st.metric("Speedup Factor", f"{speedup:.2f}x")

    else:
        st.info("Run an alignment with the Baseline checkbox enabled to see comparison.")

# ----------------- 8. Experiment Explorer -----------------
with tabs[7]:
    st.header("Phase 4 & 5 Experiment Explorer")
    csv_files = get_experiment_files()
    plot_files = get_plot_files()

    if not csv_files:
        st.warning("No experiment results found in `experiments/results/`.")
    else:
        selected_csv = st.selectbox("Select Experiment Dataset", csv_files)
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'experiments', 'results', selected_csv))
        st.dataframe(df)

    if plot_files:
        st.subheader("Generated Plots")
        selected_plot = st.selectbox("Select Plot", plot_files)
        st.image(os.path.join(os.path.dirname(__file__), 'experiments', 'plots', selected_plot))

# ----------------- 9. Phase 7 Evaluation -----------------
with tabs[8]:
    st.header("Phase 7 Research Evaluation")
    csv_files = get_experiment_files()
    phase7_files = [f for f in csv_files if f.startswith("phase7_")]

    if not phase7_files:
        st.info("No Phase 7 benchmark results found. Run `python -m experiments.run_phase7` to generate them.")
    else:
        selected_p7 = st.selectbox("Select Phase 7 Benchmark Dataset", phase7_files)
        df_p7 = pd.read_csv(os.path.join(os.path.dirname(__file__), 'experiments', 'results', selected_p7))

        st.subheader("Benchmark Metrics")

        if 'family' in df_p7.columns:
            selected_family = st.multiselect("Filter by Dataset Family", df_p7['family'].unique(), default=df_p7['family'].unique())
            df_filtered = df_p7[df_p7['family'].isin(selected_family)]
        else:
            df_filtered = df_p7

        st.dataframe(df_filtered, use_container_width=True)

        c1, c2, c3 = st.columns(3)
        if 'correctness' in df_filtered.columns:
            exact_matches = sum(df_filtered['correctness'] == 'Exact alignment match')
            equiv_matches = sum(df_filtered['correctness'] == 'Equivalent optimal score')
            c1.metric("Exact Matches", exact_matches)
            c2.metric("Equivalent Optimal", equiv_matches)
            c3.metric("Failures", len(df_filtered) - exact_matches - equiv_matches)

        if 'speedup' in df_filtered.columns:
            st.metric("Average Speedup", f"{df_filtered['speedup'].mean():.2f}x")

# ----------------- 10. About -----------------
with tabs[9]:
    st.header("About AlignX")
    st.markdown("""
    **AlignX** is a modular DNA sequence alignment framework that accelerates Needleman-Wunsch alignment using exact anchoring and adaptive banded dynamic programming.

    - **Phase 1-3:** Implemented exact string matching (KMP/Rabin-Karp) to find homology anchors, dividing the sequence into manageable gaps.
    - **Phase 4:** Established ground-truth evaluation, measuring speedup and correctness.
    - **Phase 5:** Introduced evidence-based adaptive banding and boundary-aware retries to minimize wasted DP matrix cells while preserving exact alignment properties.
    - **Phase 6:** Built this research-grade visualization suite.

    Check the repository's `docs/` folder for deeper architectural and complexity analyses.
    """)
