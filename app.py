import os
import re
import html as htmllib
import urllib.parse
import streamlit as st
import pandas as pd

# ==============================================================================
# CONFIGURACIÓN DE PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Detector gratuito de Phishing | PhishGuard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Control de navegación mediante Query Params
current_page = st.query_params.get("page", "analizar")
if isinstance(current_page, list):
    current_page = current_page[0]
if current_page not in ("analizar", "modelos", "ayuda"):
    current_page = "analizar"

# ==============================================================================
# 🧬 EXTRACTOR DE CARACTERÍSTICAS LÉXICAS
# (Compatible con extractor.py del proyecto)
# ==============================================================================
try:
    from extractor import extract_features_from_url
except ImportError:
    def extract_features_from_url(url: str) -> pd.DataFrame:
        p = urllib.parse.urlparse(url)
        n = len(url)
        return pd.DataFrame({
            "url_length": [n],
            "domain_length": [len(p.netloc)],
            "is_ip": [1 if re.match(r"^[0-9]+(?:\.[0-9]+){3}$", p.netloc) else 0],
            "is_https": [1 if p.scheme == "https" else 0],
            "digit_ratio": [sum(c.isdigit() for c in url) / n if n else 0],
            "special_char_count": [sum(not c.isalnum() for c in url)],
        })

# Carga de joblib
try:
    import joblib
except ImportError:
    joblib = None


def md(s: str):
    """Renderiza HTML en Streamlit sin que el formateo de indentación lo rompa."""
    clean = "\n".join(l.strip() for l in s.splitlines() if l.strip())
    st.markdown(clean, unsafe_allow_html=True)


# ==============================================================================
# 🎨 ESTILOS (Sistema visual NordVPN: azul #4687ff, navy #010e32, blanco)
# ==============================================================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
:root{
  --blue:#4687ff; --blue-d:#2f6fe8; --navy:#010e32; --ink:#010e32; --muted:#5b6478;
  --line:#e3e8f1; --soft:#f4f7fb; --ok:#0a8f5c; --bad:#d92d20; --ok-bg:#e8f7f0; --bad-bg:#fdecea;
}
html, body, .stApp, [class*="css"]{
  font-family:'Inter',-apple-system,'Segoe UI',Roboto,sans-serif !important;
  background:#fff !important; color:var(--ink) !important;
}
html{scroll-behavior:smooth;}
#MainMenu, header[data-testid="stHeader"], footer, div[data-testid="stToolbar"], div[data-testid="stDecoration"]{display:none !important;}
.block-container{padding:7.8rem 2.5rem 0 2.5rem !important; max-width:1240px !important;}

/* ---------- Barra superior de estado ---------- */
.pg-status{position:fixed;top:0;left:0;right:0;height:36px;background:var(--soft);border-bottom:1px solid var(--line);
  z-index:1000000;display:flex;align-items:center;justify-content:center;gap:12px;font-size:.8rem;color:var(--muted);padding:0 1rem;white-space:nowrap;overflow:hidden;}
.pg-status b{color:var(--ink);font-weight:600;}
.pg-dot{width:3px;height:3px;border-radius:50%;background:#aab3c5;}

/* ---------- Encabezado ---------- */
.pg-header{position:fixed;top:36px;left:0;right:0;height:68px;background:#fff;border-bottom:1px solid var(--line);
  z-index:999999;display:flex;align-items:center;padding:0 2.5rem;}
.pg-header-in{max-width:1240px;width:100%;margin:0 auto;display:flex;align-items:center;gap:35px;}
.pg-logo{display:flex;align-items:center;gap:10px;text-decoration:none !important;}
.pg-logo-ico{width:32px;height:32px;border-radius:9px;background:var(--blue);color:#fff;display:flex;align-items:center;justify-content:center;font-size:17px;}
.pg-logo-txt{font-size:1.25rem;font-weight:800;letter-spacing:-.5px;color:var(--ink) !important;}
.pg-nav{display:flex;gap:6px;align-items:center;}
.pg-nav a{padding:8px 14px;border-radius:8px;text-decoration:none !important;font-size:.95rem;font-weight:500;color:var(--ink) !important;transition:all .15s ease;}
.pg-nav a:hover{background:var(--soft);}
.pg-nav a.on{color:var(--blue) !important;font-weight:700;}
.pg-header-cta{margin-left:auto;display:flex;gap:10px;align-items:center;}
.pg-btn{display:inline-block;background:var(--blue);color:#fff !important;font-weight:700;font-size:.92rem;padding:9px 18px;border-radius:8px;text-decoration:none !important;}
.pg-btn:hover{background:var(--blue-d);}

/* ---------- Hero ---------- */
.hero-h1{font-size:2.6rem;font-weight:800;line-height:1.12;letter-spacing:-1.2px;margin:6px 0 22px;}
.hero-lbl{font-size:.95rem;font-weight:600;margin-bottom:8px;}
.stTextInput > div > div > input{background:#fff !important;color:var(--ink) !important;border:1.5px solid #cfd7e6 !important;
  border-radius:10px !important;padding:15px 16px !important;font-size:.98rem !important;font-family:'JetBrains Mono',monospace !important;}
.stTextInput > div > div > input:focus{border-color:var(--blue) !important;box-shadow:0 0 0 3px rgba(70,135,255,.18) !important;}
.stTextInput > div{border:none !important;}

/* Botones */
.stButton > button{border-radius:10px !important;font-weight:600 !important;transition:all .15s ease;}
.stButton > button[kind="primary"], .stButton > button[data-testid="stBaseButton-primary"]{
  background:var(--blue) !important;color:#fff !important;border:none !important;padding:14px 26px !important;font-size:1rem !important;font-weight:700 !important;}
.stButton > button[kind="primary"]:hover, .stButton > button[data-testid="stBaseButton-primary"]:hover{background:var(--blue-d) !important;}
.stButton > button[kind="secondary"], .stButton > button[data-testid="stBaseButton-secondary"]{
  background:#fff !important;color:var(--ink) !important;border:1.5px solid var(--line) !important;font-size:.82rem !important;padding:8px 10px !important;}
.stButton > button[kind="secondary"]:hover, .stButton > button[data-testid="stBaseButton-secondary"]:hover{border-color:var(--blue) !important;color:var(--blue) !important;}
.try-lbl{font-size:.85rem;color:var(--muted);margin:14px 0 6px;}

/* ---------- Tarjeta de resultado ---------- */
.res-card{border:1.5px solid var(--line);border-radius:20px;padding:26px;background:#fff;box-shadow:0 10px 30px rgba(1,14,50,.06);}
.res-banner{display:flex;align-items:center;gap:12px;padding:14px 16px;border-radius:12px;margin-bottom:18px;}
.res-banner.ok{background:var(--ok-bg);} .res-banner.bad{background:var(--bad-bg);}
.res-banner .ic{font-size:1.5rem;}
.res-banner .t{font-weight:800;font-size:1.1rem;} .res-banner.ok .t{color:var(--ok);} .res-banner.bad .t{color:var(--bad);}
.res-banner .s{font-size:.85rem;color:var(--muted);}
.meter{height:8px;border-radius:99px;background:var(--soft);overflow:hidden;margin:0 0 22px;}
.meter > div{height:100%;border-radius:99px;}
.res-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px 24px;}
.f-lbl{font-size:.82rem;color:var(--muted);margin-bottom:3px;}
.f-val{font-size:1.02rem;font-weight:700;word-break:break-word;}
.f-val.ok{color:var(--ok);} .f-val.bad{color:var(--bad);} .f-val.blue{color:var(--blue);font-size:.9rem;}
.res-empty{border:1.5px dashed #cfd7e6;border-radius:20px;padding:40px 26px;text-align:center;color:var(--muted);}

/* ---------- Índice y secciones ---------- */
.toc{display:flex;flex-wrap:wrap;gap:10px;margin:56px 0 8px;padding:20px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);}
.toc a{text-decoration:none !important;color:var(--ink) !important;font-size:.9rem;font-weight:500;padding:7px 14px;border-radius:99px;background:var(--soft);}
.toc a:hover{color:var(--blue) !important;}
.sec{padding-top:48px;}
.sec h2{font-size:1.9rem;font-weight:800;letter-spacing:-.8px;margin:0 0 14px;}
.sec p{font-size:1rem;line-height:1.7;color:#2b3550;max-width:860px;}
.tbl{width:100%;border-collapse:collapse;margin-top:8px;border:1.5px solid var(--line);border-radius:14px;overflow:hidden;}
.tbl td{padding:18px 20px;border-bottom:1px solid var(--line);vertical-align:top;font-size:.96rem;line-height:1.6;color:#2b3550;}
.tbl tr:last-child td{border-bottom:none;}
.tbl td:first-child{width:28%;font-weight:700;color:var(--ink);background:var(--soft);}

/* CTA Banner */
.cta{margin-top:56px;background:var(--navy);border-radius:24px;padding:44px 48px;display:flex;align-items:center;justify-content:space-between;gap:30px;flex-wrap:wrap;}
.cta h3{color:#fff;font-size:1.7rem;font-weight:800;letter-spacing:-.6px;margin:0 0 8px;}
.cta p{color:#b8c3de;margin:0;font-size:1rem;}

.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:10px;}
.step{background:var(--soft);border-radius:16px;padding:24px;}
.step .n{width:34px;height:34px;border-radius:50%;background:var(--blue);color:#fff;font-weight:700;display:flex;align-items:center;justify-content:center;margin-bottom:14px;}
.step h4{margin:0 0 6px;font-size:1.05rem;font-weight:700;} .step p{margin:0;font-size:.93rem;color:var(--muted);line-height:1.6;}

details.faq{border-bottom:1px solid var(--line);padding:18px 0;max-width:900px;}
details.faq summary{cursor:pointer;font-weight:700;font-size:1.03rem;list-style:none;display:flex;justify-content:space-between;}
details.faq summary::after{content:"+";color:var(--blue);font-size:1.4rem;line-height:1;}
details.faq[open] summary::after{content:"–";}
details.faq p{margin:12px 0 0;color:#2b3550;line-height:1.7;font-size:.97rem;}

/* ---------- Modelos / Ayuda ---------- */
.pg-title{font-size:2.3rem;font-weight:800;letter-spacing:-1px;margin:6px 0 10px;}
.pg-sub{font-size:1.05rem;color:var(--muted);line-height:1.6;max-width:860px;margin-bottom:30px;}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:22px;}
.card{background:#fff;border:1.5px solid var(--line);border-radius:18px;padding:28px;}
.card h3{margin:0 0 12px;font-size:1.25rem;font-weight:800;color:var(--blue);}
.card ul, .card ol{margin:0;padding-left:20px;line-height:1.8;color:#2b3550;font-size:.95rem;}
.card.alert{background:var(--bad-bg);border-color:#f6c9c4;} .card.alert h3{color:var(--bad);}
.card code{background:var(--soft);padding:2px 6px;border-radius:5px;font-size:.85em;}

/* ---------- Pie de página ---------- */
.foot{margin:80px -2.5rem 0;background:var(--soft);border-top:1px solid var(--line);padding:52px 2.5rem 30px;}
.foot-in{max-width:1240px;margin:0 auto;display:grid;grid-template-columns:1.3fr 1fr 1.6fr;gap:40px;}
.foot h5{margin:0 0 14px;font-size:.95rem;font-weight:700;}
.foot p, .foot li{font-size:.86rem;line-height:1.65;color:var(--muted);}
.foot ul{list-style:none;margin:0;padding:0;} .foot li{margin-bottom:8px;}
.foot .brand{font-size:1.25rem;font-weight:800;color:var(--ink);margin-bottom:10px;}
.foot-bottom{max-width:1240px;margin:36px auto 0;padding-top:20px;border-top:1px solid var(--line);font-size:.8rem;color:#8791a7;}

@media (max-width:900px){
  .block-container{padding:7.6rem 1.2rem 0 1.2rem !important;}
  .pg-header{padding:0 1rem;} .pg-header-in{gap:14px;} .pg-header-cta, .pg-logo-txt{display:none;}
  .pg-nav a{padding:8px 8px;font-size:.85rem;}
  .hero-h1{font-size:2rem;} .g2,.steps,.foot-in,.res-grid{grid-template-columns:1fr;}
  .cta{padding:30px 24px;} .foot{margin:60px -1.2rem 0;padding:40px 1.2rem 24px;}
  .pg-status{font-size:.72rem;}
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ==============================================================================
# 🤖 DETECCIÓN Y CARGA AUTOMÁTICA DEL MODELO ML (.pkl)
# ==============================================================================
# INSTRUCCIÓN PARA EL EQUIPO:
# Coloquen 'modelo_phishing.pkl', 'modelo_lr_phishing.pkl' o 'modelo_rf_phishing.pkl'
# en la carpeta raíz del proyecto. La aplicación lo cargará y usará automáticamente.
@st.cache_resource(show_spinner=False)
def load_pipeline():
    candidates = [
        "modelo_phishing.pkl",
        "modelo_lr_phishing.pkl",
        "modelo_rf_phishing.pkl",
        "modelo.pkl"
    ]
    for p in candidates:
        if os.path.exists(p) and joblib is not None:
            try:
                return joblib.load(p), p
            except Exception:
                pass
    # Búsqueda de respaldo si le dieron otro nombre al .pkl
    if joblib is not None:
        try:
            for f in os.listdir("."):
                if f.endswith(".pkl") and not f.startswith("."):
                    try:
                        return joblib.load(f), f
                    except Exception:
                        pass
        except Exception:
            pass
    return None, None


pipeline_ml, pipeline_path = load_pipeline()

SUSPICIOUS = ["login", "verify", "secure", "account", "update", "bank", "banco", "pago", "free", "bonus", "signin"]


def heuristic_prob(has_https, is_ip, url_len, n_kw, n_special):
    score = 10
    if not has_https: score += 25
    if is_ip: score += 35
    if url_len > 60: score += 15
    score += n_kw * 15
    if n_special > 8: score += 10
    return min(max(score / 100.0, 0.01), 0.99)


# ==============================================================================
# 🔝 BARRA DE ESTADO + ENCABEZADO FIJO
# ==============================================================================
motor_txt = f"Modelo ML activo ({pipeline_path})" if pipeline_ml is not None else "Modo heurístico (esperando .pkl)"
on = lambda p: "on" if current_page == p else ""

md(f"""
<div class="pg-status">
  <span>Motor: <b>{htmllib.escape(motor_txt)}</b></span><span class="pg-dot"></span>
  <span>Dataset: <b>116,600+ URLs</b></span><span class="pg-dot"></span>
  <span>Privacidad: <b>evaluación volátil en memoria</b></span>
</div>
<header class="pg-header"><div class="pg-header-in">
  <a class="pg-logo" href="?page=analizar" target="_self">
    <div class="pg-logo-ico">🛡️</div>
    <span class="pg-logo-txt">PhishGuard</span>
  </a>
  <nav class="pg-nav">
    <a class="{on('analizar')}" href="?page=analizar" target="_self">Analizar URL</a>
    <a class="{on('modelos')}" href="?page=modelos" target="_self">Modelos IA</a>
    <a class="{on('ayuda')}" href="?page=ayuda" target="_self">Ayuda y consejos</a>
  </nav>
  <div class="pg-header-cta">
    <a class="pg-btn" href="?page=analizar" target="_self">Analizar URL</a>
  </div>
</div></header>
""")

# ==============================================================================
# 📄 PÁGINA 1: ANALIZAR URL (HERRAMIENTA PRINCIPAL)
# ==============================================================================
if current_page == "analizar":
    EJ_PHISH = "http://banco-pichincha-seguridad-login.net/actualizar-datos.php?id=82931"
    
    if "url_input" not in st.session_state:
        st.session_state["url_input"] = EJ_PHISH

    def set_sample_url(target_url: str):
        st.session_state["url_input"] = target_url

    col_l, col_r = st.columns([1.1, 1], gap="large")

    with col_l:
        md("""
        <div class="hero-h1">Herramienta gratuita de detección de phishing: analiza la seguridad de cualquier URL</div>
        <div class="hero-lbl">Introduce la URL que quieres analizar</div>
        """)
        
        user_url = st.text_input(
            "URL a analizar",
            key="url_input",
            placeholder="https://ejemplo.com/...",
            label_visibility="collapsed"
        )
        
        st.button("Obtener detalles de URL", key="btn_run", type="primary", use_container_width=True)

        md('<div class="try-lbl">Prueba con un ejemplo de un clic:</div>')
        examples = [
            ("🚨 Phishing banco", EJ_PHISH),
            ("🚨 IP sospechosa", "http://192.168.1.105/paypal/signin/verification.php"),
            ("✅ Google", "https://www.google.com/search?q=phishing+detection"),
            ("✅ GitHub", "https://github.com/alex171215/Detector-Phishing-ML"),
        ]
        
        for col, (label, url) in zip(st.columns(4), examples):
            with col:
                st.button(
                    label,
                    key=f"ex_{label}",
                    on_click=set_sample_url,
                    args=(url,),
                    use_container_width=True
                )

    # ---------------- Lógica de Inferencia ----------------
    raw_url = (user_url or "").strip()
    with col_r:
        if not raw_url:
            md('<div class="res-empty">Introduce una dirección URL para ver el análisis de seguridad en tiempo real.</div>')
        else:
            norm_url = raw_url if "://" in raw_url else "http://" + raw_url
            parsed = urllib.parse.urlparse(norm_url)
            has_https = parsed.scheme.lower() == "https"
            host = parsed.hostname or ""
            is_ip = bool(re.match(r"^[0-9]+(?:\.[0-9]+){3}$", host))
            url_len = len(norm_url)
            n_special = sum(not c.isalnum() for c in norm_url)
            kws = [w for w in SUSPICIOUS if w in norm_url.lower()]

            prob, motor, debug_error = None, None, None
            
            # Intento de inferencia con el Pipeline entrenado
            if pipeline_ml is not None:
                try:
                    df = extract_features_from_url(norm_url)
                    prob = float(pipeline_ml.predict_proba(df)[0][1])
                    motor = f"Scikit-Learn ({pipeline_path})"
                except Exception as ex:
                    prob = None
                    debug_error = str(ex)

            # Respaldo heurístico
            if prob is None:
                prob = heuristic_prob(has_https, is_ip, url_len, len(kws), n_special)
                motor = "Heurístico léxico" + (" (error al predecir .pkl)" if pipeline_ml is not None else " (esperando .pkl)")

            threat = prob >= 0.5
            cls = "bad" if threat else "ok"
            title = "Phishing / Sospechosa" if threat else "Segura / Legítima"
            conf = f"{prob*100:.1f}% de riesgo" if threat else f"{(1-prob)*100:.1f}% de seguridad"
            color = "var(--bad)" if threat else "var(--ok)"
            kw_txt = htmllib.escape(", ".join(kws)) if kws else "Ninguna detectada"

            md(f"""
            <div class="res-card">
              <div class="res-banner {cls}">
                <div class="ic">{'⚠️' if threat else '✅'}</div>
                <div><div class="t">{title}</div><div class="s">{conf}</div></div>
              </div>
              <div class="meter"><div style="width:{prob*100:.0f}%;background:{color};"></div></div>
              <div class="res-grid">
                <div><div class="f-lbl">Dominio / Host</div><div class="f-val">{htmllib.escape(host) or 'No especificado'}</div></div>
                <div><div class="f-lbl">Protocolo Web</div>
                  <div class="f-val {'ok' if has_https else 'bad'}">{'HTTPS (cifrado)' if has_https else 'HTTP (inseguro)'}</div></div>
                <div><div class="f-lbl">Tipo de Dirección</div>
                  <div class="f-val {'bad' if is_ip else ''}">{'Dirección IP directa' if is_ip else 'Nombre de dominio (DNS)'}</div></div>
                <div><div class="f-lbl">Longitud de URL</div><div class="f-val">{url_len} caracteres</div></div>
                <div><div class="f-lbl">Palabras Sensibles</div><div class="f-val">{kw_txt}</div></div>
                <div><div class="f-lbl">Motor de IA</div><div class="f-val blue">{htmllib.escape(motor)}</div></div>
              </div>
            </div>
            """)

            if debug_error:
                st.caption(f"ℹ️ Detalle para desarrolladores: el archivo `{pipeline_path}` arrojó: {debug_error}. Revisa que extractor.py devuelva las mismas columnas del entrenamiento.")

    # ---------------- Contenido Informativo (NordVPN Style) ----------------
    md("""
    <div class="toc">
      <a href="#que-es" target="_self">Herramienta de análisis</a>
      <a href="#que-revela" target="_self">¿Qué revela el análisis?</a>
      <a href="#que-no" target="_self">¿Qué no puede revelar?</a>
      <a href="#pasos" target="_self">Cómo usarla</a>
      <a href="#faq" target="_self">Preguntas frecuentes</a>
    </div>
    <div class="sec" id="que-es"><h2>¿Qué es la herramienta de análisis de URL?</h2>
      <p>PhishGuard es un servicio académico gratuito que estima si un enlace presenta características de phishing. Extrae variables léxicas y morfológicas de la URL (longitud, protocolo, tipo de dirección, caracteres especiales y palabras sensibles) y las evalúa con algoritmos de Machine Learning entrenados con más de 116,600 registros.</p></div>
    <div class="sec" id="que-revela"><h2>¿Qué información revela el análisis?</h2>
      <table class="tbl">
        <tr><td>Nivel de riesgo</td><td>Una probabilidad continua de phishing entre 0% y 100% calculada por el modelo predictivo.</td></tr>
        <tr><td>Estructura de la URL</td><td>Host o IP, protocolo (HTTP/HTTPS), longitud de caracteres y presencia de caracteres no alfanuméricos.</td></tr>
        <tr><td>Palabras sensibles</td><td>Detección de términos comúnmente utilizados en suplantaciones bancarias (login, verify, secure, banco, etc.).</td></tr>
      </table></div>
    <div class="sec" id="que-no"><h2>¿Qué no puede revelar?</h2>
      <table class="tbl">
        <tr><td>El contenido interno de la página</td><td>El análisis es morfológico-léxico: no ejecuta JavaScript ni rastrea formularios ocultos dentro del sitio web.</td></tr>
        <tr><td>Identidad del remitente</td><td>No determina la identidad legal de quien envió el correo o mensaje con el enlace.</td></tr>
        <tr><td>Certeza absoluta del 100%</td><td>Se trata de inferencias probabilísticas basadas en datos estadísticos; siempre se recomienda precaución perimetral.</td></tr>
      </table></div>
    <div class="cta">
      <div><h3>¿Un enlace te parece sospechoso?</h3><p>Conoce las medidas inmediatas antes de abrir enlaces y cómo protegerte si ya ingresaste credenciales.</p></div>
      <a class="pg-btn" href="?page=ayuda" target="_self">Ver guía de seguridad</a>
    </div>
    <div class="sec" id="pasos"><h2>Analiza una URL en tres pasos</h2>
      <div class="steps">
        <div class="step"><div class="n">1</div><h4>Copia el enlace</h4><p>No hagas clic directamente. Copia la dirección desde el correo o mensaje.</p></div>
        <div class="step"><div class="n">2</div><h4>Pégalo en el buscador</h4><p>Introdúcelo en el campo superior y pulsa «Obtener detalles de URL».</p></div>
        <div class="step"><div class="n">3</div><h4>Evalúa el veredicto</h4><p>Revisa la probabilidad de amenaza y los factores de riesgo detectados.</p></div>
      </div></div>
    <div class="sec" id="faq"><h2>Preguntas frecuentes</h2>
      <details class="faq"><summary>¿Cómo funciona el detector?</summary><p>Convierte la URL en métricas numéricas estructuradas y las envía al Pipeline entrenado con Scikit-Learn, el cual calcula la probabilidad de pertenecer a la clase phishing mediante <code>.predict_proba()</code>.</p></details>
      <details class="faq"><summary>¿Se guardan las URLs analizadas?</summary><p>No. Las cadenas de texto se evalúan de forma efímera en la memoria RAM del servidor de inferencia sin almacenarse en bases de datos externas.</p></details>
      <details class="faq"><summary>¿Por qué una URL con HTTPS puede ser phishing?</summary><p>HTTPS únicamente garantiza que la conexión entre tu dispositivo y el servidor esté cifrada; no garantiza que el dueño del servidor sea una entidad legítima. Muchos ciberdelincuentes instalan certificados SSL gratuitos.</p></details>
    </div>
    """)

# ==============================================================================
# 📄 PÁGINA 2: MODELOS IA
# ==============================================================================
elif current_page == "modelos":
    md("""
    <div class="pg-title">Modelos de Inteligencia Artificial</div>
    <div class="pg-sub">Fundamentación técnica, formulación y comparación de algoritmos entrenados para la clasificación de phishing sobre más de 116,600 muestras.</div>
    <div class="g2">
      <div class="card"><h3>1. Regresión Logística (Modelo Lineal)</h3><ul>
        <li><strong>Tipo:</strong> Clasificador probabilístico lineal fundamentado en la función sigmoide.</li>
        <li><strong>Estimación de Certeza:</strong> Genera probabilidades continuas de 0% a 100% mediante <code>.predict_proba()</code>.</li>
        <li><strong>Interpretabilidad:</strong> Permite conocer la influencia directa de cada variable predictora mediante sus coeficientes y odds-ratios.</li>
        <li><strong>Tratamiento del Desbalance:</strong> Ajustado con <code>class_weight='balanced'</code> para penalizar los falsos negativos de phishing (14% de la muestra total).</li></ul></div>
      <div class="card"><h3>2. Bosques Aleatorios / Árboles de Decisión</h3><ul>
        <li><strong>Tipo:</strong> Modelo de ensamble no lineal basado en árboles y particiones ortogonales jerárquicas.</li>
        <li><strong>Interacciones Complejas:</strong> Detecta combinaciones sospechosas (ej. ausencia de HTTPS + dominio IP + longitud superior a 75 caracteres).</li>
        <li><strong>Importancia de Variables:</strong> Pondera la capacidad de discriminación de cada métrica mediante la reducción de impureza de Gini.</li>
        <li><strong>Evaluación Comparativa:</strong> Comparación rigurosa de Curvas ROC, AUC, Precision y Recall frente a la Regresión Logística.</li></ul></div>
    </div>
    """)

# ==============================================================================
# 📄 PÁGINA 3: AYUDA Y CONSEJOS
# ==============================================================================
else:
    md("""
    <div class="pg-title">Guía de ciberseguridad y consejos preventivos</div>
    <div class="pg-sub">Instrucciones recomendadas ante enlaces sospechosos y protocolo de mitigación ante filtración de datos.</div>
    <div class="g2">
      <div class="card alert"><h3>🚨 Si el detector clasifica una URL como phishing:</h3><ul>
        <li><strong>No accedas ni ingreses información:</strong> Jamás digites contraseñas, cédulas, números de tarjeta ni códigos temporales SMS/OTP.</li>
        <li><strong>Verifica el canal de procedencia:</strong> Inspecciona la dirección de correo o teléfono emisor para identificar irregularidades.</li>
        <li><strong>Usa el canal oficial legítimo:</strong> Abre una nueva pestaña en tu navegador y escribe tú mismo la dirección oficial de tu banco o plataforma.</li>
        <li><strong>Reporta el intento de fraude:</strong> Notifica al departamento de soporte de la institución suplantada o repórtalo en tu cliente de correo.</li></ul></div>
      <div class="card"><h3>🔑 ¿Ingresaste credenciales o datos bancarios por error?</h3><ol>
        <li><strong>Cambia tu contraseña de inmediato</strong> desde el portal oficial por una combinación robusta y no repetida.</li>
        <li><strong>Activa la autenticación en dos pasos (2FA/MFA)</strong> mediante aplicaciones autenticadoras o llaves físicas.</li>
        <li><strong>Comunícate con tu institución bancaria</strong> para solicitar el bloqueo preventivo de tarjetas o transferencias.</li>
        <li><strong>Cierra sesiones activas</strong> desde el panel de seguridad de tu cuenta en todos los dispositivos.</li></ol></div>
    </div>
    """)

# ==============================================================================
# 🔻 PIE DE PÁGINA (ESTÁNDAR NORDVPN EN 3 COLUMNAS)
# ==============================================================================
md("""
<footer class="foot">
  <div class="foot-in">
    <div>
      <div class="brand">PhishGuard AI</div>
      <p>Sistema de detección de phishing en URLs con Machine Learning. Proyecto académico de Semestre 6.</p>
    </div>
    <div>
      <h5>Autores del Proyecto</h5>
      <ul>
        <li>👨‍💻 Alejandro Flores</li>
        <li>👨‍💻 Paul Rosero</li>
        <li>👩‍💻 Gloria Chassi</li>
      </ul>
    </div>
    <div>
      <h5>Términos, cookies y privacidad</h5>
      <ul>
        <li><strong>Aviso de cookies:</strong> Se emplean únicamente variables de sesión volátiles para mantener el estado temporal; sin rastreo ni telemetría comercial.</li>
        <li><strong>Tratamiento de datos:</strong> Las URLs son examinadas en tiempo real en la memoria RAM del servidor de inferencia sin almacenamiento persistente.</li>
        <li><strong>Descargo de responsabilidad:</strong> Prototipo académico de investigación. Las clasificaciones son inferencias probabilísticas y no sustituyen soluciones perimetrales empresariales.</li>
      </ul>
    </div>
  </div>
  <div class="foot-bottom">
    © 2026 PhishGuard AI. Todos los derechos reservados.
  </div>
</footer>
""")