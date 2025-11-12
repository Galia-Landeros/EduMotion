import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(
    page_title="EduMotion - Panel",
    page_icon="🖐️",
    layout="centered"
)

st.title("🖐️ EduMotion - Panel de progreso")
st.write("Visualiza el desempeño en el minijuego de colores controlado por gestos.")

path = os.path.join("data", "colors_sessions.json")

if not os.path.exists(path):
    st.info("Aún no hay sesiones registradas. Juega primero con `colors_game.py`.")
else:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        st.error("El archivo de sesiones está dañado. Borra `colors_sessions.json` y vuelve a jugar.")
        st.stop()

    if not data:
        st.info("El archivo existe pero no tiene datos todavía.")
        st.stop()

    df = pd.DataFrame(data)

    # Métricas principales
    col1, col2, col3 = st.columns(3)
    col1.metric("Sesiones totales", len(df))
    col2.metric("Precisión promedio", f"{(df['accuracy'].mean()*100):.1f}%")
    col3.metric("Puntaje promedio", f"{df['score'].mean():.2f}")

    st.markdown("---")

    # Gráfico simple de precisión por sesión
    df_plot = df.copy()
    df_plot["label"] = range(1, len(df_plot)+1)
    st.subheader("Evolución de precisión por sesión")
    st.line_chart(
        df_plot.set_index("label")["accuracy"].multiply(100),
        height=250
    )

    st.markdown("---")
    st.subheader("Últimas sesiones")

    # Tabla ordenada por fecha (siempre útil)
    df_disp = df[["timestamp", "username", "score", "attempts", "accuracy", "duration_sec"]].copy()
    df_disp["accuracy"] = (df_disp["accuracy"] * 100).round(1)
    df_disp.rename(columns={
        "timestamp": "Fecha/Hora",
        "username": "Usuario",
        "score": "Puntos",
        "attempts": "Intentos",
        "accuracy": "Precisión (%)",
        "duration_sec": "Duración (s)"
    }, inplace=True)

    st.dataframe(
        df_disp.sort_values("Fecha/Hora", ascending=False),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")
    st.caption("EduMotion • Aprender con movimiento e inclusión.")
