# 🛡️ Detector de Phishing en URLs con Machine Learning

Sistema integral de detección, análisis de amenazas y clasificación de URLs maliciosas (*Phishing*) mediante técnicas avanzadas de **Machine Learning** y procesamiento léxico en tiempo real, desplegado a través de una aplicación web interactiva desarrollada con **Streamlit**.

---

## 👥 Equipo y Autores
* **Alejandro Flores**
* **Paul Rosero**
* **Gloria Chassi**

*Proyecto académico de Inteligencia Artificial (Semestre 6) — Clasificación Supervisada y Ciberseguridad.*

---

## 📌 Contexto del Problema y Justificación

El **phishing** es uno de los vectores de ataque más comunes y peligrosos en el ecosistema digital. Consiste en engañar a los usuarios mediante enlaces fraudulentos que imitan plataformas legítimas (entidades bancarias, pasarelas de pago, servicios de correo o redes sociales) para robar credenciales y datos confidenciales.

### ¿Qué predice este sistema?
A partir de una URL suministrada en la aplicación web, el sistema extrae automáticamente sus características morfológicas y calcula probabilísticamente:
* **Clase 0 (Benigna / Legítima):** La dirección web presenta patrones estructurales seguros.
* **Clase 1 (Phishing / Maliciosa):** La URL posee anomalías léxicas típicas de páginas de suplantación de identidad.

---

## 🧠 Modelos de Machine Learning e Interpretación

El proyecto implementa y compara dos enfoques de clasificación binaria:

### 1. Regresión Logística (`LogisticRegression`)
* **Naturaleza:** Modelo lineal probabilístico.
* **Ventajas:** Alta interpretabilidad matemática a través de coeficientes y odds-ratio, inferencia ultrarrápida y calibración de probabilidades con la función sigmoide (`.predict_proba()`).
* **Ajuste:** Optimización con `class_weight='balanced'` y algoritmo optimizador `lbfgs` para compensar el desbalance natural de las muestras.

### 2. Árboles de Decisión / Random Forest (`DecisionTreeClassifier` / `RandomForestClassifier`)
* **Naturaleza:** Modelos no lineales basados en divisiones ortogonales y ensamblado de árboles.
* **Ventajas:** Captura relaciones no lineales e interacciones complejas entre variables (ej. combinación de protocolo inseguro, dominio basado en IP numérica y longitud excesiva).
* **Interpretación:** Importancia relativa de características (*Feature Importance*) según reducción de impureza de Gini.

---

## 📊 Métricas de Evaluación para Clases Desbalanceadas

En entornos reales, el tráfico legítimo supera ampliamente al fraudulento (~85.8% benignas vs. ~14.2% phishing). Debido a este desbalance, la métrica de **Exactitud (*Accuracy*) es insuficiente**. El rendimiento se evalúa con:

* **Matriz de Confusión:**
  * **Verdaderos Positivos (VP):** Phishing detectado oportunamente.
  * **Falsos Positivos (FP):** Falsa alarma (sitio legítimo marcado como peligroso).
  * **Falsos Negativos (FN):** Amenaza no detectada (riesgo crítico de seguridad).
* **Recall (Sensibilidad en Clase 1):** Métrica prioritaria para minimizar los falsos negativos.
* **Precision (Precisión en Clase 1):** Asegura no bloquear sitios legítimos innecesariamente.
* **F1-Score:** Balance armónico entre Precision y Recall.
* **Curva ROC y AUC (Área Bajo la Curva):** Mide la capacidad de separación de clases ante diferentes umbrales de decisión.

---

## 🌐 Aplicación Web Interactiva ([`app.py`](app.py))

La aplicación fue construida con **Streamlit** e incorpora:
1. **Interfaz Visual de Ciberseguridad:** Tema oscuro con tarjetas de veredicto dinámicas (🟢 Seguro vs 🔴 Phishing) y barra medidora de riesgo.
2. **Botones de Prueba Rápida con 1 Clic:** Acceso directo a ejemplos de phishing bancario, phishing con IP directa y dominios seguros (Google, GitHub).
3. **Desglose de Señales y Factores de Riesgo:** Indicadores en tiempo real sobre el protocolo (HTTPS vs HTTP), tipo de host (DNS vs IP numérica), longitud de URL y palabras clave sensibles detectadas.
4. **Marco Legal y Privacidad:** Panel con aviso de cookies técnicas de sesión, tratamiento seguro de URLs (procesamiento volátil en memoria) y recomendaciones de seguridad.
5. **Modo Híbrido (Modelo Real + Motor Heurístico de Respaldo):** Si el archivo `.pkl` aún no ha sido generado, la app activa un motor de inferencia heurístico educativo para garantizar interactividad continua.

---

## 📁 Estructura del Repositorio

```text
Detector-Phishing-ML/
│
├── README.md                      # Documentación completa y arquitectura del proyecto
├── Plan de acción.md             # Rúbrica oficial y fases metodológicas
├── requirements.txt               # Lista de librerías y dependencias
│
├── notebook_phishing.ipynb        # Cuaderno Jupyter: EDA, preprocesamiento, modelado y métricas
├── extractor.py                   # Script de extracción de métricas léxicas desde URLs
├── app.py                         # Aplicación web interactiva (Streamlit)
│
├── modelo_phishing.pkl            # Pipeline ganador serializado con joblib (generado al entrenar)
└── Taller_Regresion_Logistica.html# Guía de referencia teórica
```

---

## 🚀 Instalación y Ejecución Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/alex171215/Detector-Phishing-ML.git
cd Detector-Phishing-ML
```

### 2. Instalar dependencias
```bash
python -m pip install -r requirements.txt
```
*(O directamente: `python -m pip install streamlit pandas scikit-learn matplotlib seaborn joblib`)*

### 3. Ejecutar la Aplicación Web
Para ejecutar en Windows o cualquier sistema evitando problemas con el PATH del sistema:
```bash
python -m streamlit run app.py
```
La aplicación se abrirá automáticamente en tu navegador en:
👉 `http://localhost:8501`

---

## ☁️ Despliegue en la Nube

> [!NOTE]
> Para el despliegue en producción se recomienda **Streamlit Community Cloud** ([share.streamlit.io](https://share.streamlit.io)) o **Hugging Face Spaces**, ya que mantienen procesos continuos de Python y WebSockets (a diferencia de plataformas serverless estáticas como Vercel).

1. Conecta tu repositorio de GitHub en [Streamlit Cloud](https://share.streamlit.io).
2. Selecciona la rama (`alejo` o `main`) y el archivo principal `app.py`.
3. Haz clic en **Deploy**.

---

## ⚖️ Licencia y Responsabilidad
Desarrollado con fines exclusivamente académicos y de investigación en seguridad informática. Las predicciones del modelo son de naturaleza probabilística y no reemplazan sistemas de seguridad perimetral de grado empresarial.
