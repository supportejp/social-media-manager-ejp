import requests
import streamlit as st
from config import API_BASE_URL


def _get_headers():
    """
    Construye headers automáticamente si existe token.
    """
    headers = {"Content-Type": "application/json"}

    token = st.session_state.get("token")

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return headers


def get(endpoint: str):
    try:
        response = requests.get(
            f"{API_BASE_URL}{endpoint}",
            headers=_get_headers()
        )

        if response.status_code == 401:
            return {"error": "unauthorized"}

        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        return {"error": str(e)}


def post(endpoint: str, data: dict):
    try:
        response = requests.post(
            f"{API_BASE_URL}{endpoint}",
            json=data,
            headers=_get_headers()
        )

        if response.status_code == 401:
            return {"error": "unauthorized"}

        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        return {"error": str(e)}