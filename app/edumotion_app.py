import streamlit as st
import json, os, subprocess, sys
import pandas as pd

from launchers import start_camera, launch_ppt_via_com, launch_ppt_fallback
from logger import LOG_PATH

st.set_page_config(page_title="EduMotion", page_icon="🖐️", layout="centered")

# Estado para el proceso de la cámara
if "proc" not in st.session_state:
    st.session_state.proc = None

# ----- ESTILO BÁSICO -----
st.markdown("""
<style>
body { background-color: #F2F6FF; }
.main { background: linear-gradient(135deg, #F2F6FF 0%, #D9EAFD 100%); border-radius: 16px; padding: 16px; }
h1,h2,h3 { color:#1E3A8A; font-family: 'Segoe UI', system-ui, sans-serif; }
</style>
""", unsafe_allow_html=True)

st.title("🖐️ EduMotion")
st.caption("Aprender con movimiento e inclusión.")

tab_control, tab_metrics, tab_about = st.tabs(["🎮 Control gestual", "📊 Métricas", "ℹ️ Acerca de"])

# ======= TAB CONTROL =======
with tab_control:
    st.header("Controla materiales didácticos con gestos")

    mode = st.selectbox("Modo de uso", ["Presentación", "Video educativo", "Juego (Dino)"])
    mode_arg = {"Presentación":"slides","Video educativo":"video","Juego (Dino)":"dino"}[mode]

    # (Opcional) Selector de PPT si eliges Presentación
    ppt_dir = os.path.join("assets","ppt")
    os.makedirs(ppt_dir, exist_ok=True)
    ppt_files = [f for f in os.listdir(ppt_dir) if f.lower().endswith(".pptx")]

    if mode == "Presentación":
        if ppt_files:
            ppt_choice = st.selectbox("Selecciona juego/plantilla PPT", ppt_files)
        else:
            st.warning("No hay .pptx en assets/ppt. Agrega tus juegos/plantillas.")

        auto_present = st.checkbox("Intentar iniciar presentación automáticamente (F5)", value=True)

    col1, col2, col3 = st.columns(3)

    if col1.button("🟢 Iniciar control"):
        if st.session_state.proc is None:
            st.session_state.proc = start_camera(mode_arg)
            st.success(f"Control gestual activo en modo: {mode}")

            if mode == "Presentación" and ppt_files:
                ppt_path = os.path.join(ppt_dir, ppt_choice)
                ok = launch_ppt_via_com(ppt_path)
                if not ok:
                    launch_ppt_fallback(ppt_path, auto_f5=auto_present)
                st.info("Si no responde a gestos, haz clic en la ventana de PowerPoint para darle foco.")
        else:
            st.info("Ya hay un motor en ejecución.")

    if col2.button("🔴 Detener control"):
        if st.session_state.proc is not None:
            st.session_state.proc.terminate()
            st.session_state.proc = None
            st.success("Control gestual detenido.")
        else:
            st.info("No hay proceso activo.")

    if col3.button("📂 Abrir carpeta PPT"):
        os.startfile(os.path.abspath(ppt_dir))

    st.markdown("---")
    st.subheader("Instrucciones rápidas")
    st.write("""
    - **Presentación (slides):** ✋ OPEN = Siguiente, ✊ FIST = Atrás, 🤏 PINCH = Enter/click.
    - **Video:** 🤏 PINCH = Play/Pausa, ✋ OPEN = Adelantar, ✊ FIST = Retroceder.
    - **Dino:** 🤏 PINCH = Saltar.
    """)
    st.info("Recuerda: la ventana que recibe las teclas debe tener el foco (clic sobre ella).")

# ======= TAB MÉTRICAS =======
with tab_metrics:
    st.header("Actividad del motor gestual")
    if not os.path.exists(LOG_PATH):
        st.info("Aún no hay actividad registrada.")
    else:
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

        if not rows:
            st.info("Sin registros válidos aún.")
        else:
            df = pd.DataFrame(rows)

            total_sessions = (df["event"] == "start").sum()
            total_gestures = (df["event"] == "gesture").sum()

            c1, c2 = st.columns(2)
            c1.metric("Sesiones ejecutadas", int(total_sessions))
            c2.metric("Gestos detectados", int(total_gestures))

            st.markdown("### Gestos por modo")
            dfg = df[df["event"]=="gesture"].groupby("mode")["gesture"].count()
            if len(dfg):
                st.bar_chart(dfg)
            else:
                st.info("Aún no hay gestos registrados.")

            st.markdown("### Eventos recientes")
            st.dataframe(
                df.tail(30)[["ts","event","mode","gesture"]],
                hide_index=True,
                use_container_width=True
            )

            st.markdown("---")
            if st.button("🧹 Limpiar log de actividad"):
                try:
                    os.remove(LOG_PATH)
                    st.success("Log reiniciado. Genera eventos nuevos para ver métricas.")
                except Exception as e:
                    st.error(f"No se pudo eliminar: {e}")

# ======= TAB ACERCA DE =======
with tab_about:
    st.header("Acerca de EduMotion")
    st.markdown("""
**EduMotion** es un sistema universal de control gestual para **materiales didácticos**:
presentaciones, videos y juegos educativos. Diseñado para **inclusión y accesibilidad** (TEA, motricidad).

- Cámara estándar + gestos naturales (🤏 PINCH, ✋ OPEN, ✊ FIST).
- Control sin contacto: **teclas simuladas** para apps existentes.
- **Registro de actividad** para evidenciar uso e impacto.

> “EduMotion: aprende moviéndote, conecta sin tocar.”
""")