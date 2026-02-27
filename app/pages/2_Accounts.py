from utils.auth_guard import require_auth
require_auth()
from utils.header import render_header
render_header()

import streamlit as st
from services.api_client import get, post

st.title("📣 Accounts")

# --------- Crear Account ----------
st.subheader("Crear nueva Account")

with st.form("create_account_form"):
    name = st.text_input("Nombre (ej: Instagram Marca X)")
    platform = st.selectbox("Plataforma", ["instagram", "facebook", "linkedin", "tiktok", "x"], index=0)
    access_token = st.text_input("Access Token (opcional)", type="password")
    urn = st.text_input("Person URN (LinkedIn ID)")
    is_active = st.checkbox("Activa", value=True)

    submitted = st.form_submit_button("Crear")

    if submitted:
        if not name.strip():
            st.error("El nombre es obligatorio.")
        else:
            payload = {
                "name": name.strip(),
                "platform": platform,
                "access_token": access_token.strip() if access_token.strip() else None,
                "urn": urn,
                "is_active": is_active
            }
            result = post("/accounts/", payload)

            if isinstance(result, dict) and result.get("error"):
                st.error(f"Error creando account: {result['error']}")
            else:
                st.success(f"Account creada con ID {result.get('id')}")
                st.rerun()

st.divider()

# --------- Listar Accounts ----------
st.subheader("Listado de Accounts")

data = get("/accounts/")

if isinstance(data, dict) and data.get("error"):
    st.error(f"Error cargando accounts: {data['error']}")
else:
    accounts = data if isinstance(data, list) else []

    if not accounts:
        st.info("No hay accounts para mostrar.")
    else:
        st.dataframe(accounts, use_container_width=True)