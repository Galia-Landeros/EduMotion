import streamlit as st
import json, os, subprocess, sys
import pandas as pd

st.set_page_config(page_title="EduMotion", page_icon="🖐️", layout="centered")

# Estado para el proceso de la cámara
if "proc" not in st.session_state:
    st.session_state.proc = None

st.title(" EduMotion")

tab_controller, tab_dashboard = st.tabs(["Control de gestos", " Dashboard"])

with tab_controller:
    st.subheader("Controla tus materiales didácticos con gestos")

    mode = st.selectbox(
        "Selecciona el modo de uso",
        ["Presentación", "Video", "Juego (Dino)"]
    )

    # Mapear el modo a argumento
    mode_arg = {
        "Presentación": "slides",
        "Video": "video",
        "Juego (Dino)": "dino"
    }[mode]

    col1, col2 = st.columns(2)

    if col1.button("🟢 Iniciar control"):
        if st.session_state.proc is None:
            # Lanza camera.py como proceso separado con el modo
            st.session_state.proc = subprocess.Popen(
                [sys.executable, "app/camera.py", mode_arg]
            )
            st.success(f"Control gestual iniciado en modo: {mode}")
        else:
            st.info("Ya está en ejecución.")

    if col2.button("🔴 Detener control"):
        if st.session_state.proc is not None:
            st.session_state.proc.terminate()
            st.session_state.proc = None
            st.success("Control gestual detenido.")
        else:
            st.info("No hay proceso activo.")

with tab_dashboard:
    
    st.subheader("Resultados y sesiones (demo)")

    path = os.path.join("data", "colors_sessions.json")
    if not os.path.exists(path):
        st.info("Aún no hay sesiones guardadas. Juega primero con EduMotion.")
    else:
        try:
            data = json.load(open(path, "r", encoding="utf-8"))
        except json.JSONDecodeError:
            st.error("Archivo de sesiones dañado. Borra colors_sessions.json y vuelve a jugar.")
        else:
            if not data:
                st.info("Sin datos todavía.")
            else:
                df = pd.DataFrame(data)
                col1, col2, col3 = st.columns(3)
                col1.metric("Sesiones", len(df))
                col2.metric("Precisión promedio", f"{df['accuracy'].mean()*100:.1f}%")
                col3.metric("Puntaje promedio", f"{df['score'].mean():.2f}")

                st.line_chart(df["accuracy"].multiply(100), height=200)

                st.write("Últimas sesiones:")
                st.dataframe(df.sort_values("timestamp", ascending=False), hide_index=True)
