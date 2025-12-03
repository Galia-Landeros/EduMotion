import streamlit as st
import json, os, subprocess, sys
import pandas as pd

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
# CSS COMPATIBLE CON STREAMLIT
# =============================================
st.markdown("""
<style>
    .title-wrapper {
        text-align: center;
        margin-top: 1.5rem;
        margin-bottom: 2rem;
    }

    .rainbow-title-3d {
        font-family: 'Poppins', sans-serif;
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(
            90deg, 
            #ff005e, 
            #ff9900, 
            #ffee00, 
            #33dd55, 
            #00ccff, 
            #6a00ff, 
            #ff00aa
        );
        background-size: 300%;
        -webkit-background-clip: text;
        color: transparent;

        /* Sombra 3D */
        text-shadow:
            2px 2px 0px rgba(0,0,0,0.15),
            4px 4px 0px rgba(0,0,0,0.10),
            6px 6px 0px rgba(0,0,0,0.07);

        animation: rainbowShift 5s linear infinite;
    }

    @keyframes rainbowShift {
        0% { background-position: 0%; }
        100% { background-position: 200%; }
    }

    .rainbow-sub {
        font-size: 1.4rem;
        color: white;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.4);
        font-weight: 600;
        margin-top: -10px;
    }

    .rainbow-tagline {
        font-size: 1.1rem;
        color: white;
        background: rgba(0,0,0,0.25);
        padding: 6px 16px;
        border-radius: 10px;
        display: inline-block;
        margin-top: 8px;
        font-style: italic;
    }
    
</style>

<div class="title-wrapper">
    <div class="rainbow-title-3d">EduMotion</div>
    <div class="rainbow-sub">Donde los Gestos Cobran Vida</div>
    <div class="rainbow-tagline">Aprende, Juega y Crece con Magia</div>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<style>
    /* FONDO INFANTIL CON GRADIENTE */
    .stApp {
        background: linear-gradient(135deg, 
            #ff9a9e 0%, 
            #fad0c4 25%, 
            #fad0c4 50%, 
            #a1c4fd 75%, 
            #c2e9fb 100%);
        background-size: 400% 400%;
        animation: gradientBackground 15s ease infinite;
    }
    
    @keyframes gradientBackground {
        0% { background-position: 0% 50% }
        50% { background-position: 100% 50% }
        100% { background-position: 0% 50% }
    }
    
    /* BLOQUE DE TÍTULO SIMPLIFICADO */
    .title-block {
        background: linear-gradient(135deg, #8A2BE2, #6A5ACD);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem auto;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        border: 5px solid white;
        max-width: 90%;
    }
    
    /* TÍTULO SIMPLE */
    .main-title {
        font-size: 3.5rem;
        font-weight: bold;
        color: white;
        margin-bottom: 0.5rem;
        font-family: 'Arial', sans-serif;
    }
    
    /* SUBTÍTULO SIMPLE */
    .main-subtitle {
        font-size: 1.5rem;
        color: white;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    /* TAGLINE SIMPLE */
    .main-tagline {
        font-size: 1.1rem;
        color: white;
        font-style: italic;
        background: rgba(0, 0, 0, 0.2);
        padding: 0.5rem 1rem;
        border-radius: 10px;
        display: inline-block;
    }

    /* CONTENEDOR DE PESTAÑAS CON MEJOR ESPACIADO */
    .tabs-container {
        margin: 2rem 0;
        padding: 0 1rem;
    }
    
    /* PESTAÑAS MEJORADAS CON MÁS ESPACIO */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: transparent;
        padding: 1rem 0;
        margin: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 80px;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7));
        border-radius: 20px;
        padding: 1rem 1.5rem;
        color: #666;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.4s ease;
        border: 3px solid transparent;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
        margin: 0 2px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex: 1;
        min-width: 0;
        position: relative;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(138, 43, 226, 0.2);
        border: 3px solid #8A2BE2;
        background: linear-gradient(135deg, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0.9));
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8A2BE2, #6A5ACD) !important;
        color: white !important;
        box-shadow: 0 8px 25px rgba(138, 43, 226, 0.4);
        border: 3px solid white;
        transform: translateY(-3px);
    }
    
    .stTabs [aria-selected="true"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(138, 43, 226, 0.6);
    }
    
    /* EFECTO DE BORDE ARCOÍRIS ANIMADO EN PESTAÑA ACTIVA */
    .stTabs [aria-selected="true"]::before {
        content: "";
        position: absolute;
        top: -3px;
        left: -3px;
        right: -3px;
        bottom: -3px;
        background: linear-gradient(45deg, #ff00cc, #3333ff, #00ff00, #ffcc00, #ff00cc);
        border-radius: 23px;
        z-index: -1;
        animation: borderGlow 3s linear infinite;
        background-size: 400% 400%;
        filter: blur(2px);
    }
    
    @keyframes borderGlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* ============================================ */
    /* NUEVO DISEÑO CON 3 CARDS PARA SELECCIÓN */
    /* ============================================ */
    
    /* CONTENEDOR DE CARDS */
    .cards-container {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin: 2rem 0;
    }
    
    /* CARDS INDIVIDUALES */
    .mode-card {
        flex: 1;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        border: 3px solid #E0E0E0;
        transition: all 0.3s ease;
        cursor: pointer;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
    }
    
    .mode-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
    }
    
    .mode-card.selected {
        border: 3px solid #8A2BE2;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(138, 43, 226, 0.1));
        box-shadow: 0 8px 25px rgba(138, 43, 226, 0.3);
    }
    
    /* ICONOS DE LAS CARDS */
    .card-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    /* TÍTULOS DE LAS CARDS */
    .card-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #8A2BE2;
        margin-bottom: 0.5rem;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    
    .card-description {
        color: #666;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    /* INDICADOR DE SELECCIÓN */
    .selected-badge {
        background: #8A2BE2;
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 1rem;
        display: inline-block;
    }
    
    /* TARJETA DE ESTADO SIMPLE */
    .status-simple {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #8A2BE2;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .status-title {
        color: #8A2BE2;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    
    .status-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .status-item:last-child {
        border-bottom: none;
    }
    
    .status-label {
        font-weight: 600;
        color: #666;
    }
    
    .status-value {
        font-weight: 700;
        color: #8A2BE2;
    }
    
    .status-active {
        color: #48bb78;
        font-weight: 700;
    }
    
    .status-inactive {
        color: #a0aec0;
        font-weight: 700;
    }
    
    /* ============================================ */
    /* NUEVO DISEÑO PARA BOTONES MÁGICOS */
    /* ============================================ */
    
    .magic-buttons-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        border: 3px solid #8A2BE2;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(138, 43, 226, 0.2);
        text-align: center;
    }
    
    .magic-buttons-title {
        color: #8A2BE2;
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* BOTONES MÁGICOS PERSONALIZADOS */
    .stButton > button {
        width: 100% !important;
        height: 80px !important;
        border-radius: 20px !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        font-family: 'Comic Sans MS', cursive, sans-serif !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2) !important;
        border: none !important;
        margin: 0.5rem 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(1.02) !important;
    }
    
    /* BOTÓN ACTIVAR ESPECIAL */
    div[data-testid="column"]:nth-child(1) .stButton > button {
        background: linear-gradient(135deg, #48bb78, #38a169) !important;
        color: white !important;
    }
    
    div[data-testid="column"]:nth-child(1) .stButton > button:hover {
        background: linear-gradient(135deg, #38a169, #48bb78) !important;
        box-shadow: 0 12px 30px rgba(72, 187, 120, 0.4) !important;
    }
    
    /* BOTÓN PAUSAR ESPECIAL */
    div[data-testid="column"]:nth-child(2) .stButton > button {
        background: linear-gradient(135deg, #e53e3e, #c53030) !important;
        color: white !important;
    }
    
    div[data-testid="column"]:nth-child(2) .stButton > button:hover {
        background: linear-gradient(135deg, #c53030, #e53e3e) !important;
        box-shadow: 0 12px 30px rgba(229, 62, 62, 0.4) !important;
    }
    
    /* BOTÓN REINICIAR ESPECIAL */
    div[data-testid="column"]:nth-child(3) .stButton > button {
        background: linear-gradient(135deg, #ed8936, #dd6b20) !important;
        color: white !important;
    }
    
    div[data-testid="column"]:nth-child(3) .stButton > button:hover {
        background: linear-gradient(135deg, #dd6b20, #ed8936) !important;
        box-shadow: 0 12px 30px rgba(237, 137, 54, 0.4) !important;
    }
    
    /* ICONOS EN BOTONES */
    .stButton > button::after {
        font-size: 1.8rem;
        margin-right: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# ESTADO DE LA APLICACIÓN
# =============================================
if "proc" not in st.session_state:
    st.session_state.proc = None

# Inicializar el modo seleccionado si no existe
if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = "Presentación"


# =============================================
# CONTENEDOR PARA PESTAÑAS CON MEJOR DISTRIBUCIÓN
# =============================================
st.markdown('<div class="tabs-container">', unsafe_allow_html=True)

# =============================================
# PESTAÑAS PRINCIPALES MEJOR ESPACIADAS
# =============================================
tab1, tab2, tab3 = st.tabs([
    "🏠 **Casa Mágica**", 
    "🎮 **Mundo de Juegos**", 
    "📊 **Tablero Mágico**"
])

st.markdown('</div>', unsafe_allow_html=True)

# =============================================
# PESTAÑA 1: CASA MÁGICA - NUEVO DISEÑO CON 3 CARDS
# =============================================
with tab1:
    # TÍTULO PRINCIPAL
    st.markdown("## 🏠 Casa Mágica de Controles")
    st.markdown("### ¡Aquí es donde la magia comienza! Configura tus poderes gestuales 🎯")
    
    # TRES CARDS PARA SELECCIÓN DE MODO
    st.markdown("### 🎯 Elige tu Aventura")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        is_selected = st.session_state.selected_mode == "Presentación"
        card_class = "mode-card selected" if is_selected else "mode-card"
        st.markdown(f"""
        <div class="{card_class}" onclick="selectMode('Presentación')">
            <div class="card-icon">📊</div>
            <div class="card-title">Presentación</div>
            <div class="card-description">Controla diapositivas y presentaciones con gestos mágicos</div>
            {'''<div class="selected-badge">✓ Seleccionado</div>''' if is_selected else ""}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Seleccionar Presentación", key="btn_presentacion", use_container_width=True):
            st.session_state.selected_mode = "Presentación"
            st.rerun()
    
    with col2:
        is_selected = st.session_state.selected_mode == "Video"
        card_class = "mode-card selected" if is_selected else "mode-card"
        st.markdown(f"""
        <div class="{card_class}" onclick="selectMode('Video')">
            <div class="card-icon">🎬</div>
            <div class="card-title">Video</div>
            <div class="card-description">Controla reproducción de videos con movimientos de manos</div>
            {'''<div class="selected-badge">✓ Seleccionado</div>''' if is_selected else ""}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Seleccionar Video", key="btn_video", use_container_width=True):
            st.session_state.selected_mode = "Video"
            st.rerun()
    
    with col3:
        is_selected = st.session_state.selected_mode == "Juego (Dino)"
        card_class = "mode-card selected" if is_selected else "mode-card"
        st.markdown(f"""
        <div class="{card_class}" onclick="selectMode('Juego (Dino)')">
            <div class="card-icon">🦖</div>
            <div class="card-title">Juego (Dino)</div>
            <div class="card-description">Juega al dinosaurio de Chrome con gestos divertidos</div>
            {'''<div class="selected-badge">✓ Seleccionado</div>''' if is_selected else ""}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Seleccionar Juego", key="btn_juego", use_container_width=True):
            st.session_state.selected_mode = "Juego (Dino)"
            st.rerun()
    
    # CONVERSIÓN DEL MODO SELECCIONADO (MANTIENE LA FUNCIONALIDAD ORIGINAL)
    mode = st.session_state.selected_mode
    mode_arg = {
        "Presentación": "slides",
        "Video": "video", 
        "Juego (Dino)": "dino"
    }[mode]
    
    # TARJETA DE ESTADO SIMPLE
    st.markdown("""
    <div class="status-simple">
        <div class="status-title">📊 Tu Estado Mágico</div>
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
    
    # MOSTRAR PID SI ESTÁ ACTIVO
    if st.session_state.proc is not None:
        st.info(f"**PID del proceso:** `{st.session_state.proc.pid}`")
    
    # SEPARADOR
    st.markdown("---")
    
    # NUEVA SECCIÓN DE BOTONES MÁGICOS MEJORADA
    st.markdown("""
    <div class="magic-buttons-container">
        <div class="magic-buttons-title">⚡ Botones Mágicos</div>
    </div>
    """, unsafe_allow_html=True)
    
    # BOTONES MÁGICOS CON DISEÑO MEJORADO (LOS MISMOS BOTONES FUNCIONALES)
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        if st.button("🚀 **Activar Poderes**", key="start", use_container_width=True):
            if st.session_state.proc is None:
                st.session_state.proc = subprocess.Popen(
                    [sys.executable, "app/camera.py", mode_arg]
                )
                st.success(f"¡Magia activada! Modo: {mode} ✨")
                st.balloons()
            else:
                st.info("¡Tus poderes ya están activos! 🦸")
    
    with col_btn2:
        if st.button("⏹️ **Pausar Magia**", key="stop", use_container_width=True):
            if st.session_state.proc is not None:
                st.session_state.proc.terminate()
                st.session_state.proc = None
                st.success("Magia pausada. ¡Descansa! 😴")
            else:
                st.info("No hay magia activa en este momento")
    
    with col_btn3:
        if st.button("🔄 **Reiniciar Todo**", key="restart", use_container_width=True):
            st.session_state.proc = None
            st.rerun()

# =============================================
# PESTAÑA 2: MUNDO DE JUEGOS (MANTENIDO)
# =============================================
with tab2:
    st.markdown("## 🎮 Mundo de Juegos Mágicos")
    st.markdown("### ¡Elige tu juego favorito y controla con gestos! 🎯")
    
    # TRES COLUMNAS PARA JUEGOS
    col_juego1, col_juego2, col_juego3 = st.columns(3)
    
    with col_juego1:
        st.markdown("""
        <div class="game-card">
            <div style="font-size: 3rem;">🎪</div>
            <h3>Playland & Gestos</h3>
            <p>¡Un mundo donde tus gestos crean magia! Aprende mientras juegas con movimientos naturales.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Cómo jugar:**")
        col1a, col1b = st.columns([0.15, 0.85])
        with col1a:
            st.markdown('<div class="step-badge">1</div>', unsafe_allow_html=True)
        with col1b:
            st.markdown("Selecciona modo Juego")
            st.caption("Elige Playland en los controles")
        
        col2a, col2b = st.columns([0.15, 0.85])
        with col2a:
            st.markdown('<div class="step-badge">2</div>', unsafe_allow_html=True)
        with col2b:
            st.markdown("Activa control gestual")
            st.caption("En la Casa Mágica")
        
        col3a, col3b = st.columns([0.15, 0.85])
        with col3a:
            st.markdown('<div class="step-badge">3</div>', unsafe_allow_html=True)
        with col3b:
            st.markdown("¡A jugar con gestos!")
            st.caption("Comienza tu aventura")
    
    with col_juego2:
        st.markdown("""
        <div class="game-card">
            <div style="font-size: 3rem;">🔺</div>
            <h3>Shapes Match</h3>
            <p>Combina formas y colores con movimientos mágicos. Desarrolla tu reconocimiento espacial.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Cómo jugar:**")
        col1a, col1b = st.columns([0.15, 0.85])
        with col1a:
            st.markdown('<div class="step-badge">1</div>', unsafe_allow_html=True)
        with col1b:
            st.markdown("Elige Shapes Match")
            st.caption("En el menú de juegos")
        
        col2a, col2b = st.columns([0.15, 0.85])
        with col2a:
            st.markdown('<div class="step-badge">2</div>', unsafe_allow_html=True)
        with col2b:
            st.markdown("Aprende gestos")
            st.caption("Asocia movimientos a acciones")
        
        col3a, col3b = st.columns([0.15, 0.85])
        with col3a:
            st.markdown('<div class="step-badge">3</div>', unsafe_allow_html=True)
        with col3b:
            st.markdown("Combina formas")
            st.caption("Resuelve puzzles mágicos")
    
    with col_juego3:
        st.markdown("""
        <div class="game-card">
            <div style="font-size: 3rem;">🎨</div>
            <h3>Color Match</h3>
            <p>Domina el arte del color con gestos intuitivos. Mejora tu coordinación y memoria visual.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Cómo jugar:**")
        col1a, col1b = st.columns([0.15, 0.85])
        with col1a:
            st.markdown('<div class="step-badge">1</div>', unsafe_allow_html=True)
        with col1b:
            st.markdown("Selecciona Color Match")
            st.caption("Desde esta sección")
        
        col2a, col2b = st.columns([0.15, 0.85])
        with col2a:
            st.markdown('<div class="step-badge">2</div>', unsafe_allow_html=True)
        with col2b:
            st.markdown("Domina gestos de color")
            st.caption("Para selección y combinación")
        
        col3a, col3b = st.columns([0.15, 0.85])
        with col3a:
            st.markdown('<div class="step-badge">3</div>', unsafe_allow_html=True)
        with col3b:
            st.markdown("Crea obras maestras")
            st.caption("Forma paletas de colores")

# =============================================
# PESTAÑA 3: TABLERO MÁGICO (DASHBOARD)
# =============================================
with tab3:
    st.markdown("## 📊 Tablero Mágico de Progreso")
    st.markdown("### ¡Mira lo increíble que te estás volviendo! 🌟")
    
    # CÓDIGO ORIGINAL DEL DASHBOARD
    path = os.path.join("data", "colors_sessions.json")
    if not os.path.exists(path):
        st.info("🎯 ¡Aún no hay aventuras registradas! Juega primero para ver tu progreso mágico.")
    else:
        try:
            data = json.load(open(path, "r", encoding="utf-8"))
        except json.JSONDecodeError:
            st.error("¡Ups! El archivo mágico está dañado. Los duendes lo arreglarán pronto.")
        else:
            if not data:
                st.info("📝 Comienza tu aventura mágica para llenar este tablero")
            else:
                df = pd.DataFrame(data)
                
                # MÉTRICAS PRINCIPALES
                col_met1, col_met2, col_met3 = st.columns(3)
                
                with col_met1:
                    st.markdown("""
                    <div class="metric-card">
                        <h3>🎯 Aventuras</h3>
                        <h2 style="color: #8A2BE2; font-size: 2.5rem;">{}</h2>
                        <p>Sesiones completadas</p>
                    </div>
                    """.format(len(df)), unsafe_allow_html=True)
                
                with col_met2:
                    avg_accuracy = df['accuracy'].mean() * 100
                    st.markdown("""
                    <div class="metric-card">
                        <h3>⭐ Magia</h3>
                        <h2 style="color: #8A2BE2; font-size: 2.5rem;">{:.1f}%</h2>
                        <p>Precisión promedio</p>
                    </div>
                    """.format(avg_accuracy), unsafe_allow_html=True)
                
                with col_met3:
                    avg_score = df['score'].mean()
                    st.markdown("""
                    <div class="metric-card">
                        <h3>🏆 Puntos</h3>
                        <h2 style="color: #8A2BE2; font-size: 2.5rem;">{:.1f}</h2>
                        <p>Puntaje promedio</p>
                    </div>
                    """.format(avg_score), unsafe_allow_html=True)
    
    # INFORMACIÓN ADICIONAL
    st.markdown("---")
    st.markdown("### 🎨 Tu Camino Mágico")
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown("""
        <div class="kids-card">
            <h4>🎪 Niveles de Poder</h4>
            <p>• <strong>Aprendiz Mágico:</strong> 0-50 puntos</p>
            <p>• <strong>Mago Gestual:</strong> 51-80 puntos</p>
            <p>• <strong>Archimago Supremo:</strong> 81-100 puntos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_info2:
        st.markdown("""
        <div class="kids-card">
            <h4>🌟 Logros por Desbloquear</h4>
            <p>• <strong>Primeros Pasos:</strong> Completa 1 juego</p>
            <p>• <strong>Gestos Mágicos:</strong> 75% de precisión</p>
            <p>• <strong>Maestro Gestual:</strong> 5 sesiones completadas</p>
        </div>
        """, unsafe_allow_html=True)

# =============================================
# FOOTER INFANTIL
# =============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: rgba(255, 255, 255, 0.8); border-radius: 20px; margin-top: 3rem;">
    <div style="font-size: 1.5rem; color: #8A2BE2; margin-bottom: 0.5rem;">
        ✨ EduMotion - ¡Donde los Gestos son Magia! ✨
    </div>
    <div style="color: #888; font-size: 1rem;">
        Para niños super inteligentes y creativos como tú 🦸‍♀️
    </div>
    <div style="margin-top: 1rem; font-size: 0.9rem; color: #999;">
        Hecho con ❤️ para hacer el aprendizaje divertido
    </div>
</div>
""", unsafe_allow_html=True)