import requests
import streamlit as st
import os
import time

# ============================================
# Configuración base
# ============================================

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


# ============================================
# Headers helper
# ============================================

def _get_headers():
    headers = {
        "Content-Type": "application/json"
    }

    token = st.session_state.get("token")

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return headers


# ============================================
# GET
# ============================================

def get(endpoint: str):
    start = time.time()

    try:
        response = requests.get(
            f"{API_BASE_URL}{endpoint}",
            headers=_get_headers(),
            timeout=30
        )

        duration = round(time.time() - start, 2)
        print(f"[GET] {endpoint} took {duration} seconds")

        if response.status_code == 401:
            return {"error": "unauthorized"}

        response.raise_for_status()

        return response.json()

    except requests.RequestException as e:
        duration = round(time.time() - start, 2)
        print(f"[GET ERROR] {endpoint} failed after {duration} seconds")
        return {"error": str(e)}


# ============================================
# POST
# ============================================

def post(endpoint: str, data: dict):
    start = time.time()

    try:
        response = requests.post(
            f"{API_BASE_URL}{endpoint}",
            json=data,
            headers=_get_headers(),
            timeout=30
        )

        duration = round(time.time() - start, 2)
        print(f"[POST] {endpoint} took {duration} seconds")

        if response.status_code == 401:
            return {"error": "unauthorized"}

        response.raise_for_status()

        return response.json()

    except requests.RequestException as e:
        duration = round(time.time() - start, 2)
        print(f"[POST ERROR] {endpoint} failed after {duration} seconds")
        return {"error": str(e)}