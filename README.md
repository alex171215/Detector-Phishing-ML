# 🛡️ Detector de Phishing en URLs con Machine Learning

Sistema de detección y clasificación de URLs maliciosas (*Phishing*) utilizando técnicas avanzadas de **Machine Learning** y procesamiento léxico de URLs, desplegado a través de una aplicación web interactiva desarrollada con **Streamlit**.

---

## 📌 Contexto del Problema y Justificación

El **phishing** es uno de los vectores de ataque más comunes y peligrosos en ciberseguridad. Consiste en engañar a los usuarios mediante enlaces fraudulentos que imitan sitios legítimos (bancos, redes sociales, servicios en la nube) para sustraer credenciales o infectar dispositivos.

### ¿Qué predice este sistema?
Dada una URL introducida por el usuario o interceptada en tiempo real, el sistema predice probabilísticamente:
* **Clase 0 (Benigna):** La URL corresponde a un sitio legítimo y seguro.
* **Clase 1 (Phishing):** La URL exhibe patrones maliciosos característicos de sitios fraudulentos.

---

## 🧠 Arquitectura de Modelos de Machine Learning

El proyecto contempla el entrenamiento, evaluación rigurosa y comparación de dos enfoques de clasificación binaria:

### 1. Regresión Logística (`LogisticRegression`)
* **Naturaleza:** Modelo lineal probabilístico.
* **Ventajas:** Alta interpretabilidad mediante coeficientes, cálculo nativo de probabilidades calibradas con la función sigmoide (`.predict_proba()`), y excelente velocidad de inferencia en tiempo real.
* **Ajuste:** Optimización con `class_weight='balanced'` y solucionador `lbfgs` para compensar el desbalance natural de clases.

### 2. Árboles de Decisión / Bosques Aleatorios (`DecisionTree` / `RandomForest`)
* **Naturaleza:** Modelos no lineales basados en particiones jerárquicas y ensamblado de árboles.
* **Ventajas:** Capacidad de capturar interacciones complejas y no lineales entre características estructurales (ej. longitud extrema combinada con ausencia de HTTPS y presencia de caracteres sospechosos).
* **Interpretación:** Importancia de características (*Feature Importance*) según impureza de Gini.

---

## 📊 Métricas de Evaluación para Clases Desbalanceadas

En la web real, el tráfico legítimo supera ampliamente al malicioso (~85.8% benignas vs. ~14.2% phishing). Por ello, la métrica de **Exactitud (*Accuracy*) es engañosa**. El sistema se evalúa mediante:

* **Matriz de Confusión:**
  * **Verdaderos Positivos (VP):** Phishing detectado correctamente.
  * **Falsos Positivos (FP):** Falsa alarma (sitio seguro bloqueado).
  * **Falsos Negativos (FN):** Amenaza no detectada (riesgo crítico de seguridad).
* **Recall (Sensibilidad en Clase 1):** Prioridad en ciberseguridad para minimizar los falsos negativos.
* **Precision (Precisión en Clase 1):** Garantiza que no se bloqueen sitios web legítimos sin justificación.
* **F1-Score:** Media armónica entre Precision y Recall.
* **Curva ROC y AUC (Área Bajo la Curva):** Capacidad del modelo de discriminar entre ambas clases ante distintos umbrales de decisión.

---

## 🌐 ¿Por qué una Aplicación Web en Streamlit (Python) y no solo HTML estático?

Un archivo HTML estático por sí solo en el navegador no puede ejecutar modelos de Scikit-Learn empaquetados en formato binario (`.pkl`) ni procesar la extracción de características de Python.

Se utiliza **Streamlit** porque:
1. **Backend y Frontend en Python unificados:** Carga en memoria el pipeline serializado (`joblib`) y procesa solicitudes instantáneamente.
2. **Extracción Léxica en Vivo:** Cuando el usuario pega una URL, [`extractor.py`](extractor.py) descompone la URL en tiempo real y la entrega al pipeline con las transformaciones exactas (`StandardScaler`, `ColumnTransformer`).
3. **Semáforo y Diagnóstico Visual:** Muestra la probabilidad porcentual calculada y desglosa qué elementos hicieron sospechosa la URL (longitud, uso de IP en lugar de dominio, caracteres especiales, protocolo inseguro, etc.).

---

## 📁 Estructura del Repositorio

```text
Detector-Phishing-ML/
│
├── README.md                      # Documentación principal y contextualización
├── Plan de acción.md             # Rúbrica y fases metodológicas del proyecto
├── requirements.txt               # Dependencias del entorno de desarrollo
│
├── notebook_phishing.ipynb        # EDA, ingeniería de características, entrenamiento y comparación de modelos
├── extractor.py                   # Módulo de extracción de características léxicas de URLs
├── app.py                         # Aplicación web interactiva (Streamlit)
│
├── modelo_phishing.pkl            # Pipeline del modelo ganador serializado con joblib (generado tras entrenar)
└── Taller_Regresion_Logistica.html# Guía de referencia teórica
```

---

## 🚀 Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/alex171215/Detector-Phishing-ML.git
cd Detector-Phishing-ML
```

### 2. Crear y activar un entorno virtual (Recomendado)
```bash
# En Windows:
python -m venv .venv
.venv\Scripts\activate

# En Linux/macOS:
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 4. Entrenar y generar el modelo
1. Descargar el archivo `Dataset.csv` y colocarlo en la raíz del proyecto.
2. Abrir y ejecutar todas las celdas de [`notebook_phishing.ipynb`](notebook_phishing.ipynb).
3. Se generará automáticamente el archivo `modelo_phishing.pkl`.

### 5. Ejecutar la Aplicación Web
```bash
streamlit run app.py
```
La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`.

---

## 👥 Equipo y Autores
Proyecto académico de Inteligencia Artificial - Clasificación Supervisada para Ciberseguridad.
