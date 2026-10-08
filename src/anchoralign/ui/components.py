import streamlit as st
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

def render_card(title, description, icon=""):
    st.markdown(f"""
    <div class="alignx-card">
        <h4 style="margin-top: 0; display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 1.5rem;">{icon}</span> {title}
        </h4>
        <p style="color: var(--text-secondary); margin-bottom: 0;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def initialize_session():
    if 'pipeline_result' not in st.session_state:
        st.session_state.pipeline_result = None
    if 'baseline_result' not in st.session_state:
        st.session_state.baseline_result = None
    if 'config' not in st.session_state:
        st.session_state.config = None
    if 'runtimes' not in st.session_state:
        st.session_state.runtimes = {}
        
def validate_dna(seq):
    seq = seq.upper().replace(" ", "").replace("\\n", "")
    valid_chars = set("ACGTN")
    if not set(seq).issubset(valid_chars):
        return None, "Sequence contains invalid characters. Only A, C, G, T, N are supported."
    return seq, None

def get_experiment_files():
    results_dir = PROJECT_ROOT / 'experiments' / 'results'
    if not os.path.exists(results_dir):
        return []
    return [f for f in os.listdir(results_dir) if f.endswith('.csv')]

def get_plot_files():
    plots_dir = PROJECT_ROOT / 'experiments' / 'plots'
    if not os.path.exists(plots_dir):
        return []
    return [f for f in os.listdir(plots_dir) if f.endswith('.png')]
