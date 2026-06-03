# frontend/app.py
# Import libraries
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Configure streamlit
st.set_page_config(page_title="Expen Pal ⚡🔥🚀", page_icon="🔮", layout="wide")
API_URL = "http://127.0.0.1:8000"

# --- OFFLINE MODERN GLASSMORPHIC ENGINE (Local CSS Injector) ---
st.markdown("""
<style>
    @import url('https://googleapis.com');
    
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .futuristic-title { font-family: 'Orbitron', sans-serif; color: #00f2fe; text-shadow: 0 0 15px rgba(0,242,254,0.6); text-align:center; }
    
    /* Dynamic Client-Side Animations */
    @keyframes corePulse { 0% { opacity: 0.85; transform: scale(1); } 50% { opacity: 1; transform: scale(1.01); } 100% { opacity: 0.85; transform: scale(1); } }
    @keyframes viewFade { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
    
    .stApp { animation: viewFade 0.8s ease-in-out; background-color: #060713; }
    
    /* Local Glassmorphism Styling Definitions */
    div[data-testid="stForm"], .glass-card {
        background: rgba(15, 23, 42, 0.4) !important;
        backdrop-filter: blur(16px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(16px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 25px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    }
    
    /* Futuristic Cyber Metric Nodes */
    .cyber-node {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(0, 242, 254, 0.15);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: all 0.4s ease;
    }
    .cyber-node:hover {
        border-color: #00f2fe;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.25);
        transform: translateY(-2px);
    }
    .cyber-node h6 { margin: 0; color: #a4b0be; text-transform: uppercase; font-size: 11px; letter-spacing: 2px; }
    .cyber-node h2 { margin: 8px 0 0 0; color: #00f2fe; font-family: 'Orbitron', sans-serif; font-size: 26px; }

    /* Offline Text Terminal */
    .ai-terminal {
        background: #020208;
        border-left: 3px solid #00f2fe;
        font-family: monospace;
        padding: 15px;
        color: #00ff88;
        border-radius: 4px;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None

def run_login(u, p):
    try:
        r = requests.post(f"{API_URL}/token", data={"username": u, "password": p})
        if r.status_code == 200:
            st.session_state.token = r.json()["access_token"]
            st.session_state.username = u
            st.rerun()
        else:
            st.error("🔑 SECURITY COMPROMISED: ACCESS DENIED.")
    except Exception:
        st.error("❌ CORE OFFLINE: START THE BACKEND SERVER.")

def run_register(u, p):
    try:
        r = requests.post(f"{API_URL}/auth/register", json={"username": u, "password": p})
        if r.status_code == 201:
            st.success("🛰️ CREDENTIAL MATRIX INITIALIZED. SWITCH TO SIGN IN.")
    except Exception:
        st.error("❌ BACKEND PIPELINE NETWORK ERROR.")

# ==========================================
#   INTERFACE ROUTER LAYER
# ==========================================
if not st.session_state.token:
    st.markdown("<br><br><h1 class='futuristic-title'>🔮 Expen Pal</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #70a1ff;'>Secure, Completely Offline Ledger Core Architecture</p>", unsafe_allow_html=True)
    
    _, center_col, _ = st.columns([1, 1.2, 1])
    with center_col:
        with st.container():
            t_auth, t_reg = st.tabs(["🔒 CONNECT NODE", "🛰️ PROVISION ACCESS"])
            with t_auth:
                u_in = st.text_input("Username:", key="u1")
                p_in = st.text_input("Password:", type="password", key="p1")
                if st.button("Login 🔑→", width='stretch'):
                    run_login(u_in, p_in)
            with t_reg:
                u_up = st.text_input("Username: ", key="u2")
                p_up = st.text_input("Password: ", type="password", key="p2")
                if st.button("Sign Up →", width='stretch'):
                    run_register(u_up, p_up)
else:
    # PLATFORM DASHBOARD ACTIVE
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    top_l, top_r = st.columns([4, 1])
    with top_l:
        st.markdown(f"<h2 style='color:#ffffff; margin:0;'>Operator: <span style='color:#00f2fe;'>{st.session_state.username}</span> 📡</h2>", unsafe_allow_html=True)
    with top_r:
        if st.button("Logout", width='stretch'):
            st.session_state.token, st.session_state.username = None, None
            st.rerun()
            
    st.markdown("<hr style='border:1px solid rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
    
    try:
        analytics = requests.get(f"{API_URL}/expenses/analytics", headers=headers).json()
        expenses_raw = requests.get(f"{API_URL}/expenses", headers=headers).json()
    except Exception:
        st.error("🚨 CRITICAL PIPELINE BREAKDOWN: DATA STREAM DISCONNECTED.")
        st.stop()

    # Dynamic KPI Readouts
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"<div class='cyber-node'><h6>Aggregate Drainage</h6><h2>${analytics.get('total', 0):,}</h2></div>", unsafe_allow_html=True)
    with k2:
        st.markdown(f"<div class='cyber-node'><h6>Core Strain Index</h6><h2>{analytics.get('highest_category', 'None')}</h2></div>", unsafe_allow_html=True)
    with k3:
        st.markdown(f"<div class='cyber-node'><h6>Database Records</h6><h2>{len(expenses_raw)} Indices</h2></div>", unsafe_allow_html=True)
    with k4:
        st.markdown(f"<div class='cyber-node'><h6>System State</h6><h2>ONLINE</h2></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Main Interface Segments
    panel_left, panel_right = st.columns([1, 1.4])
    
    with panel_left:
        st.markdown("### 📥 Stream Transaction")
        with st.form("new_transaction"):
            title = st.text_input("Resource Tag / Identifier")
            amount = st.number_input("Outflow Quantum ($)", min_value=0.01, step=0.01)
            cat = st.selectbox("Classification Vector", ["Infrastructure", "Data Feeds", "Power Core", "Logistics", "Operations", "Leisure"])
            notes = st.text_area("System Metadata Logs")
            
            if st.form_submit_button("Commit Transaction to Ledger Matrix", width='stretch'):
                if title and amount > 0:
                    payload = {"title": title, "amount": amount, "category": cat, "description": notes}
                    res = requests.post(f"{API_URL}/expenses", json=payload, headers=headers)
                    if res.status_code == 200:
                        st.toast("⚡ Transaction committed seamlessly.", icon="🛰️")
                        st.rerun()

    with panel_right:
        st.markdown("### 📊 Interactive Visual Data Matrix")
        
        if expenses_raw:
            tab_line, tab_pie, tab_bar, tab_ai = st.tabs(["📈 Timeline Engine", "🍩 Distribution Donut", "📊 Vector Volume", "🧠 Algorithmic Explainer"])
            
            with tab_line:
                # Dynamic Timeframe Switcher
                sub_tf = st.radio("Isolate Temporal Resolution Mapping:", ["minute", "hour", "day", "month", "year"], horizontal=True, index=2)
                tf_data = analytics["timeframes"].get(sub_tf, [])
                
                if tf_data:
                    df_line = pd.DataFrame(tf_data)
                    fig_l = px.line(df_line, x="date", y="amount", markers=True, template="plotly_dark")
                    fig_l.update_traces(line_color='#00f2fe', marker=dict(size=6, color='#00ff88'))
                    fig_l.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=280, margin=dict(t=10,b=10,l=10,r=10))
                    st.plotly_chart(fig_l, width='stretch')
                else:
                    st.caption("Insufficient historical data blocks for timeline parsing.")
                    
            with tab_pie:
                df_p = pd.DataFrame(list(analytics["breakdown"].items()), columns=["Vector", "Drain"])
                fig_p = px.pie(df_p, values="Drain", names="Vector", hole=0.5, template="plotly_dark", color_discrete_sequence=px.colors.sequential.Agsunset)
                fig_p.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=280, margin=dict(t=10,b=10,l=10,r=10))
                st.plotly_chart(fig_p, width='stretch')
                
            with tab_bar:
                df_b = pd.DataFrame(list(analytics["breakdown"].items()), columns=["Vector", "Drain"])
                fig_b = px.bar(df_b, x="Vector", y="Drain", template="plotly_dark", color="Vector", color_discrete_sequence=px.colors.sequential.Viridis)
                fig_b.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=280, showlegend=False, margin=dict(t=10,b=10,l=10,r=10))
                st.plotly_chart(fig_b, width='stretch')
                
            with tab_ai:
                st.markdown("<div class='ai-terminal'>", unsafe_allow_html=True)
                st.text(analytics.get("explanation", ""))
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Awaiting structural transactions to initialize visual matrix charts.")
