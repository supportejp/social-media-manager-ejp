from utils.auth_guard import require_auth
require_auth()
from utils.header import render_header
render_header()

import streamlit as st
from services.api_client import get, post
import os
import uuid

st.title("📝 Posts")

# ============================================
# Control de reinicio de formulario
# ============================================

if "form_counter" not in st.session_state:
    st.session_state.form_counter = 0

form_key = f"create_post_form_{st.session_state.form_counter}"

# ============================================
# Crear Post
# ============================================

st.subheader("Crear nuevo Post")

with st.form(form_key):

    title = st.text_input("Título")
    content = st.text_area("Contenido")
    uploaded_file = st.file_uploader(
        "Subir imagen (opcional)",
        type=["png", "jpg", "jpeg"]
    )
    status = st.selectbox(
        "Estado inicial",
        ["draft", "scheduled", "published"],
        index=0
    )

    submitted = st.form_submit_button("Crear")

if submitted:

    if not title.strip() or not content.strip():
        st.error("Título y contenido son obligatorios.")
    else:

        media_path = None
        media_type = None

        if uploaded_file is not None:
            os.makedirs("uploads/linkedin", exist_ok=True)

            file_extension = uploaded_file.name.split(".")[-1]
            filename = f"{uuid.uuid4()}.{file_extension}"
            save_path = os.path.join("uploads/linkedin", filename)

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            media_path = save_path
            media_type = "image"

        payload = {
            "title": title,
            "content": content,
            "status": status,
            "media_type": media_type,
            "media_path": media_path
        }

        result = post("/posts/", payload)

        if isinstance(result, dict) and result.get("error"):
            st.error(f"Error creando post: {result['error']}")
        else:
            st.success(f"Post creado con ID {result.get('id')}")

            # 🔥 Incrementa contador → fuerza reinicio limpio
            st.session_state.form_counter += 1
            st.rerun()

st.divider()

# ============================================
# Listado de Posts
# ============================================

st.subheader("📚 Posts")

status_filter = st.selectbox(
    "Filtrar por estado",
    ["all", "draft", "scheduled", "published"],
    index=0
)

@st.cache_data(ttl=5)
def load_posts():
    return get("/posts/")

data = load_posts()

if isinstance(data, dict) and data.get("error"):
    st.error(f"Error cargando posts: {data['error']}")
else:
    posts = data if isinstance(data, list) else []

    if status_filter != "all":
        posts = [p for p in posts if p.get("status") == status_filter]

    if not posts:
        st.info("No hay posts para mostrar.")
    else:
        for post_item in posts:

            with st.container():

                col1, col2 = st.columns([9, 1])

                with col1:
                    st.markdown(f"**{post_item.get('title')}**")
                    st.caption(post_item.get("content"))

                    with col2:
                        status = post_item.get("status")

                        if status == "published":
                            st.markdown(
                                "<span style='background-color:#dcfce7; color:#166534; padding:4px 8px; border-radius:12px; font-size:12px;'>Publicado</span>",
                                unsafe_allow_html=True
                            )
                        elif status == "scheduled":
                            st.markdown(
                                "<span style='background-color:#fef3c7; color:#92400e; padding:4px 8px; border-radius:12px; font-size:12px;'>Programado</span>",
                                unsafe_allow_html=True
                            )
                        else:
                            st.markdown(
                                "<span style='background-color:#e2e8f0; color:#334155; padding:4px 8px; border-radius:12px; font-size:12px;'>Borrador</span>",
                                unsafe_allow_html=True
                            )
                if post_item.get("media_path"):
                    st.image(post_item.get("media_path"), width=180)

                if post_item.get("linkedin_post_urn"):
                    linkedin_url = f"https://www.linkedin.com/feed/update/{post_item.get('linkedin_post_urn')}"
                    st.link_button("Ver en LinkedIn", linkedin_url)

                st.divider()