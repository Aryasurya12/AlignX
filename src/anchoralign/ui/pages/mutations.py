import streamlit as st
import pandas as pd

def render():
    st.header("Mutation Analysis")
    if not st.session_state.pipeline_result:
        st.info("Run an alignment to analyze mutations.")
        return

    res = st.session_state.pipeline_result

    st.subheader("Raw Mutations")
    if res.mutations:
        df_mut = pd.DataFrame([{
            "Type": m.type,
            "Ref Pos": m.reference_position,
            "Qry Pos": m.query_position,
            "Ref Seq": m.reference_sequence,
            "Qry Seq": m.query_sequence
        } for m in res.mutations])
        st.dataframe(df_mut, use_container_width=True)
    else:
        st.write("No mutations detected.")

    st.subheader("Compound Mutation Events")
    if res.compound_events:
        df_comp = pd.DataFrame([{
            "Event Type": "Compound" if c["mutation_count"] > 1 else "Single",
            "Sub-mutations": c["mutation_count"],
            "Ref Range": f"{c['start_position']}-{c['end_position']}"
        } for c in res.compound_events])
        st.dataframe(df_comp, use_container_width=True)
    else:
        st.write("No compound events detected.")
