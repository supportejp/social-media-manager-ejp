import time as pytime
start = pytime.time()
import streamlit as st
from utils.header import render_header
render_header()

st.set_page_config(layout="wide")

# 🔐 Si no hay token → forzar login
if "token" not in st.session_state or not st.session_state["token"]:
    st.session_state["redirect_to_login"] = True
    st.switch_page("pages/0_Login.py")

# ----- HEADER GLOBAL -----
st.markdown(
    f"""
    <div style="
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 60px;
        background-color: #0f172a;
        color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 30px;
        z-index: 999;
    ">
        <div style="font-size:18px;font-weight:600;">
            🚀 EJP Social Manager
        </div>
        <div style="font-size:14px;">
            Sesión activa
            <button onclick="window.location.reload()">Cerrar sesión</button>
        </div>
    </div>
    <div style="height:70px;"></div>
    """,
    unsafe_allow_html=True
)

st.write("Render:", round(pytime.time() - start, 2), "seconds")