import os
import re
import urllib.parse
import streamlit as st
import pandas as pd
import numpy as np

# Intentamos importar extractor.py si existe
try:
    from extractor import extract_features_from_url
except ImportError:
    # Definición de respaldo si el archivo se mueve
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

# Intento de carga de joblib
try:
    import joblib
except ImportError:
    joblib = None

# ==============================================================================
# ⚙️ CONFIGURACIÓN DE PÁGINA STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="PhishGuard AI - Detector de Phishing",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 🎨 ESTILOS PERSONALIZADOS (CSS MODERNO Y CYBERSECURITY AESTHETICS)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Fondo principal y tarjetas */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(13, 27, 42, 0.95) 0%, rgba(10, 15, 29, 0.98) 90%);
        color: #f1f5f9;
    }
    
    /* Header hero */
    .hero-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(12px);
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 15px;
    }
    
    .badge-authors {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.88rem;
        color: #38bdf8;
        font-weight: 600;
    }

    /* Tarjetas de Veredicto */
    .verdict-card {
        border-radius: 16px;
        padding: 24px;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease;
    }
    
    .verdict-safe {
        background: linear-gradient(135deg, rgba(6, 78, 59, 0.4) 0%, rgba(4, 120, 87, 0.2) 100%);
        border: 2px solid #10b981;
    }
    
    .verdict-danger {
        background: linear-gradient(135deg, rgba(127, 29, 29, 0.4) 0%, rgba(185, 28, 28, 0.2) 100%);
        border: 2px solid #ef4444;
    }
    
    .verdict-warning {
        background: linear-gradient(135deg, rgba(120, 53, 15, 0.4) 0%, rgba(180, 83, 9, 0.2) 100%);
        border: 2px solid #f59e0b;
    }
    
    /* Tarjetas de métricas y diagnóstico */
    .metric-box {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #38bdf8;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-top: 4px;
    }
    
    /* Footer */
    .custom-footer {
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        color: #64748b;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 🤖 CARGA DEL MODELO DE MACHINE LEARNING
# ==============================================================================
# INSTRUCCIÓN PARA COMPAÑEROS DE EQUIPO:
# Cuando el notebook termine de entrenar y exporte 'modelo_phishing.pkl' o
# 'modelo_lr_phishing.pkl', el modelo se cargará automáticamente aquí abajo.
@st.cache_resource(show_spinner=False)
def load_trained_model():
    model_paths = [
        "modelo_phishing.pkl",
        "modelo_lr_phishing.pkl",
        "modelo_rf_phishing.pkl"
    ]
    for path in model_paths:
        if os.path.exists(path) and joblib is not None:
            try:
                pipeline = joblib.load(path)
                return pipeline, path
            except Exception as e:
                st.sidebar.error(f"Error al cargar {path}: {e}")
    return None, None

pipeline_model, model_loaded_name = load_trained_model()

# ==============================================================================
# 🛡️ SIDEBAR: INFORMACIÓN, POLÍTICA DE SEGURIDAD Y PRIVACIDAD
# ==============================================================================
with st.sidebar:
    st.markdown("### 🛡️ **PhishGuard AI**")
    st.caption("Sistema de Inteligencia Artificial para Detección de Amenazas Web")
    
    st.markdown("---")
    
    # Estado del modelo
    st.markdown("#### 🧠 Estado del Modelo")
    if pipeline_model is not None:
        st.success(f"🟢 **Modelo Activo:** `{model_loaded_name}`")
        st.info("Pipeline completo cargado con preprocesamiento y Scikit-Learn.")
    else:
        st.warning("🟡 **Modo Demostración / Heurístico**")
        st.caption("No se encontró `modelo_phishing.pkl`. El sistema está usando el extractor léxico con análisis heurístico de respaldo hasta que se ejecute el entrenamiento.")

    st.markdown("---")
    
    # Autores
    st.markdown("#### 👥 Equipo de Desarrollo")
    st.markdown("""
    * **Alejandro Flores**
    * **Paul Rosero**
    * **Gloria Chassi**
    """)
    st.caption("Proyecto de Inteligencia Artificial - Semestre 6")
    
    st.markdown("---")
    
    # Términos, Cookies y Privacidad
    with st.expander("⚖️ Términos, Privacidad y Cookies"):
        st.markdown("""
        **1. Aviso de Cookies y Sesión:**
        Esta aplicación utiliza almacenamiento de sesión volátil temporal exclusivamente para mantener el estado de la URL analizada durante la interacción del usuario. No se emplean cookies de rastreo publicitario.
        
        **2. Tratamiento de Datos:**
        Las URLs ingresadas son analizadas únicamente en memoria con fines de extracción de características léxicas. No se almacenan contraseñas ni credenciales personales.
        
        **3. Marco de Seguridad y Ciberseguridad:**
        Esta herramienta es un prototipo con fines de auditoría preventiva y académicos. Las predicciones se basan en modelos probabilísticos y no sustituyen una suite de ciberseguridad perimetral (antivirus, firewall o DNS sinkhole).
        """)

# ==============================================================================
# 🌟 HERO SECTION & ENCABEZADO
# ==============================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🛡️ Detector de Phishing en URLs con IA</div>
    <div class="hero-subtitle">
        Clasificación y análisis de ciberseguridad en tiempo real mediante Machine Learning y extracción léxica avanzada.
    </div>
    <div class="badge-authors">
        <span>👨‍💻 Autores: Alejandro Flores • Paul Rosero • Gloria Chassi</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 🎯 ENTRADA DE DATOS Y BOTONES DE PRUEBA RÁPIDA
# ==============================================================================
st.markdown("### 🔍 Analizar una Dirección Web (URL)")
st.write("Ingresa una URL completa para extraer sus métricas léxicas y predecir su nivel de riesgo de phishing.")

# URLs de ejemplo
col_ex1, col_ex2, col_ex3, col_ex4 = st.columns(4)

if "url_input_value" not in st.session_state:
    st.session_state["url_input_value"] = "http://banco-pichincha-seguridad-login.net/actualizar-datos.php?id=82931"

with col_ex1:
    if st.button("🧪 Ejemplo: Phishing Bancario", use_container_width=True):
        st.session_state["url_input_value"] = "http://banco-pichincha-seguridad-login.net/actualizar-datos.php?id=82931"

with col_ex2:
    if st.button("🧪 Ejemplo: Phishing con IP", use_container_width=True):
        st.session_state["url_input_value"] = "http://192.168.1.105/paypal/signin/verification.php"

with col_ex3:
    if st.button("✅ Ejemplo: Google (Seguro)", use_container_width=True):
        st.session_state["url_input_value"] = "https://www.google.com/search?q=machine+learning"

with col_ex4:
    if st.button("✅ Ejemplo: GitHub (Seguro)", use_container_width=True):
        st.session_state["url_input_value"] = "https://github.com/alex171215/Detector-Phishing-ML"

# Campo de texto para la URL
url_input = st.text_input(
    "Dirección URL a inspeccionar:",
    value=st.session_state["url_input_value"],
    placeholder="https://ejemplo.com/login...",
    help="Ingresa el enlace que deseas verificar"
)

btn_analyze = st.button("🚀 Analizar Seguridad de la URL", type="primary", use_container_width=True)

# ==============================================================================
# 📊 LÓGICA DE INFERENCIA Y EXTRACCIÓN
# ==============================================================================
if btn_analyze or url_input:
    if not url_input.strip():
        st.warning("⚠️ Por favor ingresa una URL válida para analizar.")
    else:
        # 1. Extracción de características
        df_features = extract_features_from_url(url_input.strip())
        
        parsed = urllib.parse.urlparse(url_input.strip())
        is_https = (parsed.scheme.lower() == 'https')
        is_ip = bool(re.match(r'^[0-9]+(?:\.[0-9]+){3}$', parsed.netloc))
        url_len = len(url_input.strip())
        suspicious_words = ["login", "verify", "secure", "account", "update", "bank", "banco", "pago", "free", "bonus", "signin"]
        found_keywords = [w for w in suspicious_words if w in url_input.lower()]
        
        # 2. Predicción (vía Modelo o Heurística de Respaldo)
        if pipeline_model is not None:
            try:
                # =========================================================================
                # 🤖 CONEXIÓN DEL MODELO OFICIAL
                # Predice usando el Pipeline de Scikit-Learn entrenado
                # =========================================================================
                prob_phishing = float(pipeline_model.predict_proba(df_features)[0][1])
                pred_label = int(prob_phishing >= 0.5)
            except Exception as err:
                st.error(f"Error al ejecutar el pipeline del modelo: {err}")
                prob_phishing = 0.5
                pred_label = 0
        else:
            # Heurística didáctica de respaldo para visualización interactiva
            risk_score = 10
            if not is_https: risk_score += 25
            if is_ip: risk_score += 35
            if url_len > 60: risk_score += 15
            if len(found_keywords) > 0: risk_score += len(found_keywords) * 15
            if df_features.get('special_char_count', [0])[0] > 10: risk_score += 10
            
            prob_phishing = min(max(risk_score / 100.0, 0.02), 0.99)
            pred_label = 1 if prob_phishing >= 0.5 else 0

        # ==============================================================================
        # 🚦 PANEL DE RESULTADOS Y VEREDICTO VISUAL
        # ==============================================================================
        st.markdown("---")
        st.markdown("## 📊 Diagnóstico de Amenaza")
        
        col_res1, col_res2 = st.columns([1.2, 1])
        
        with col_res1:
            if pred_label == 1 or prob_phishing >= 0.5:
                st.markdown(f"""
                <div class="verdict-card verdict-danger">
                    <h2 style="color: #ef4444; margin:0;">🚨 PELIGRO: Alta Probabilidad de Phishing</h2>
                    <p style="color: #fca5a5; font-size: 1.1rem; margin-top: 8px;">
                        Esta URL presenta patrones característicos de páginas fraudulentas diseñadas para suplantación de identidad o robo de credenciales.
                    </p>
                    <hr style="border-color: rgba(239, 68, 68, 0.3);">
                    <h3 style="color: #ffffff; margin-bottom: 0;">Probabilidad de Amenaza: <strong>{prob_phishing * 100:.1f}%</strong></h3>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="verdict-card verdict-safe">
                    <h2 style="color: #10b981; margin:0;">✅ SITIO SEGURO: URL Benigna</h2>
                    <p style="color: #a7f3d0; font-size: 1.1rem; margin-top: 8px;">
                        La estructura léxica y el dominio de esta dirección corresponden a patrones legítimos y seguros.
                    </p>
                    <hr style="border-color: rgba(16, 185, 129, 0.3);">
                    <h3 style="color: #ffffff; margin-bottom: 0;">Probabilidad de Seguridad: <strong>{(1 - prob_phishing) * 100:.1f}%</strong></h3>
                </div>
                """, unsafe_allow_html=True)
                
            # Barra de progreso estilizada
            st.write("**Nivel de Riesgo Calculado:**")
            st.progress(prob_phishing)
        
        with col_res2:
            st.markdown("#### 🔍 Desglose Rápido de Señales")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-value">{'🔒 HTTPS' if is_https else '🔓 HTTP Inseguro'}</div>
                    <div class="metric-label">Protocolo Web</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-value">{'⚠️ Dirección IP' if is_ip else '🌐 Dominio DNS'}</div>
                    <div class="metric-label">Tipo de Host</div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            c3, c4 = st.columns(2)
            with c3:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-value">{url_len} caracteres</div>
                    <div class="metric-label">Longitud de URL</div>
                </div>
                """, unsafe_allow_html=True)
            with c4:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-value">{len(found_keywords)} detectadas</div>
                    <div class="metric-label">Palabras Sensibles</div>
                </div>
                """, unsafe_allow_html=True)

        # ==============================================================================
        # 📋 TABLA DE CARACTERÍSTICAS EXTRAÍDAS
        # ==============================================================================
        st.markdown("### 🧬 Variables Léxicas Extraídas por el Sistema")
        st.caption("Estas son las columnas y métricas matemáticas que alimentan el Pipeline de Machine Learning:")
        
        st.dataframe(df_features, use_container_width=True)
        
        # Consejos de seguridad
        with st.expander("💡 Recomendaciones de Seguridad para el Usuario"):
            st.markdown("""
            * **Verifica el dominio exacto:** Desconfía de dominios con faltas ortográficas sutiles (ej. `paypa1.com` en lugar de `paypal.com`).
            * **No ingreses credenciales bajo HTTP:** Los sitios legítimos que solicitan contraseñas o datos bancarios siempre emplean cifrado HTTPS.
            * **Cuidado con direcciones IP directas:** Muy rara vez un servicio web seguro solicita iniciar sesión utilizando una IP numérica como `http://192.168.1.1/...`.
            """)

# ==============================================================================
# 📜 PIE DE PÁGINA
# ==============================================================================
st.markdown("""
<div class="custom-footer">
    <p><strong>PhishGuard AI</strong> • Proyecto de Detección de Phishing con Machine Learning</p>
    <p>Desarrollado por: <strong>Alejandro Flores</strong> • <strong>Paul Rosero</strong> • <strong>Gloria Chassi</strong></p>
    <p>© 2026 - Todos los derechos reservados. Aplicación con fines académicos y de investigación en ciberseguridad.</p>
</div>
""", unsafe_allow_html=True)
