import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    /* AlignX Research Studio Dark Theme */
    
    :root {
        --primary-bg: #0B1020;
        --secondary-bg: #111827;
        --card-bg: #172033;
        --border-color: #293449;
        --primary-accent: #8B5CF6;
        --secondary-accent: #22D3EE;
        --success: #34D399;
        --warning: #FBBF24;
        --error: #FB7185;
        --text-primary: #F1F5F9;
        --text-secondary: #94A3B8;
    }

    /* Overall background */
    .stApp {
        background-color: var(--primary-bg);
        color: var(--text-primary);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--secondary-bg) !important;
        border-right: 1px solid var(--border-color);
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Code blocks and sequence text */
    code {
        font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
        background-color: var(--secondary-bg) !important;
        color: var(--text-primary) !important;
        padding: 0.2em 0.4em;
        border-radius: 4px;
        border: 1px solid var(--border-color);
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background-color: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px;
    }
    
    /* Metric blocks */
    [data-testid="stMetricValue"] {
        color: var(--secondary-accent) !important;
    }
    
    /* Custom brand header */
    .alignx-brand {
        background: linear-gradient(90deg, var(--primary-accent) 0%, var(--secondary-accent) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .alignx-subtitle {
        color: var(--text-secondary);
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Custom Card Style */
    .alignx-card {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    </style>
    """, unsafe_allow_html=True)

def render_header():
    st.markdown("""
        <div class="alignx-brand">🧬 AlignX</div>
        <div class="alignx-subtitle">Adaptive Anchor-Guided DNA Sequence Alignment<br/>
        <span style="font-size: 0.9em; opacity: 0.8;">Research & Analysis Workspace</span></div>
    """, unsafe_allow_html=True)
