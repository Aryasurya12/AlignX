import streamlit as st
import time
from anchoralign.pipeline.orchestrator import run_pipeline
from anchoralign.config import AnchorAlignConfig
from anchoralign.evaluation.baseline import full_sequence_align
from anchoralign.ui.components import validate_dna

def render():
    st.header("Sequence Alignment Workspace")
    
    st.markdown("### Presets")
    preset = st.selectbox("Load an example dataset", ["None", "Identical Sequences", "Substitution", "Insertion", "Long Indel", "Complex"])
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
        elif preset == "Long Indel":
            st.session_state.ref_in = "A" * 100 + "G" * 50
            st.session_state.query_in = "A" * 10 + "T" * 80 + "A" * 90 + "G" * 50
        elif preset == "Complex":
            st.session_state.ref_in = "ACGT" * 20 + "TGCA" * 20
            st.session_state.query_in = "ACGT" * 5 + "AAAAA" + "ACGT" * 5 + "G" + "ACGT" * 9 + "TGCA" * 20
        st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Reference Sequence")
        ref_input = st.text_area("Input Reference DNA (FASTA or Plain Text)", height=150, key="ref_in")
    with col2:
        st.subheader("Query Sequence")
        query_input = st.text_area("Input Query DNA (FASTA or Plain Text)", height=150, key="query_in")

    with st.expander("Alignment Configuration", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            l_min = st.number_input("Minimum Anchor Length", min_value=3, value=10)
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

    run_baseline = st.checkbox("Run Full DP Baseline for Comparison (Warning: O(N*M))", value=False)

    if st.button("Run Alignment", type="primary"):
        if not ref_input or not query_input:
            st.error("Please provide both sequences.")
        else:
            ref_lines = [l for l in ref_input.split('\\n') if not l.startswith('>')]
            query_lines = [l for l in query_input.split('\\n') if not l.startswith('>')]
            ref_clean, err1 = validate_dna("".join(ref_lines))
            query_clean, err2 = validate_dna("".join(query_lines))

            if err1 or err2:
                st.error(err1 or err2)
            elif len(ref_clean) > 10000 or len(query_clean) > 10000:
                st.warning("Sequences exceed 10,000 bases. This interface limits sequence size.")
            else:
                cfg = AnchorAlignConfig(
                    L_min=l_min, anchor_algorithm=algo, anchor_merge_threshold=merge_thresh,
                    match_score=match_score, mismatch_penalty=mismatch_pen, gap_penalty=gap_pen,
                    adaptive_band_enabled=adaptive_enabled, band_width=band_width,
                    band_safety_margin=band_margin, max_band_retries=max_retries,
                    band_growth_factor=growth_factor, clustering_k=clustering_k
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
                            b_start = time.perf_counter()
                            b_ref, b_query, b_score, b_runtime, b_muts = full_sequence_align(ref_clean, query_clean, cfg)
                            b_end = time.perf_counter()
                            st.session_state.baseline_result = {
                                'aligned_reference': b_ref, 'aligned_query': b_query,
                                'score': b_score, 'runtime': b_runtime, 'mutations': len(b_muts)
                            }
                            st.session_state.runtimes['baseline'] = b_end - b_start
                        else:
                            st.session_state.baseline_result = None

                        st.success("Pipeline Execution Complete!")
                    except Exception as e:
                        st.error(f"Execution Error: {e}")
