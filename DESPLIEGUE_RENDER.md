# 🚀 Guía de Despliegue en Producción con Render

Este documento detalla el estado actual del proyecto, los pasos pendientes que debe completar el equipo y las instrucciones paso a paso para publicar la aplicación web **PhishGuard AI** en la nube de **Render.com** de forma 100% gratuita.

---

## 📋 1. Estado Actual: ¿Qué está listo y qué falta?

### ✅ Lo que ya está listo y probado:
* **Aplicación Web ([`app.py`](app.py)):** Interfaz completa y responsiva inspirada en el diseño y paleta de NordVPN (azul `#4687ff`, blanco y azul noche `#010e32`), con encabezado fijo, navegación entre pestañas (*Analizar URL*, *Modelos IA*, *Ayuda y consejos*) y pie de página en 3 columnas con autores y avisos legales.
* **Manejo de Errores y Modo Respaldo:** Si aún no existe el archivo `.pkl`, la aplicación funciona automáticamente con un motor heurístico léxico sin romperse.
* **Detección Automática de Modelos:** `app.py` busca automáticamente cualquier archivo `.pkl` (`modelo_phishing.pkl`, `modelo_lr_phishing.pkl`, `modelo_rf_phishing.pkl`).
* **Dependencias ([`requirements.txt`](requirements.txt)):** Todas las librerías necesarias ya están declaradas.

### ⏳ Lo que falta por completar antes del despliegue final:
1. **Descargar el Dataset:** Descargar `Dataset.csv` (desde Kaggle: *Phishing URL Detection, 111K/116K URLs, 22 Features*) y colocarlo en la raíz del proyecto.
2. **Entrenar y Comparar Modelos en el Notebook:**
   * Abrir [`notebook_phishing.ipynb`](notebook_phishing.ipynb).
   * Ejecutar la **Regresión Logística**.
   * Agregar y entrenar el segundo modelo (**Random Forest** o **Árbol de Decisión**).
   * Comparar métricas (Precision, Recall, F1-Score, Curva ROC / AUC).
3. **Exportar el Pipeline Ganador:**
   * Guardar el modelo ganador con:
     ```python
     import joblib
     joblib.dump(pipeline_ganador, 'modelo_phishing.pkl')
     ```
4. **Alinear [`extractor.py`](extractor.py):**
   * Verificar que la función `extract_features_from_url(url)` devuelva exactamente los mismos nombres y tipos de columnas que las 22 variables con las que fue entrenado el pipeline en el notebook.

---

## ☁️ 2. Paso a Paso para Desplegar en Render.com (Gratis)

Render permite desplegar aplicaciones de Python y Streamlit en servidores con ejecución continua y certificado SSL (HTTPS) automático.

### Paso 1: Crear cuenta en Render
1. Ingresa a [https://render.com](https://render.com).
2. Haz clic en **"Sign In"** o **"Get Started"** e inicia sesión utilizando tu cuenta de **GitHub**.

### Paso 2: Crear un Nuevo Web Service
1. En tu panel de control de Render (Dashboard), haz clic en el botón **"New +"** (arriba a la derecha).
2. Selecciona **"Web Service"**.
3. Elige la opción **"Build and deploy from a Git repository"** y presiona **Next**.
4. Busca y selecciona tu repositorio: `alex171215/Detector-Phishing-ML` (si no aparece, haz clic en *Configure GitHub App* para darle permisos al repositorio).

### Paso 3: Configurar los Parámetros del Servicio
En el formulario de configuración, completa los campos con los siguientes valores:

| Parámetro | Valor a Configurar |
| :--- | :--- |
| **Name** | `phishguard-ai` *(o el nombre que prefieras para tu subdominio)* |
| **Region** | `Oregon (US West)` u `Ohio (US East)` |
| **Branch** | `alejo` *(o `main` si ya fusionaron la rama)* |
| **Root Directory** | *(Dejar en blanco / vacío)* |
| **Environment / Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true` |
| **Instance Type** | `Free` *(0.5 CPU, 512 MB RAM)* |

> [!IMPORTANT]
> El comando de inicio (**Start Command**) debe incluir `--server.port $PORT --server.address 0.0.0.0 --server.headless true` para que Render pueda asignar su puerto dinámico a Streamlit sin generar errores de conexión.

### Paso 4: Iniciar el Despliegue
1. Haz clic en el botón azul **"Create Web Service"** al final de la página.
2. Render comenzará a construir el proyecto (verás la terminal en vivo instalando dependencias desde `requirements.txt`).
3. Cuando termine la instalación y se ejecute el Start Command, verás el mensaje:
   ```text
   ==> Your service is live 🎉
   ```
4. Render te proporcionará tu URL pública gratuita en la parte superior, con formato:
   👉 `https://phishguard-ai.onrender.com`

---

## ⚠️ 3. Consideraciones Importantes sobre Render (Plan Gratuito)

1. **Suspensión por Inactividad (*Spin down*):**
   * En el plan gratuito de Render, el servidor entra en modo de reposo si no recibe visitas durante 15 minutos.
   * La primera persona que ingrese tras un período de inactividad experimentará una espera de aproximadamente **30 a 50 segundos** mientras el servidor despierta. Las siguientes peticiones responderán instantáneamente.
2. **Tamaño del archivo `.pkl`:**
   * GitHub tiene un límite de 100 MB por archivo. Los modelos de Scikit-Learn (Regresión Logística o Random Forest podado) pesan habitualmente entre **5 MB y 40 MB**, por lo que podrás subirlo a GitHub con `git add modelo_phishing.pkl` y Render lo descargará sin problemas.
3. **Actualizaciones Automáticas (*Auto-Deploy*):**
   * Cada vez que hagas un `git push` a la rama configurada (`alejo`), Render detectará los cambios y re-desplegará la aplicación automáticamente sin que tengas que intervenir.

---

## 👥 Equipo
* **Alejandro Flores**
* **Paul Rosero**
* **Gloria Chushig**

*Proyecto académico de Inteligencia Artificial - Semestre 6.*
