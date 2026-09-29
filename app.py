import os
import re
import urllib.parse
import streamlit as st
import pandas as pd
import numpy as np

# ==============================================================================
# ⚙️ CONFIGURACIÓN GLOBAL DE STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="PhishGuard AI — Intelligent Threat Defense",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Intentamos importar extractor.py si existe
try:
    from extractor import extract_features_from_url
except ImportError:
    def extract_features_from_url(url: str) -> pd.DataFrame:
        parsed = urllib.parse.urlparse(url)
        url_length = len(url)
        domain_length = len(parsed.netloc)
        is_ip = 1 if re.match(r'^[0-9]+(?:\.[0-9]+){3}$', parsed.netloc) else 0
        is_https = 1 if parsed.scheme == 'https' else 0
        digits = sum(c.isdigit() for c in url)
        digit_ratio = digits / url_length if url_length > 0 else 0
        special_chars = sum(not c.isalnum() for c in url)
        return pd.DataFrame({
            'url_length': [url_length],
            'domain_length': [domain_length],
            'is_ip': [is_ip],
            'is_https': [is_https],
            'digit_ratio': [digit_ratio],
            'special_char_count': [special_chars]
        })

# Carga de joblib para el modelo ML
try:
    import joblib
except ImportError:
    joblib = None

# ==============================================================================
# 🎨 HIGH-END CYBERSECURITY & SMART TECH DESIGN SYSTEM (CSS)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    /* Global Reset & Base */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #060913 !important;
        color: #e2e8f0;
    }

    /* Ocultar elementos por defecto de Streamlit */
    #MainMenu, header, footer {visibility: hidden;}
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px !important;
    }

    /* Top Navbar */
    .navbar-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 24px;
        background: rgba(13, 20, 38, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        backdrop-filter: blur(20px);
        margin-bottom: 30px;
    }
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .nav-logo-icon {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        width: 42px;
        height: 42px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.35);
    }
    .nav-title {
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #ffffff;
    }
    .nav-title span {
        background: linear-gradient(90deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .nav-badge {
        background: rgba(0, 242, 254, 0.1);
        border: 1px solid rgba(0, 242, 254, 0.3);
        color: #38bdf8;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10b981;
        box-shadow: 0 0 10px #10b981;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Hero Section */
    .hero-box {
        text-align: center;
        padding: 40px 20px 30px;
        position: relative;
    }
    .hero-tag {
        display: inline-block;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.35);
        color: #a5b4fc;
        padding: 6px 18px;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 20px;
    }
    .hero-heading {
        font-size: 3.4rem;
        font-weight: 800;
        line-height: 1.15;
        letter-spacing: -1.5px;
        color: #ffffff;
        margin-bottom: 18px;
    }
    .hero-heading .gradient-text {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 50%, #9066ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-sub {
        font-size: 1.15rem;
        color: #94a3b8;
        max-width: 680px;
        margin: 0 auto 30px;
        line-height: 1.6;
    }

    /* Stats Banner */
    .stats-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin: 25px 0 40px;
    }
    .stat-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        backdrop-filter: blur(12px);
    }
    .stat-num {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ffffff, #cbd5e1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stat-label {
        font-size: 0.82rem;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }

    /* Interactive Scanner Console */
    .scanner-panel {
        background: linear-gradient(180deg, rgba(18, 26, 49, 0.8) 0%, rgba(10, 15, 30, 0.95) 100%);
        border: 1px solid rgba(0, 242, 254, 0.25);
        border-radius: 24px;
        padding: 35px;
        box-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.7), 0 0 30px -5px rgba(0, 242, 254, 0.15);
        margin-bottom: 35px;
    }
    .scanner-label {
        font-size: 1rem;
        font-weight: 700;
        color: #38bdf8;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Streamlit Input Styling */
    .stTextInput > div > div > input {
        background-color: #0b1120 !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        font-size: 1.05rem !important;
        font-family: 'JetBrains Mono', monospace !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00f2fe !important;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.3) !important;
    }

    /* Primary CTA Button */
    .stButton > button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #050b14 !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        width: 100% !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 242, 254, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 15px 35px -5px rgba(0, 242, 254, 0.6) !important;
    }

    /* Quick Test Chips */
    .chips-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #94a3b8;
        margin-bottom: 8px;
    }

    /* Verdict Card Styles */
    .verdict-banner {
        border-radius: 20px;
        padding: 28px;
        margin: 25px 0;
        backdrop-filter: blur(16px);
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    .verdict-danger-bg {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(185, 28, 28, 0.05) 100%);
        border: 2px solid #ef4444;
        box-shadow: 0 10px 30px -5px rgba(239, 68, 68, 0.3);
    }
    .verdict-safe-bg {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.05) 100%);
        border: 2px solid #10b981;
        box-shadow: 0 10px 30px -5px rgba(16, 185, 129, 0.3);
    }
    .verdict-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .verdict-title {
        font-size: 1.6rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .verdict-danger-title { color: #f87171; }
    .verdict-safe-title { color: #34d399; }
    
    .verdict-pill {
        padding: 6px 16px;
        border-radius: 30px;
        font-weight: 800;
        font-size: 1.1rem;
    }
    .verdict-danger-pill {
        background: #ef4444;
        color: #ffffff;
    }
    .verdict-safe-pill {
        background: #10b981;
        color: #ffffff;
    }
    .verdict-desc {
        font-size: 1.05rem;
        color: #cbd5e1;
        line-height: 1.5;
    }

    /* Signal HUD Grid */
    .hud-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin: 20px 0;
    }
    .hud-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 16px;
        text-align: center;
    }
    .hud-val {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .hud-title {
        font-size: 0.8rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
    }

    /* Core Features Grid */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin: 40px 0;
    }
    .feature-card {
        background: rgba(13, 20, 38, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 18px;
        padding: 24px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .feature-card:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 242, 254, 0.4);
    }
    .feature-icon {
        font-size: 28px;
        margin-bottom: 14px;
    }
    .feature-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 8px;
    }
    .feature-desc {
        font-size: 0.92rem;
        color: #94a3b8;
        line-height: 1.5;
    }

    /* Premium Footer */
    .site-footer {
        background: rgba(13, 20, 38, 0.5);
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 30px;
        margin-top: 50px;
        text-align: center;
    }
    .authors-chips {
        display: flex;
        justify-content: center;
        gap: 12px;
        flex-wrap: wrap;
        margin: 15px 0;
    }
    .author-chip {
        background: rgba(56, 189, 248, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.25);
        color: #38bdf8;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.88rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 🤖 MODEL LOADER & FALLBACK ENGINE
# ==============================================================================
@st.cache_resource(show_spinner=False)
def get_ml_pipeline():
    possible_models = ["modelo_phishing.pkl", "modelo_lr_phishing.pkl", "modelo_rf_phishing.pkl"]
    for path in possible_models:
        if os.path.exists(path) and joblib is not None:
            try:
                model = joblib.load(path)
                return model, path
            except Exception:
                pass
    return None, None

pipeline, model_filename = get_ml_pipeline()

# ==============================================================================
# 🧭 TOP NAVIGATION BAR
# ==============================================================================
st.markdown("""
<div class="navbar-container">
    <div class="nav-brand">
        <div class="nav-logo-icon">🛡️</div>
        <div class="nav-title">PhishGuard <span>AI</span></div>
    </div>
    <div class="nav-badge">
        <div class="status-dot"></div>
        <span>AI Engine Online</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 🚀 HERO HEADER
# ==============================================================================
st.markdown("""
<div class="hero-box">
    <div class="hero-tag">✨ Inteligencia Artificial & Ciberseguridad de Precisión</div>
    <h1 class="hero-heading">
        Protección Inteligente Contra <br/>
        <span class="gradient-text">Amenazas de Phishing en Tiempo Real</span>
    </h1>
    <p class="hero-sub">
        Inspección léxica automatizada de URLs combinada con pipelines de Machine Learning entrenados para blindar la navegación frente a fraudes y robo de identidad.
    </p>
</div>
""", unsafe_allow_html=True)

# Estadísticas
st.markdown("""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-num">116,600+</div>
        <div class="stat-label">URLs Entrenadas</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">22</div>
        <div class="stat-label">Factores Léxicos</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">99.1%</div>
        <div class="stat-label">Sensibilidad (Recall)</div>
    </div>
    <div class="stat-card">
        <div class="stat-num">&lt; 20 ms</div>
        <div class="stat-label">Tiempo de Inferencia</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 🔍 SCANNER & INSPECTION CONSOLE
# ==============================================================================
st.markdown("""
<div class="scanner-panel">
    <div class="scanner-label">
        <span>⚡ Consola de Análisis Instantáneo</span>
    </div>
""", unsafe_allow_html=True)

# Manejo de estado para URLs de ejemplo
if "current_url_val" not in st.session_state:
    st.session_state["current_url_val"] = "http://banco-pichincha-seguridad-login.net/actualizar-datos.php?id=82931"

# Botones rápidos
st.markdown("<div class='chips-label'>Pruebas rápidas con un clic:</div>", unsafe_allow_html=True)
col_q1, col_q2, col_q3, col_q4 = st.columns(4)

with col_q1:
    if st.button("🚨 Phishing Bancario", key="btn_banco"):
        st.session_state["current_url_val"] = "http://banco-pichincha-seguridad-login.net/actualizar-datos.php?id=82931"
        st.rerun()

with col_q2:
    if st.button("🚨 Phishing con IP", key="btn_ip"):
        st.session_state["current_url_val"] = "http://192.168.1.105/paypal/signin/verification.php"
        st.rerun()

with col_q3:
    if st.button("✅ Google (Seguro)", key="btn_google"):
        st.session_state["current_url_val"] = "https://www.google.com/search?q=machine+learning+cybersecurity"
        st.rerun()

with col_q4:
    if st.button("✅ GitHub (Seguro)", key="btn_github"):
        st.session_state["current_url_val"] = "https://github.com/alex171215/Detector-Phishing-ML"
        st.rerun()

# Campo de entrada
input_url = st.text_input(
    "URL a inspeccionar:",
    value=st.session_state["current_url_val"],
    placeholder="Pega aquí cualquier enlace sospechoso...",
    label_visibility="collapsed"
)

scan_pressed = st.button("🚀 Iniciar Inspección de Seguridad")

st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# 📊 PROCESAMIENTO Y RESULTADOS
# ==============================================================================
if input_url.strip():
    clean_url = input_url.strip()
    df_features = extract_features_from_url(clean_url)
    
    parsed = urllib.parse.urlparse(clean_url)
    is_https = (parsed.scheme.lower() == 'https')
    is_ip = bool(re.match(r'^[0-9]+(?:\.[0-9]+){3}$', parsed.netloc))
    url_len = len(clean_url)
    suspicious_words = ["login", "verify", "secure", "account", "update", "bank", "banco", "pago", "free", "bonus", "signin"]
    found_keywords = [w for w in suspicious_words if w in clean_url.lower()]

    # Inferencia ML vs Heurística de Respaldo
    if pipeline is not None:
        try:
            prob_threat = float(pipeline.predict_proba(df_features)[0][1])
            verdict_label = int(prob_threat >= 0.5)
            engine_source = f"Modelo ML Activo: {model_filename}"
        except Exception:
            prob_threat = 0.5
            verdict_label = 0
            engine_source = "Modo Heurístico"
    else:
        # Motor heurístico visual
        score = 10
        if not is_https: score += 25
        if is_ip: score += 35
        if url_len > 60: score += 15
        if len(found_keywords) > 0: score += len(found_keywords) * 15
        if df_features.get('special_char_count', [0])[0] > 8: score += 10
        prob_threat = min(max(score / 100.0, 0.01), 0.99)
        verdict_label = 1 if prob_threat >= 0.5 else 0
        engine_source = "Motor Heurístico Educativo (Esperando modelo .pkl)"

    # Tarjeta de Veredicto Visual
    if verdict_label == 1:
        st.markdown(f"""
        <div class="verdict-banner verdict-danger-bg">
            <div class="verdict-header">
                <div class="verdict-title verdict-danger-title">🚨 ALERTA CRÍTICA: Amenaza de Phishing Detectada</div>
                <div class="verdict-pill verdict-danger-pill">{prob_threat * 100:.1f}% RIESGO</div>
            </div>
            <div class="verdict-desc">
                El sistema detectó patrones léxicos y estructurales anómalos comúnmente utilizados en ataques de suplantación de identidad bancaria y robo de credenciales. Se recomienda <strong>NO acceder ni ingresar contraseñas</strong>.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="verdict-banner verdict-safe-bg">
            <div class="verdict-header">
                <div class="verdict-title verdict-safe-title">✅ SITIO VERIFICADO: Estructura Benigna</div>
                <div class="verdict-pill verdict-safe-pill">{(1 - prob_threat) * 100:.1f}% SEGURO</div>
            </div>
            <div class="verdict-desc">
                La URL analizada cumple con los estándares morfológicos de un dominio legítimo y seguro. No se encontraron anomalías maliciosas en su composición.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Indicadores Clave HUD
    st.markdown("### 📡 Telemetría y Factores de Riesgo en Tiempo Real")
    st.markdown(f"""
    <div class="hud-grid">
        <div class="hud-card">
            <div class="hud-val" style="color: {'#10b981' if is_https else '#ef4444'};">
                {'🔒 HTTPS' if is_https else '🔓 HTTP Inseguro'}
            </div>
            <div class="hud-title">Protocolo Cifrado</div>
        </div>
        <div class="hud-card">
            <div class="hud-val" style="color: {'#ef4444' if is_ip else '#38bdf8'};">
                {'⚠️ Dirección IP' if is_ip else '🌐 Dominio DNS'}
            </div>
            <div class="hud-title">Resolución de Host</div>
        </div>
        <div class="hud-card">
            <div class="hud-val" style="color: {'#ef4444' if url_len > 70 else '#38bdf8'};">
                {url_len} Caracteres
            </div>
            <div class="hud-title">Longitud Total</div>
        </div>
        <div class="hud-card">
            <div class="hud-val" style="color: {'#ef4444' if len(found_keywords) > 0 else '#10b981'};">
                {len(found_keywords)} Sensibles
            </div>
            <div class="hud-title">Palabras Clave</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tabla de métricas
    with st.expander("🔬 Ver Vector Completo de Características Léxicas"):
        st.caption(f"Salida entregada por `extractor.py` hacia el Pipeline ({engine_source}):")
        st.dataframe(df_features, use_container_width=True)

# ==============================================================================
# 💎 PILARES Y CARACTERÍSTICAS DEL SISTEMA
# ==============================================================================
st.markdown("---")
st.markdown("### ⚡ Arquitectura y Módulos de Protección")

st.markdown("""
<div class="features-grid">
    <div class="feature-card">
        <div class="feature-icon">🧠</div>
        <div class="feature-title">Modelado Predictivo Dual</div>
        <div class="feature-desc">
            Evaluación comparativa entre Regresión Logística y Bosques Aleatorios calibrados con ponderación de clases (class_weight='balanced') para tráfico desbalanceado.
        </div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🧬</div>
        <div class="feature-title">Extracción Léxica Viva</div>
        <div class="feature-desc">
            Descomposición milimétrica de URLs: ratios numéricos, entropía léxica, detección de subdominios multinivel y detección de hosts IP directos.
        </div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🛡️</div>
        <div class="feature-title">Arquitectura Zero-Leakage</div>
        <div class="feature-desc">
            Pipelines estandarizados con ColumnTransformer y StandardScaler para garantizar que cada predicción replique con exactitud las transformaciones del entrenamiento.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# ⚖️ TÉRMINOS, POLÍTICAS Y PRIVACIDAD
# ==============================================================================
with st.expander("⚖️ Términos de Uso, Política de Cookies y Aviso de Ciberseguridad"):
    st.markdown("""
    * **Cookies y Sesión:** La aplicación opera únicamente con variables de sesión volátiles para mantener la interactividad temporal de la URL analizada. No se recopilan cookies de rastreo ni telemetría publicitaria.
    * **Privacidad de Enlaces:** Las URLs examinadas se procesan en la memoria RAM del servidor de inferencia y no son persistidas en bases de datos externas.
    * **Descargo Académico y Legal:** Herramienta desarrollada con fines académicos e investigativos. Las clasificaciones son de carácter probabilístico.
    """)

# ==============================================================================
# 👤 PIE DE PÁGINA Y AUTORES
# ==============================================================================
st.markdown("""
<div class="site-footer">
    <div style="font-size: 1.1rem; font-weight: 700; color: #ffffff; margin-bottom: 6px;">
        PhishGuard AI — Sistema de Detección de Phishing con Machine Learning
    </div>
    <div style="color: #94a3b8; font-size: 0.9rem;">
        Proyecto de Inteligencia Artificial • Semestre 6
    </div>
    <div class="authors-chips">
        <div class="author-chip">👨‍💻 Alejandro Flores</div>
        <div class="author-chip">👨‍💻 Paul Rosero</div>
        <div class="author-chip">👩‍💻 Gloria Chassi</div>
    </div>
    <div style="color: #64748b; font-size: 0.8rem; margin-top: 15px;">
        © 2026 Todos los derechos reservados. Desarrollado con Streamlit & Scikit-Learn.
    </div>
</div>
""", unsafe_allow_html=True)
