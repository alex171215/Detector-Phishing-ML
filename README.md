# 🛡️ Detector de Phishing en URLs con Machine Learning (PhishGuard)

Sistema integral de detección, análisis de amenazas y clasificación de URLs maliciosas (*Phishing*) mediante técnicas avanzadas de **Machine Learning** y procesamiento léxico en tiempo real, desplegado a través de una aplicación web interactiva desarrollada con **Streamlit** y diseñada con el sistema visual limpio de **NordVPN**.

---

## 👥 Equipo y Autores
* **Alejandro Flores**
* **Paul Rosero**
* **Gloria CHUSHIG**

*Proyecto académico de Inteligencia Artificial (Semestre 6) — Clasificación Supervisada y Ciberseguridad.*

---

## 📌 Contexto del Problema y Justificación

El **phishing** es uno de los vectores de ataque más comunes y peligrosos en el ecosistema digital. Consiste en engañar a los usuarios mediante enlaces fraudulentos que imitan plataformas legítimas (entidades bancarias, pasarelas de pago, servicios de correo o redes sociales) para sustraer credenciales y datos confidenciales.

### ¿Qué predice este sistema?
A partir de una URL suministrada en la aplicación web, el sistema extrae automáticamente sus características morfológicas y calcula probabilísticamente:
* **Clase 0 (Benigna / Legítima):** La dirección web presenta patrones estructurales seguros.
* **Clase 1 (Phishing / Maliciosa):** La URL posee anomalías léxicas típicas de páginas de suplantación de identidad.

---

## 🧠 Modelos de Machine Learning e Interpretación

El proyecto implementa y compara dos enfoques de clasificación binaria:

### 1. Regresión Logística (`LogisticRegression`)
* **Naturaleza:** Modelo lineal probabilístico.
* **Ventajas:** Alta interpretabilidad matemática a través de coeficientes y odds-ratio, inferencia ultrarrápida y calibración de probabilidades continuas con la función sigmoide (`.predict_proba()`).
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

La aplicación fue construida con **Streamlit** y un sistema de diseño limpio basado en **NordVPN** (azul `#4687ff`, blanco y navy `#010e32`), incorporando:
1. **Encabezado Fijo y Navegación Dinámica:** Menú integrado con navegación entre pantallas (*Analizar URL*, *Modelos IA*, *Ayuda y consejos*).
2. **Consola de Búsqueda y Resultados en 2 Columnas:**
   * Campo de entrada con botones de prueba rápida en un clic (Phishing bancario, IP sospechosa, Google seguro, GitHub).
   * Tarjeta de diagnóstico de 6 métricas (Host, Protocolo HTTPS/HTTP, Tipo de dirección DNS vs IP, Longitud de enlace, Palabras sensibles y Motor activo).
3. **Pie de Página en 3 Columnas:** Con créditos de los autores (**Alejandro Flores**, **Paul Rosero**, **Gloria Chassi**), aviso de cookies técnicas y descargo de responsabilidad.
4. **Detección Automática de Modelos:** Búsqueda y carga automática de `modelo_phishing.pkl` o `modelo_lr_phishing.pkl`, con motor heurístico léxico de respaldo.

---

## 📁 Estructura del Repositorio

```text
Detector-Phishing-ML/
│
├── README.md                      # Documentación completa y arquitectura del proyecto
├── DESPLIEGUE_RENDER.md          # Guía detallada para poner en producción en Render.com
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

### 3. Ejecutar la Aplicación Web
```bash
python -m streamlit run app.py
```
La aplicación se abrirá automáticamente en tu navegador en:
👉 `http://localhost:8501`

---

## ☁️ Despliegue en Producción (Render.com)

Para poner la aplicación en línea gratis con certificado HTTPS automático:
* Consulta la **[Guía de Despliegue en Render (DESPLIEGUE_RENDER.md)](DESPLIEGUE_RENDER.md)** para el paso a paso detallado.
* **Comando de inicio en Render:**
  ```bash
  streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
  ```

---

## ⚖️ Licencia y Responsabilidad
Desarrollado con fines exclusivamente académicos y de investigación en seguridad informática. Las predicciones del modelo son de naturaleza probabilística y no reemplazan sistemas de seguridad perimetral de grado empresarial.
