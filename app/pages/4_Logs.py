from utils.auth_guard import require_auth
require_auth()
from utils.header import render_header
render_header()

import streamlit as st
from services.api_client import get

st.title("🧾 Logs")

data = get("/logs/")

if isinstance(data, dict) and data.get("error"):
    st.error(f"Error cargando logs: {data['error']}")
    st.stop()

logs = data if isinstance(data, list) else []

# Filtros
col1, col2 = st.columns(2)
with col1:
    level_filter = st.selectbox("Nivel", ["all", "info", "error"], index=0)
with col2:
    event_filter = st.text_input("Filtrar por event (contiene)", value="")

filtered = logs

if level_filter != "all":
    filtered = [l for l in filtered if (l.get("level") or "").lower() == level_filter]

if event_filter.strip():
    q = event_filter.strip().lower()
    filtered = [l for l in filtered if q in (l.get("event") or "").lower()]

st.caption(f"Mostrando {len(filtered)} de {len(logs)} logs")

if not filtered:
    st.info("No hay logs para mostrar con los filtros actuales.")
else:
    st.dataframe(filtered, use_container_width=True)