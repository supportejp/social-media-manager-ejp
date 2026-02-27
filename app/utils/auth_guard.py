import streamlit as st


def require_auth():
    token = st.session_state.get("token")

    if not token:
        st.warning("Debes iniciar sesión.")
        st.switch_page("pages/0_Login.py")