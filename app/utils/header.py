import streamlit as st


def render_header():

    email = st.session_state.get("user_email", "—")
    org = st.session_state.get("organization_name", "—")

    st.markdown("""
        <style>
        .ejp-header {
            background: linear-gradient(90deg, #0f172a, #1e293b);
            padding: 18px 25px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
        }

        .ejp-left {
            color: white;
            font-weight: 600;
            font-size: 18px;
        }

        .ejp-right {
            display: flex;
            align-items: center;
            gap: 15px;
            color: #d1d5db;
            font-size: 14px;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([0.85, 0.15])

    with col1:
        st.markdown(f"""
            <div class="ejp-header">
                <div class="ejp-left">
                    🚀 EJP Social Manager
                </div>
                <div class="ejp-right">
                    👤 {email} | 🏢 {org}
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button("⚙️"):
            st.info("Configuración próximamente")

        if st.button("Cerrar"):
            st.session_state.clear()
            st.switch_page("pages/0_Login.py")