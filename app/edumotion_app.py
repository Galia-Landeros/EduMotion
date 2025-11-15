import streamlit as st
import os, json
import pandas as pd
import cv2 as cv
import streamlit.components.v1 as components 
from pathlib import Path
from launchers import start_camera_slides, launch_ppt_via_com, launch_ppt_fallback
from logger import LOG_PATH

#Config de la página
st.set_page_config(
    page_title="EduMotion - Presentaciones didácticas",
    page_icon="🧩",
    layout="wide",
)

#Cargar el CSS
css_path = Path(__file__).parent.parent / "assets" / "edumotion_home.css"
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()


st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


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

        
        st.markdown('<div class="edm-kpi-row">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)

        with c1:
            st.metric("Sesiones ejecutadas", int(total_sessions))

        with c2:
            st.metric("Gestos realizados", int(total_gestures))

        st.markdown("</div>", unsafe_allow_html=True)

        
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



st.markdown('<div class="edm-topbar">', unsafe_allow_html=True)

brand_col, nav_col = st.columns([0.35, 0.65])


with brand_col:
    logo_col, text_col = st.columns([0.25, 0.75])

    with logo_col:
        
        st.image("assets/logo_edumotion_mascota.png", width=52)

    with text_col:
        st.markdown(
            '<div class="edm-brand-name">EduMotion</div>',
            unsafe_allow_html=True,
        )


with nav_col:
    col_inicio, col_control, col_metricas, _ = st.columns([0.2, 0.2, 0.2, 0.4])

    with col_inicio:
        nav_button("Inicio", "inicio", "nav_inicio")

    with col_control:
        nav_button("Control", "control", "nav_control")

    with col_metricas:
        nav_button("Métricas", "metricas", "nav_metricas")

st.markdown('</div>', unsafe_allow_html=True)


#Routers

if st.session_state.page == "inicio":
    # ===== LANDING PAGE: HERO + CARDS =====
    st.markdown('<div class="edm-landing">', unsafe_allow_html=True)

    # --- HERO ---
    st.markdown('<div class="edm-landing-hero">', unsafe_allow_html=True)
    col_left, col_right = st.columns([2, 1.1])

    with col_left:
        st.markdown(
            """
            <div class="edm-hero-badge">
              <span>Nuevo motor gestual educativo</span>
            </div>
            <h1 class="edm-hero-title">
              Aprendizaje con<br />
              <span>movimiento</span> y sin contacto
            </h1>
            <p class="edm-hero-subtitle">
              EduMotion convierte tus presentaciones, videos y juegos en experiencias
              inclusivas que responden a gestos de la mano, especialmente pensadas
              para niñas y niños con TEA o dificultades motrices.
            </p>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="edm-hero-cta">', unsafe_allow_html=True)
        if st.button("Probar modo presentación", key="hero_to_control"):
            st.session_state.page = "control"
            st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <p class="edm-hero-note">
              Compatible con PowerPoint y cualquier material que responda a teclas
              (Flechas, Enter, espacio, etc.).
            </p>
            """,
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown(
            """
            <div class="edm-hero-figure">
              <div class="edm-hero-figure-circle">
                <div class="edm-hero-figure-badge"></div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)  # cierra edm-landing-hero

    # --- CARDS BAJO EL HERO ---
    st.markdown(
        """
        <section class="edm-landing-cards">
          <article class="edm-landing-card">
            <div class="edm-landing-card-icon">🧒</div>
            <h3>Diseñado para TEA</h3>
            <p>
              Gestos claros, sin sobrecarga visual y pensados para favorecer 
              la autonomía de niñas y niños con diversidad funcional.
            </p>
          </article>

          <article class="edm-landing-card">
            <div class="edm-landing-card-icon">🖥️</div>
            <h3>Control universal</h3>
            <p>
              EduMotion envía teclas a cualquier app: presentaciones, 
              videos, juegos educativos o actividades interactivas.
            </p>
          </article>

          <article class="edm-landing-card">
            <div class="edm-landing-card-icon">📊</div>
            <h3>Métricas de progreso</h3>
            <p>
              Registra sesiones, gestos y actividades para analizar el 
              avance del grupo o de cada estudiante.
            </p>
          </article>

          <article class="edm-landing-card">
            <div class="edm-landing-card-icon">⚙️</div>
            <h3>Hecho en Python</h3>
            <p>
              OpenCV, MediaPipe y Streamlit integrados en un mismo motor, 
              fácil de instalar, extender y adaptar a tu aula.
            </p>
          </article>
        </section>
        </div>
        """,
        unsafe_allow_html=True,
    )

elif st.session_state.page == "control":
    render_control_view()

elif st.session_state.page == "metricas":
    render_metrics_view()



