import streamlit as st
import json

def render():
    st.header("Reproducible Export")
    if not st.session_state.pipeline_result:
        st.info("Run an alignment to export results.")
        return

    res = st.session_state.pipeline_result
    cfg = st.session_state.config

    banded_count = sum(1 for a in res.alignments if a.strategy == "banded_dp")
    full_dp_count = sum(1 for a in res.alignments if a.strategy == "full_dp_fallback" or a.strategy == "full_dp")
    retries = sum(a.decision_metadata.get("retry_count", 0) for a in res.alignments if a.decision_metadata)

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

    st.subheader("Download Artifacts")
    st.download_button("Download Execution Report (JSON)", data=json.dumps(export_data, indent=2), file_name="alignx_report.json", mime="application/json")
    st.download_button("Download Alignment (FASTA)", data=f">Reference\\n{res.final_alignment.aligned_reference}\\n>Query\\n{res.final_alignment.aligned_query}", file_name="alignment.fasta", mime="text/plain")
