import streamlit as st
import json, os, subprocess, sys
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
# =============================================
# CONFIGURACIÓN PRINCIPAL
# =============================================
st.set_page_config(
    page_title="EduMotion",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# CSS COMPATIBLE CON STREAMLIT - MANTENIENDO TODO IGUAL EXCEPTO EL FONDO
# =============================================
st.markdown("""
<style>
    .title-wrapper {
        text-align: center;
        margin-top: 1.5rem;
        margin-bottom: 2rem;
        padding: 2.5rem;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.85));
        border-radius: 25px;
        border: 4px solid #314CB6;
        box-shadow: 0 12px 35px rgba(49, 76, 182, 0.3);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }

    .title-wrapper::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(239, 189, 235, 0.2), transparent);
        transform: rotate(45deg);
        z-index: 0;
    }

    .rainbow-title-3d {
        font-family: 'Poppins', sans-serif;
        font-size: 5rem;
        font-weight: 900;
        background: linear-gradient(
            135deg, 
            #EFBDEB 0%, 
            #B68CB8 25%, 
            #6461A0 50%, 
            #314CB6 75%, 
            #0A5FD1 100%
        );
        -webkit-background-clip: text;
        color: transparent;
        text-shadow:
            3px 3px 0px rgba(0,0,0,0.15),
            6px 6px 0px rgba(0,0,0,0.10),
            9px 9px 0px rgba(0,0,0,0.05);
        position: relative;
        z-index: 1;
        margin-bottom: 1.5rem;
        letter-spacing: 2px;
    }

    .main-tagline {
        font-size: 1.8rem;
        color: #6461A0;
        background: linear-gradient(135deg, rgba(239, 189, 235, 0.4), rgba(182, 140, 184, 0.3));
        padding: 1rem 3rem;
        border-radius: 15px;
        display: inline-block;
        font-style: italic;
        font-weight: 600;
        border: 2px solid rgba(255,255,255,0.5);
        position: relative;
        z-index: 1;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
    }
    
</style>

<div class="title-wrapper">
    <div class="rainbow-title-3d">EduMotion</div>
    <div class="main-tagline">Donde los Gestos Cobran Vida con Magia</div>
</div>
""", unsafe_allow_html=True)

# =============================================
# CSS - SOLO CAMBIO EL FONDO A AZUL MÁS SUAVE
# =============================================
st.markdown("""
<style>
    /* FONDO CON AZULES MÁS SUAVES Y PASTEL */
    .stApp {
        background: linear-gradient(135deg, 
            #FFD6E7 0%,     /* Rosa muy suave */
            #FFC8E8 25%,    /* Rosa-lila suave */
            #C8D0FF 50%,    /* Azul lila pastel */
            #A0B8FF 75%,    /* Azul celeste suave */
            #8AAFFF 100%    /* Azul principal suavizado */
        );
    }
    
    /* EL RESTO DEL CSS SE MANTIENE EXACTAMENTE IGUAL */
    
    /* CONTENEDOR DE PESTAÑAS */
    .tabs-container {
        margin: 2rem 0;
        padding: 0 1rem;
    }
    
    /* PESTAÑAS MÁS DESTACADAS Y LLAMATIVAS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        padding: 1.5rem;
        margin: 0;
        border-radius: 25px;
        border: 3px solid rgba(255,255,255,0.3);
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 90px;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.85));
        border-radius: 20px;
        padding: 1rem 1.5rem;
        color: #314CB6;
        font-weight: 800;
        font-size: 1.2rem;
        transition: all 0.4s ease;
        border: 3px solid transparent;
        box-shadow: 0 8px 25px rgba(49, 76, 182, 0.2);
        margin: 0 2px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex: 1;
        min-width: 0;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"]::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.6s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover::before {
        left: 100%;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 15px 35px rgba(49, 76, 182, 0.3);
        border: 3px solid #314CB6;
        background: linear-gradient(135deg, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0.9));
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #314CB6, #6461A0) !important;
        color: white !important;
        box-shadow: 0 12px 30px rgba(49, 76, 182, 0.5);
        border: 3px solid #EFBDEB;
        transform: translateY(-5px) scale(1.08);
    }
    
    .stTabs [aria-selected="true"]:hover {
        transform: translateY(-8px) scale(1.1);
        box-shadow: 0 18px 40px rgba(49, 76, 182, 0.7);
    }
    
    /* EFECTO DE BORDE MEJORADO PARA PESTAÑAS ACTIVAS */
    .stTabs [aria-selected="true"]::after {
        content: "";
        position: absolute;
        top: -4px;
        left: -4px;
        right: -4px;
        bottom: -4px;
        background: linear-gradient(135deg, #EFBDEB, #B68CB8, #6461A0, #314CB6, #0A5FD1);
        border-radius: 24px;
        z-index: -1;
        filter: blur(8px);
        opacity: 0.8;
    }
    
    /* ============================================ */
    /* CARDS DE SELECCIÓN MÁS DESTACADAS */
    /* ============================================ */
    
    .cards-container {
        display: flex;
        justify-content: space-between;
        gap: 25px;
        margin: 3rem 0;
    }
    
    .mode-card {
        flex: 1;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.85));
        border-radius: 25px;
        padding: 2.5rem 2rem;
        text-align: center;
        border: 4px solid #B68CB8;
        transition: all 0.4s ease;
        cursor: pointer;
        box-shadow: 0 10px 30px rgba(100, 97, 160, 0.2);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .mode-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #EFBDEB, #B68CB8, #6461A0, #314CB6);
    }
    
    .mode-card:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 0 20px 40px rgba(49, 76, 182, 0.3);
        border: 4px solid #314CB6;
    }
    
    .mode-card.selected {
        border: 4px solid #314CB6;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(49, 76, 182, 0.15));
        box-shadow: 0 15px 35px rgba(49, 76, 182, 0.4);
        transform: translateY(-5px);
    }
    
    .card-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        display: block;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.2));
    }
    
    .card-title {
        font-size: 1.6rem;
        font-weight: 800;
        color: #314CB6;
        margin-bottom: 1rem;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .card-description {
        color: #6461A0;
        font-size: 1rem;
        line-height: 1.5;
        font-weight: 500;
    }
    
    .selected-badge {
        background: linear-gradient(135deg, #314CB6, #6461A0);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 700;
        margin-top: 1.5rem;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(49, 76, 182, 0.3);
        border: 2px solid white;
    }
    
    /* TARJETA DE ESTADO MEJORADA */
    .status-simple {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.85));
        padding: 2rem;
        border-radius: 20px;
        border: 3px solid #314CB6;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(49, 76, 182, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .status-title {
        color: #314CB6;
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        text-align: center;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .status-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.8rem 0;
        border-bottom: 2px solid rgba(182, 140, 184, 0.2);
        font-size: 1.1rem;
    }
    
    .status-item:last-child {
        border-bottom: none;
    }
    
    .status-label {
        font-weight: 700;
        color: #6461A0;
    }
    
    .status-value {
        font-weight: 800;
        color: #314CB6;
        font-size: 1.2rem;
    }
    
    .status-active {
        color: #314CB6;
        font-weight: 800;
        background: rgba(72, 187, 120, 0.1);
        padding: 0.3rem 1rem;
        border-radius: 10px;
        border: 2px solid #314CB6;
    }
    
    .status-inactive {
        color: #B68CB8;
        font-weight: 800;
        background: rgba(160, 174, 192, 0.1);
        padding: 0.3rem 1rem;
        border-radius: 10px;
        border: 2px solid #B68CB8;
    }
    
    /* ============================================ */
    /* BOTONES MÁGICOS MÁS DESTACADOS */
    /* ============================================ */
    
    .magic-buttons-container {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.85));
        padding: 2.5rem;
        border-radius: 25px;
        border: 4px solid #314CB6;
        margin: 3rem 0;
        box-shadow: 0 15px 35px rgba(49, 76, 182, 0.3);
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .magic-buttons-title {
        color: #314CB6;
        font-size: 2rem;
        font-weight: 900;
        margin-bottom: 2rem;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, rgba(239, 189, 235, 0.3), rgba(182, 140, 184, 0.2));
        padding: 1rem 2rem;
        border-radius: 15px;
        display: inline-block;
        border: 2px solid rgba(49, 76, 182, 0.3);
    }
    
    /* BOTONES MÁGICOS MÁS GRANDES Y DESTACADOS */
    .stButton > button {
        width: 100% !important;
        height: 90px !important;
        border-radius: 25px !important;
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        font-family: 'Comic Sans MS', cursive, sans-serif !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 10px 30px rgba(49, 76, 182, 0.3) !important;
        border: none !important;
        margin: 0.8rem 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        position: relative !important;
        overflow: hidden !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2) !important;
    }
    
    .stButton > button::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.6s ease;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-8px) scale(1.08) !important;
        box-shadow: 0 20px 40px rgba(49, 76, 182, 0.5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-4px) scale(1.04) !important;
    }
    
    /* BOTÓN ACTIVAR ESPECIAL MÁS DESTACADO */
    div[data-testid="column"]:nth-child(1) .stButton > button {
        background: linear-gradient(135deg, #314CB6, #6461A0) !important;
        color: white !important;
        border: 3px solid #EFBDEB !important;
    }
    
    div[data-testid="column"]:nth-child(1) .stButton > button:hover {
        background: linear-gradient(135deg, #6461A0, #314CB6) !important;
        box-shadow: 0 20px 45px rgba(49, 76, 182, 0.6) !important;
    }
    
    /* BOTÓN PAUSAR ESPECIAL MÁS DESTACADO */
    div[data-testid="column"]:nth-child(2) .stButton > button {
        background: linear-gradient(135deg, #B68CB8, #6461A0) !important;
        color: white !important;
        border: 3px solid #EFBDEB !important;
    }
    
    div[data-testid="column"]:nth-child(2) .stButton > button:hover {
        background: linear-gradient(135deg, #6461A0, #B68CB8) !important;
        box-shadow: 0 20px 45px rgba(182, 140, 184, 0.6) !important;
    }
    
    /* BOTÓN REINICIAR ESPECIAL MÁS DESTACADO */
    div[data-testid="column"]:nth-child(3) .stButton > button {
        background: linear-gradient(135deg, #0A5FD1, #314CB6) !important;
        color: white !important;
        border: 3px solid #EFBDEB !important;
    }
    
    div[data-testid="column"]:nth-child(3) .stButton > button:hover {
        background: linear-gradient(135deg, #314CB6, #0A5FD1) !important;
        box-shadow: 0 20px 45px rgba(10, 95, 209, 0.6) !important;
    }

    /* ESTILOS PARA INSTRUCCIONES MÁS DESTACADAS */
    .instructions-container {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.85));
        padding: 2.5rem;
        border-radius: 25px;
        border: 4px solid #314CB6;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(49, 76, 182, 0.3);
        backdrop-filter: blur(10px);
    }

    .instructions-title {
        color: #314CB6;
        font-size: 2rem;
        font-weight: 900;
        margin-bottom: 2rem;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, rgba(239, 189, 235, 0.3), rgba(182, 140, 184, 0.2));
        padding: 1rem 2rem;
        border-radius: 15px;
        display: inline-block;
    }

    /* ESTILOS PARA PANEL DE PROGRESO MÁS DESTACADO */
    .progress-container {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.85));
        padding: 2.5rem;
        border-radius: 25px;
        border: 4px solid #314CB6;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(49, 76, 182, 0.3);
        backdrop-filter: blur(10px);
    }

    .progress-title {
        color: #314CB6;
        font-size: 2rem;
        font-weight: 900;
        margin-bottom: 2rem;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    /* ESTILOS PARA MÉTRICAS MÁS DESTACADAS */
    .metric-card {
        background: linear-gradient(135deg, #314CB6, #6461A0);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(49, 76, 182, 0.4);
        border: 3px solid #EFBDEB;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(49, 76, 182, 0.6);
    }

    .metric-value {
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 0.8rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }

    .metric-label {
        font-size: 1.1rem;
        font-weight: 700;
        opacity: 0.95;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# EL RESTO DEL CÓDIGO SE MANTIENE EXACTAMENTE IGUAL
# =============================================

# ESTADO DE LA APLICACIÓN
if "proc" not in st.session_state:
    st.session_state.proc = None

if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = "Presentación"

# CONTENEDOR PARA PESTAÑAS
st.markdown('<div class="tabs-container">', unsafe_allow_html=True)

# PESTAÑAS PRINCIPALES SIN EMOJIS
tab1, tab2, tab3 = st.tabs([
    "**Casa Mágica**", 
    "**Instrucciones**", 
    "**Panel de Progreso**"
])

st.markdown('</div>', unsafe_allow_html=True)

# PESTAÑA 1: CASA MÁGICA SIN EMOJIS
with tab1:
    st.markdown("## Casa Mágica de Controles")
    st.markdown("### ¡Aquí es donde la magia comienza! Configura tus poderes gestuales")
    
    st.markdown("### Elige tu Aventura")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        is_selected = st.session_state.selected_mode == "Presentación"
        card_class = "mode-card selected" if is_selected else "mode-card"
        st.markdown(f"""
        <div class="{card_class}">
            <div class="card-title">Presentación</div>
            <div class="card-description">Controla diapositivas y presentaciones con gestos mágicos</div>
            {'''<div class="selected-badge">Seleccionado</div>''' if is_selected else ""}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Seleccionar Presentación", key="btn_presentacion", use_container_width=True):
            st.session_state.selected_mode = "Presentación"
            st.rerun()
    
    with col2:
        is_selected = st.session_state.selected_mode == "Video"
        card_class = "mode-card selected" if is_selected else "mode-card"
        st.markdown(f"""
        <div class="{card_class}">
            <div class="card-title">Video</div>
            <div class="card-description">Controla reproducción de videos con movimientos de manos</div>
            {'''<div class="selected-badge">Seleccionado</div>''' if is_selected else ""}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Seleccionar Video", key="btn_video", use_container_width=True):
            st.session_state.selected_mode = "Video"
            st.rerun()
    
    with col3:
        is_selected = st.session_state.selected_mode == "Juego (Dino)"
        card_class = "mode-card selected" if is_selected else "mode-card"
        st.markdown(f"""
        <div class="{card_class}">
            <div class="card-title">Juego (Dino)</div>
            <div class="card-description">Juega al dinosaurio de Chrome con gestos divertidos</div>
            {'''<div class="selected-badge">Seleccionado</div>''' if is_selected else ""}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Seleccionar Juego", key="btn_juego", use_container_width=True):
            st.session_state.selected_mode = "Juego (Dino)"
            st.rerun()
    
    mode = st.session_state.selected_mode
    mode_arg = {
        "Presentación": "slides",
        "Video": "video", 
        "Juego (Dino)": "dino"
    }[mode]
    
    st.markdown("""
    <div class="status-simple">
        <div class="status-title">Tu Estado Mágico</div>
        <div class="status-item">
            <span class="status-label">Modo seleccionado:</span>
            <span class="status-value">{}</span>
        </div>
        <div class="status-item">
            <span class="status-label">Poderes:</span>
            <span class="{}">{}</span>
        </div>
        <div class="status-item">
            <span class="status-label">Aventura:</span>
            <span class="status-value">{}</span>
        </div>
    </div>
    """.format(
        mode,
        "status-active" if st.session_state.proc is not None else "status-inactive",
        "Activo" if st.session_state.proc is not None else "Inactivo",
        mode
    ), unsafe_allow_html=True)
    
    if st.session_state.proc is not None:
        st.info(f"**PID del proceso:** `{st.session_state.proc.pid}`")
    
    st.markdown("---")
    
    st.markdown("""
    <div class="magic-buttons-container">
        <div class="magic-buttons-title">Botones Mágicos</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        if st.button("**Activar Poderes**", key="start", use_container_width=True):
            if st.session_state.proc is None:
                # ruta absoluta a camera.py dentro de la carpeta app
                camera_path = os.path.join(BASE_DIR, "camera.py")
                st.session_state.proc = subprocess.Popen(
                [sys.executable, camera_path, mode_arg]
            )
            st.success(f"¡Magia activada! Modo: {mode}")
            st.balloons()
        else:
            st.info("¡Tus poderes ya están activos!")
           
    
    
    with col_btn2:
        if st.button("**Pausar Magia**", key="stop", use_container_width=True):
            if st.session_state.proc is not None:
                st.session_state.proc.terminate()
                st.session_state.proc = None
                st.success("Magia pausada. ¡Descansa!")
            else:
                st.info("No hay magia activa en este momento")
    
    with col_btn3:
        if st.button("**Reiniciar Todo**", key="restart", use_container_width=True):
            st.session_state.proc = None
            st.rerun()

# PESTAÑA 2: INSTRUCCIONES SIN EMOJIS
with tab2:
    st.markdown("## Instrucciones")
    st.markdown("### ¡Aprende cómo usar la magia de los gestos!")
    
    st.markdown("""
    <div class="instructions-container">
        <div class="instructions-title">Escribe tus Instrucciones Aquí</div>
    </div>
    """, unsafe_allow_html=True)
    
    instrucciones = st.text_area(
        "**Escribe las instrucciones para usar EduMotion:**",
        placeholder="Por ejemplo:\n• Colócate frente a la cámara\n• Asegúrate de tener buena iluminación\n• Haz gestos con las manos claramente\n• Mantén las manos dentro del área de detección...",
        height=300,
        help="Escribe aquí todas las instrucciones que los usuarios necesitan saber para usar la aplicación correctamente."
    )
    
    if st.button("Guardar Instrucciones", key="guardar_instrucciones"):
        if instrucciones:
            st.success("¡Instrucciones guardadas correctamente!")
        else:
            st.warning("Escribe algunas instrucciones antes de guardar")

# PESTAÑA 3: PANEL DE PROGRESO SIN EMOJIS
with tab3:
    st.markdown("## Panel de Progreso")
    st.markdown("### Visualiza el desempeño en el minijuego de colores controlado por gestos")
    
    path = os.path.join("data", "colors_sessions.json")

    if not os.path.exists(path):
        st.info("Aún no hay sesiones registradas. Juega primero con el minijuego de colores.")
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

        st.markdown("### Métricas Principales")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(df)}</div>
                <div class="metric-label">Sesiones totales</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            precision_promedio = f"{(df['accuracy'].mean()*100):.1f}%"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{precision_promedio}</div>
                <div class="metric-label">Precisión promedio</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            puntaje_promedio = f"{df['score'].mean():.2f}"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{puntaje_promedio}</div>
                <div class="metric-label">Puntaje promedio</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        df_plot = df.copy()
        df_plot["label"] = range(1, len(df_plot)+1)
        
        st.line_chart(
            df_plot.set_index("label")["accuracy"].multiply(100),
            height=300
        )

        st.markdown("---")
        
        st.markdown("### Historial de Sesiones")
        
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

# FOOTER SIN EMOJIS
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2.5rem; background: linear-gradient(135deg, rgba(239, 189, 235, 0.9), rgba(182, 140, 184, 0.8)); border-radius: 25px; margin-top: 3rem; border: 3px solid #314CB6; box-shadow: 0 10px 30px rgba(49, 76, 182, 0.2);">
    <div style="font-size: 1.8rem; color: #314CB6; margin-bottom: 0.8rem; font-weight: 800; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
        EduMotion - Donde los Gestos son Magia
    </div>
    <div style="color: #6461A0; font-size: 1.1rem; font-weight: 600;">
        Para niños super inteligentes y creativos como tú
    </div>
    <div style="margin-top: 1.2rem; font-size: 1rem; color: #B68CB8; font-weight: 600;">
        Hecho con amor para hacer el aprendizaje divertido
    </div>
</div>
""", unsafe_allow_html=True)