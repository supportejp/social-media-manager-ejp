import streamlit as st
from services.api_client import post, get

st.set_page_config(
    page_title="Login - EJP Social Manager",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 🔐 Si ya está autenticado → ir al home
if "token" in st.session_state and st.session_state["token"]:
    st.switch_page("app.py")

# 🔒 Ocultar sidebar y header default
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        header {visibility: hidden;}
        .login-container {
            max-width: 420px;
            margin: auto;
            margin-top: 120px;
            padding: 40px;
            border-radius: 12px;
            background-color: white;
            box-shadow: 0 8px 25px rgba(0,0,0,0.06);
        }
        .login-title {
            text-align: center;
            font-size: 26px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        .login-subtitle {
            text-align: center;
            color: #6b7280;
            margin-bottom: 30px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="login-container">', unsafe_allow_html=True)

st.markdown('<div class="login-title">🚀 EJP Social Manager</div>', unsafe_allow_html=True)
st.markdown('<div class="login-subtitle">Inicia sesión para continuar</div>', unsafe_allow_html=True)

with st.form("login_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Ingresar")

    if submit:
        if not email or not password:
            st.error("Completa email y password.")
        else:
            # 🔹 Login
            response = post("/auth/login", {
                "email": email,
                "password": password
            })

            if response.get("error"):
                st.error("Credenciales inválidas.")
            else:
                # Guardar token
                st.session_state["token"] = response["access_token"]

                # 🔹 Obtener datos del usuario autenticado
                me = get("/auth/me")
              

                if me.get("error"):
                    st.error("Error obteniendo datos del usuario.")
                else:
                    st.session_state["user_email"] = me.get("email")
                    st.session_state["role"] = me.get("role")
                    st.session_state["organization_id"] = me.get("organization_id")
                    st.session_state["organization_name"] = me.get("organization_name")

                    st.switch_page("app.py")

st.markdown('</div>', unsafe_allow_html=True)