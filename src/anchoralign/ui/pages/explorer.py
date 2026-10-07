import streamlit as st
import pandas as pd

def render():
    st.header("Alignment Explorer")
    if not st.session_state.pipeline_result:
        st.info("Run an alignment to visualize results.")
        return

    res = st.session_state.pipeline_result
    
    tab1, tab2, tab3 = st.tabs(["Alignment Viewer", "Anchors", "Gaps"])
    
    with tab1:
        st.subheader("Final Alignment")
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
        c3.metric("Insertions", insertions)
        c4.metric("Deletions", deletions)
        st.metric("Sequence Identity", f"{identity:.2f}%")

        st.subheader("Sequence Viewer")
        chunk_size = 100
        for i in range(0, len(ref_aln), chunk_size):
            end = min(i + chunk_size, len(ref_aln))
            r_chunk = ref_aln[i:end]
            q_chunk = query_aln[i:end]
            match_str = "".join('|' if r == q and r != '-' else ' ' for r, q in zip(r_chunk, q_chunk))
            st.code(f"Ref  [{i:04d}]: {r_chunk}\\n          {' '*len(str(i))}{match_str}\\nQry  [{i:04d}]: {q_chunk}", language="text")

    with tab2:
        st.subheader("Anchors")
        if res.anchors:
            df_anchors = pd.DataFrame([{
                "Ref Start": a.reference_start, "Ref End": a.reference_end,
                "Qry Start": a.query_start, "Qry End": a.query_end,
                "Length": a.length, "Algo": a.source_algorithm
            } for a in res.anchors])
            st.dataframe(df_anchors, use_container_width=True)
        else:
            st.write("No anchors found.")

    with tab3:
        st.subheader("Gaps")
        if res.gaps:
            df_gaps = pd.DataFrame([{
                "Ref Start": g.reference_start, "Ref End": g.reference_end,
                "Ref Length": g.reference_end - g.reference_start,
                "Qry Length": g.query_end - g.query_start,
                "Len Diff": abs((g.reference_end - g.reference_start) - (g.query_end - g.query_start))
            } for g in res.gaps])
            st.dataframe(df_gaps, use_container_width=True)
        else:
            st.write("No gaps extracted (sequences are fully anchored).")
