from utils.auth_guard import require_auth
require_auth()
from utils.header import render_header
render_header()

import streamlit as st
from datetime import datetime, date, time
from services.api_client import get, post
from datetime import timezone
from zoneinfo import ZoneInfo

st.title("📅 Agenda (Calendar)")

# -------------------------
# Helpers
# -------------------------
TZ_CHILE = ZoneInfo("America/Santiago")

def parse_dt(value: str):
    try:
        dt = datetime.fromisoformat(value.replace("Z", "").replace(" ", "T"))
        # Lo que viene del API lo tratamos como UTC naive
        dt_utc = dt.replace(tzinfo=timezone.utc)
        return dt_utc.astimezone(TZ_CHILE)
    except Exception:
        return None

def badge(text: str):
    """Simple badge-like label."""
    st.markdown(
        f"<span style='padding:4px 10px;border-radius:999px;background:#1f2937;color:#fff;font-size:12px;'>{text}</span>",
        unsafe_allow_html=True
    )

def status_badge(status: str):
    status = (status or "").lower()
    if status == "draft":
        badge("📝 draft")
    elif status == "scheduled":
        badge("⏳ scheduled")
    elif status == "published":
        badge("✅ published")
    else:
        badge(f"ℹ️ {status}")

def schedule_badge(status: str):
    status = (status or "").lower()
    if status == "pending":
        badge("🕒 pending")
    elif status == "executed":
        badge("✅ executed")
    elif status == "failed":
        badge("❌ failed")
    else:
        badge(f"ℹ️ {status}")

# -------------------------
# Cargar datos base
# -------------------------
posts = get("/posts/")
accounts = get("/accounts/")
calendar_items = get("/calendar/")
schedules = get("/schedules/")

# Manejo errores API
if isinstance(posts, dict) and posts.get("error"):
    st.error(f"Error cargando posts: {posts['error']}")
    st.stop()
if isinstance(accounts, dict) and accounts.get("error"):
    st.error(f"Error cargando accounts: {accounts['error']}")
    st.stop()
if isinstance(calendar_items, dict) and calendar_items.get("error"):
    st.error(f"Error cargando calendar: {calendar_items['error']}")
    st.stop()
if isinstance(schedules, dict) and schedules.get("error"):
    st.error(f"Error cargando schedules: {schedules['error']}")
    st.stop()

posts = posts if isinstance(posts, list) else []
accounts = accounts if isinstance(accounts, list) else []
calendar_items = calendar_items if isinstance(calendar_items, list) else []
schedules = schedules if isinstance(schedules, list) else []

# Mapas útiles
posts_by_id = {p["id"]: p for p in posts if "id" in p}
accounts_by_id = {a["id"]: a for a in accounts if "id" in a}
schedule_by_calendar_id = {}
for sch in schedules:
    cid = sch.get("calendar_item_id")
    if cid is not None:
        schedule_by_calendar_id[cid] = sch

# -------------------------
# Crear Calendar Item (Agenda)
# -------------------------
st.subheader("Agendar publicación")

if not posts:
    st.warning("No hay posts. Crea uno primero en la página Posts.")
elif not accounts:
    st.warning("No hay accounts. Crea una primero en la página Accounts.")
else:
    # Filtro de posts sugerido: prioriza draft
    draft_posts = [p for p in posts if p.get("status") == "draft"]
    post_options = draft_posts if draft_posts else posts

    post_label_map = {
        p["id"]: f"#{p['id']} • {p.get('title','(sin título)')} • ({p.get('status','')})"
        for p in post_options
    }
    account_label_map = {
        a["id"]: f"#{a['id']} • {a.get('name','')} • {a.get('platform','')}"
        for a in accounts
    }

    with st.form("calendar_create_form"):
        col1, col2 = st.columns(2)
        with col1:
            selected_post_id = st.selectbox(
                "Post",
                options=list(post_label_map.keys()),
                format_func=lambda pid: post_label_map.get(pid, str(pid)),
            )
        with col2:
            selected_account_id = st.selectbox(
                "Account",
                options=list(account_label_map.keys()),
                format_func=lambda aid: account_label_map.get(aid, str(aid)),
            )

        col3, col4 = st.columns(2)
        with col3:
            d = st.date_input("Fecha", value=date.today())
        with col4:
            t = st.time_input("Hora", value=time(10, 0))

        submitted = st.form_submit_button("Agendar")

        if submitted:
            scheduled_at = datetime.combine(d, t).strftime("%Y-%m-%dT%H:%M:%S")
            payload = {
                "post_id": int(selected_post_id),
                "account_id": int(selected_account_id),
                "scheduled_at": scheduled_at
            }
            result = post("/calendar/", payload)

            if isinstance(result, dict) and result.get("error"):
                st.error(f"Error agendando: {result['error']}")
            else:
                st.success("Agendado ✅ (Post pasa a scheduled y Schedule queda pending)")
                st.rerun()

st.divider()

# -------------------------
# Vista Agenda Moderna
# -------------------------
st.subheader("Agenda")

# Filtros UX
colf1, colf2, colf3 = st.columns([0.34, 0.33, 0.33])
with colf1:
    filtro_platform = st.selectbox(
        "Filtrar por plataforma",
        options=["all"] + sorted(list({a.get("platform") for a in accounts if a.get("platform")})),
        index=0
    )
with colf2:
    filtro_account = st.selectbox(
        "Filtrar por account",
        options=["all"] + [f"{a['id']} • {a.get('name','')}" for a in accounts],
        index=0
    )
with colf3:
    filtro_schedule_status = st.selectbox(
        "Filtrar por schedule",
        options=["all", "pending", "executed", "failed"],
        index=0
    )

# Enriquecer y ordenar items
items_enriched = []
for ci in calendar_items:
    ci_dt = parse_dt(ci.get("scheduled_at", ""))
    if not ci_dt:
        continue

    post_obj = posts_by_id.get(ci.get("post_id"), {})
    acc_obj = accounts_by_id.get(ci.get("account_id"), {})
    sch_obj = schedule_by_calendar_id.get(ci.get("id"), None)

    # aplicar filtros
    if filtro_platform != "all" and acc_obj.get("platform") != filtro_platform:
        continue
    if filtro_account != "all":
        # filtro_account = "1 • Instagram Marca X"
        try:
            wanted_id = int(filtro_account.split("•")[0].strip())
            if acc_obj.get("id") != wanted_id:
                continue
        except Exception:
            pass
    if filtro_schedule_status != "all":
        sch_status = (sch_obj.get("status") if sch_obj else "").lower()
        if sch_status != filtro_schedule_status:
            continue

    items_enriched.append({
        "calendar": ci,
        "dt": ci_dt,
        "post": post_obj,
        "account": acc_obj,
        "schedule": sch_obj
    })

items_enriched.sort(key=lambda x: x["dt"])

if not items_enriched:
    st.info("No hay items en agenda con los filtros actuales.")
else:
    # Agrupar por día
    current_day = None

    for item in items_enriched:
        ci = item["calendar"]
        dtv = item["dt"]
        post_obj = item["post"]
        acc_obj = item["account"]
        sch_obj = item["schedule"]

        day_label = dtv.strftime("%A %d-%m-%Y")
        hour_label = dtv.strftime("%H:%M")

        if day_label != current_day:
            st.markdown(f"### {day_label}")
            current_day = day_label

        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([0.13, 0.42, 0.25, 0.20])

            with c1:
                st.markdown(f"**{hour_label}**")

            with c2:
                st.markdown(f"**{post_obj.get('title','(sin título)')}**")
                st.caption(f"Post #{post_obj.get('id')} • CalendarItem #{ci.get('id')}")

            with c3:
                st.markdown(f"**{acc_obj.get('name','(sin account)')}**")
                st.caption(f"{acc_obj.get('platform','')} • Account #{acc_obj.get('id')}")
                status_badge(post_obj.get("status", ""))

            with c4:
                if sch_obj:
                    schedule_badge(sch_obj.get("status", ""))
                    st.caption(f"Schedule #{sch_obj.get('id')}")
                    # Ejecutar si pending
                    if (sch_obj.get("status") or "").lower() == "pending":
                        if st.button("▶ Ejecutar", key=f"exec_{sch_obj.get('id')}"):
                            exec_result = post(f"/schedules/{sch_obj.get('id')}/execute", {})
                            if isinstance(exec_result, dict) and exec_result.get("error"):
                                st.error(f"Error ejecutando: {exec_result['error']}")
                            else:
                                st.success("Ejecutado ✅ (Post pasa a published + Log info)")
                                st.rerun()
                else:
                    badge("⚠️ sin schedule")
                    st.caption("Revisa creación automática")