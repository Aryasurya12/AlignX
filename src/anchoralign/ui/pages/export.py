import streamlit as st
import json


def render():
    st.header("Reproducible Export")
    if not st.session_state.pipeline_result:
        st.info("Run an alignment in **Sequence Alignment** to export results.")
        return

    res = st.session_state.pipeline_result
    cfg = st.session_state.config

    banded_count = sum(1 for a in res.alignments if a.strategy == "banded_dp")
    full_dp_count = sum(1 for a in res.alignments if a.strategy in ("full_dp_fallback", "full_dp"))
    retries = sum(a.decision_metadata.get("retry_count", 0) for a in res.alignments if a.decision_metadata)
    total_cells = sum(getattr(a, "cells_evaluated", 0) for a in res.alignments)

    export_data = {
        "config": cfg.__dict__ if cfg else {},
        "metrics": {
            "reference_length": res.reference_length,
            "query_length": res.query_length,
            "score": res.final_alignment.score if res.final_alignment else 0.0,
            "anchors": len(res.anchors),
            "gaps": len(res.gaps),
            "mutations": len(res.mutations),
            "banded_count": banded_count,
            "full_dp_count": full_dp_count,
            "retries": retries,
            "dp_cells_evaluated": total_cells,
            "runtime_seconds": st.session_state.runtimes.get('pipeline', 0.0),
            "timings_breakdown_seconds": res.timings,
            "memory": {
                "peak_kb": getattr(res, "memory_peak_kb", 0.0),
                "current_kb": getattr(res, "memory_current_kb", 0.0),
            }
        }
    }

    st.subheader("Download Artifacts")
    st.download_button(
        "Download Execution Report (JSON)",
        data=json.dumps(export_data, indent=2),
        file_name="alignx_report.json",
        mime="application/json"
    )

    if res.final_alignment:
        fasta_content = f">Reference (len={res.reference_length})\n{res.final_alignment.aligned_reference}\n>Query (len={res.query_length})\n{res.final_alignment.aligned_query}"
        st.download_button(
            "Download Alignment (FASTA)",
            data=fasta_content,
            file_name="alignment.fasta",
            mime="text/plain"
        )
