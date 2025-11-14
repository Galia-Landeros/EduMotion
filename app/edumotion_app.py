# app/edumotion_app.py (solo parte del tab de control)

import streamlit as st
import os, json
import pandas as pd
import cv2 as cv
import streamlit.components.v1 as components 
from pathlib import Path
from launchers import start_camera_slides, launch_ppt_via_com, launch_ppt_fallback
from logger import LOG_PATH

# Config de la página
st.set_page_config(
    page_title="EduMotion - Presentaciones didácticas",
    page_icon="🧩",
    layout="wide",
)

# === Cargar CSS de la nueva homepage ===
css_path = Path(__file__).parent.parent / "assets" / "edumotion_home.css"
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# 1) CSS para TODO lo que pinta Streamlit (barra de navegación, cards, etc.)
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


# ===== SESSION NAVIGATION =====
if "page" not in st.session_state:
    st.session_state.page = "inicio"

if "proc" not in st.session_state:
    st.session_state.proc = None

def nav_button(label: str, page_name: str, key: str):
    active_class = "edm-nav-btn-wrapper-active" if st.session_state.page == page_name else "edm-nav-btn-wrapper"
    st.markdown(f'<div class="{active_class}">', unsafe_allow_html=True)
    if st.button(label, key=key):
        st.session_state.page = page_name
    st.markdown("</div>", unsafe_allow_html=True)

def render_control_view():
    # ===== TÍTULO DE SECCIÓN =====
    st.markdown(
        """
        <section class="edm-section">
          <h2 class="edm-section-title">Control gestual de presentaciones</h2>
          <p class="edm-section-subtitle">
            Configura la cámara, selecciona una presentación y controla las diapositivas 
            mediante gestos sin contacto.
          </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    section = st.container()
    with section:
        col_left, col_right = st.columns([1.2, 1])

        # ========= COL LEFT: VISTA PREVIA DE CÁMARA =========
        with col_left:
            st.markdown(
                """
                <div class="edm-card">
                  <div class="edm-card-header">
                    <div class="edm-card-title">Vista previa de cámara</div>
                  </div>
                """,
                unsafe_allow_html=True,
            )

            user_name = st.text_input(
                "Nombre del alumno (opcional)",
                placeholder="Ej. Camila",
            )

            if st.button("🔄 Actualizar vista previa"):
                cap = cv.VideoCapture(0)
                ok, frame = cap.read()
                cap.release()
                if ok:
                    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                    st.image(frame, caption="Cámara detectada", use_column_width=True)
                else:
                    st.error("No se pudo leer la cámara. Verifica que no esté en uso.")

            st.markdown("</div>", unsafe_allow_html=True)

        # ========= COL RIGHT: ESTADO DEL MOTOR + PPT =========
        with col_right:
            # Encabezado de card con chip dinámico
            if st.session_state.proc is None:
                chip_html = '<span class="edm-chip edm-chip-warn">INACTIVO</span>'
                estado_texto = "Motor gestual: INACTIVO"
            else:
                chip_html = '<span class="edm-chip edm-chip-ok">ACTIVO</span>'
                estado_texto = "Motor gestual: ACTIVO"

            st.markdown(
                f"""
                <div class="edm-card">
                  <div class="edm-card-header">
                    <div class="edm-card-title">Estado del motor</div>
                    {chip_html}
                  </div>
                """,
                unsafe_allow_html=True,
            )

            st.write(estado_texto)

            st.markdown("### Selecciona una presentación didáctica")

            ppt_dir = os.path.join("assets", "ppt")
            os.makedirs(ppt_dir, exist_ok=True)
            ppt_files = [f for f in os.listdir(ppt_dir) if f.lower().endswith(".pptx")]

            if not ppt_files:
                st.warning("No hay archivos .pptx en assets/ppt. Agrega tus presentaciones didácticas.")
                ppt_choice = None
            else:
                ppt_choice = st.selectbox(
                    "Presentación",
                    ppt_files,
                    label_visibility="collapsed",
                )

            auto_present = st.checkbox(
                "Intentar iniciar presentación automáticamente (F5)",
                value=True,
            )

            st.markdown("</div>", unsafe_allow_html=True)

    # ========= FILA DE BOTONES DE CONTROL =========
    st.markdown('<div class="edm-section-tight">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    start_btn = col1.button("🟢 Iniciar control gestual")
    stop_btn  = col2.button("🔴 Detener control")
    open_btn  = col3.button("📂 Abrir carpeta PPT")
    st.markdown("</div>", unsafe_allow_html=True)

    # ========= LÓGICA DE BOTONES =========

    # START
    if start_btn:
        if not ppt_files:
            st.error("No hay presentaciones para iniciar.")
        elif st.session_state.proc is not None:
            st.info("Ya hay un motor en ejecución.")
        else:
            # lanzar cámara con nombre de alumno (si quieres usar user_name aquí)
            st.session_state.proc = start_camera_slides()
            st.success("Motor gestual activo (modo presentación).")

            ppt_path = os.path.join(ppt_dir, ppt_choice)
            ok = launch_ppt_via_com(ppt_path)
            if not ok:
                launch_ppt_fallback(ppt_path, auto_f5=auto_present)
            st.info("Si no responde a gestos, haz clic en la ventana de PowerPoint para darle foco.")

    # STOP
    if stop_btn:
        if st.session_state.proc is not None:
            st.session_state.proc.terminate()
            st.session_state.proc = None
            st.success("Control gestual detenido.")
        else:
            st.info("No hay motor activo.")

    # OPEN FOLDER
    if open_btn:
        os.startfile(os.path.abspath(ppt_dir))

    # ========= CARD DE GESTOS DISPONIBLES =========
    st.markdown(
        """
        <section class="edm-section">
          <div class="edm-card">
            <div class="edm-card-header">
              <div class="edm-card-title">Gestos disponibles</div>
            </div>
            <ul class="edm-gestures-list">
              <li>✋ <strong>OPEN (mano abierta)</strong> → Siguiente diapositiva</li>
              <li>✊ <strong>FIST (puño)</strong> → Diapositiva anterior</li>
              <li>🤏 <strong>PINCH (pinza)</strong> → Activar animaciones o hipervínculos (Enter)</li>
            </ul>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "Asegúrate de que tu presentación use animaciones *al hacer clic* "
        "para que PINCH tenga efecto."
    )

def render_metrics_view():
    # ===== TITULAR DE LA SECCIÓN =====
    st.markdown(
        """
        <section class="edm-section">
          <h2 class="edm-section-title">Actividad del motor</h2>
          <p class="edm-section-subtitle">
            Revisa el historial de sesiones y gestos realizados para entender 
            cómo se está utilizando EduMotion en tus presentaciones didácticas.
          </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    # ===== BACKEND: CARGA DE LOGS =====
    def load_log_rows():
        if not os.path.exists(LOG_PATH):
            return []

        rows = []
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except:
                    pass
        return rows

    rows = load_log_rows()

    if not rows:
        st.info("Aún no hay actividad registrada.")
    else:
        df = pd.DataFrame(rows)

        total_sessions = (df["event"] == "start").sum()
        total_gestures = (df["event"] == "gesture").sum()

        # ===== FILA DE KPIs =====
        st.markdown('<div class="edm-kpi-row">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)

        with c1:
            st.metric("Sesiones ejecutadas", int(total_sessions))

        with c2:
            st.metric("Gestos realizados", int(total_gestures))

        st.markdown("</div>", unsafe_allow_html=True)

        # ===== CARD DE EVENTOS RECIENTES =====
        st.markdown(
            """
            <section class="edm-section">
              <div class="edm-card">
                <div class="edm-card-header">
                  <div class="edm-card-title">Eventos recientes</div>
                </div>
            """,
            unsafe_allow_html=True,
        )

        cols = [c for c in ["ts", "event", "mode", "gesture"] if c in df.columns]

        st.dataframe(
            df.tail(25)[cols],
            hide_index=True,
            use_container_width=True,
        )

        st.markdown("</div></section>", unsafe_allow_html=True)


# ===== BARRA DE NAVEGACIÓN DE PÁGINA (debajo del hero) =====
st.markdown('<div class="edm-nav-strip"><div class="edm-nav-strip-inner">', unsafe_allow_html=True)
col_inicio, col_control, col_metricas = st.columns(3)

with col_inicio:
    nav_button("Inicio", "inicio", "nav_inicio")

with col_control:
    nav_button("Control", "control", "nav_control")

with col_metricas:
    nav_button("Métricas", "metricas", "nav_metricas")

st.markdown('</div></div>', unsafe_allow_html=True)


#Routers
# ===== ROUTER DE PÁGINAS =====
if st.session_state.page == "inicio":
    # solo el hero; ya se pintó con components.html arriba
    pass  # si después quieres texto o cards extras de inicio, van aquí

elif st.session_state.page == "control":
    render_control_view()

elif st.session_state.page == "metricas":
    render_metrics_view()


