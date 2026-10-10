# 🛡️ PhishGuard: detector de phishing en URLs con Machine Learning

Sistema que clasifica URLs como **benignas (0)** o **phishing (1)** a partir de sus características léxicas y estructurales. Compara tres modelos de scikit-learn (Regresión Logística, SVM lineal y SVM gaussiano) y despliega el ganador en una aplicación web con **Streamlit**.

*Proyecto académico de Inteligencia Artificial (Semestre 6): clasificación supervisada y ciberseguridad.*

## 👥 Equipo y reparto

| Integrante | Modelo | Archivo de lógica | Notebook |
| --- | --- | --- | --- |
| **Paul Rosero** | Regresión Logística | `src/models/logistic_regression.py` | `notebooks/02_regresion_logistica.ipynb` |
| **Alejandro Flores** | SVM gaussiano (RBF) | `src/models/svm_gaussiano.py` | `notebooks/03_svm_gaussiano.ipynb` |
| **Gloria Chushig** | SVM lineal | `src/models/linear_svm.py` | `notebooks/04_svm_lineal.ipynb` |
| Todos | EDA, extractor y comparación | `src/extractor.py`, `src/config.py` | `01_…` y `05_…` |

## 📁 Estructura

```text
ProyectoRDA1/
├── app.py                      # Interfaz web (Streamlit). Sin lógica de ML.
├── requirements.txt
├── README.md
│
├── data/
│   └── Dataset.csv             # ← descargar de Kaggle (no se sube a GitHub)
│
├── models/                     # Modelos exportados (los genera el entrenamiento)
│   ├── modelo_lr.pkl
│   ├── modelo_svm.pkl
│   ├── modelo_svm_rbf.pkl
│   └── metricas.json           # métricas de prueba (las muestra la app)
│
├── notebooks/
│   ├── 01_eda_preprocesamiento.ipynb   # común: EDA, 3 gráficos, división
│   ├── 02_regresion_logistica.ipynb    # Paul
│   ├── 03_svm_gaussiano.ipynb          # Alejandro
│   ├── 04_svm_lineal.ipynb             # Gloria
│   └── 05_comparacion_modelos.ipynb    # tabla, ROC superpuestas, ganador
│
├── src/                        # Código común (lo importan notebooks, scripts y app)
│   ├── config.py               # rutas, columnas, FEATURES, semilla, umbral
│   ├── data.py                 # carga, limpieza y división estratificada 80/20
│   ├── preprocessing.py        # ColumnTransformer (StandardScaler / passthrough)
│   ├── extractor.py            # URL → variables (mismas columnas que el dataset)
│   ├── evaluation.py           # métricas, matriz de confusión, curvas ROC
│   ├── training.py             # entrenar_y_evaluar() y exportar_final()
│   ├── predictor.py            # interfaz única que usa la app
│   └── models/
│       ├── __init__.py         # registro de modelos y armado del Pipeline
│       ├── logistic_regression.py
│       ├── linear_svm.py
│       └── svm_gaussiano.py
│
├── scripts/
│   ├── entrenar.py             # python -m scripts.entrenar svm_rbf
│   └── validar_extractor.py    # python -m scripts.validar_extractor
│
└── docs/
    ├── Informe_PhishGuard.pdf  # informe final (y .docx editable)
    ├── capturas/               # capturas de la app para el informe
    ├── Plan de acción.md
    ├── PLAN_IMPLEMENTACION.md
    ├── DESPLIEGUE_RENDER.md
    └── Taller_Regresion_Logistica.html
```

## 🔌 Cómo encaja todo

```text
Dataset.csv ─► data.py ─► preprocessing.py + models/<tu_modelo>.py ─► Pipeline
                                                                      │
                               evaluation.py ◄─ training.py ──────────┤
                                                                      ▼
                                                           models/modelo_xx.pkl
                                                                      │
   URL del usuario ─► app.py ─► predictor.py ─► extractor.py ─────────┘
```

Cada integrante **solo programa `construir_clasificador()`** en su archivo de `src/models/`. Esa función devuelve el estimador de scikit-learn sin entrenar. El código común ya resuelve lo demás: preprocesamiento, Pipeline, partición, métricas, gráficos, exportación del `.pkl`, la tabla de la app y la conexión con la interfaz.

## 📊 Resultados

Evaluación en el conjunto de prueba (23.047 URLs, 3.318 de phishing), después de eliminar 1.369 URLs duplicadas:

| Modelo | Recall | Precision | F1 | AUC | Ataques no detectados (FN) | Falsas alarmas (FP) |
| --- | --- | --- | --- | --- | --- | --- |
| Regresión Logística | **0,920** | 0,686 | 0,786 | 0,977 | **264** | 1.396 |
| SVM lineal | 0,758 | 0,910 | 0,827 | 0,976 | 803 | **248** |
| **SVM gaussiano (RBF) 🏆** | 0,903 | **0,915** | **0,909** | **0,991** | 322 | 277 |

**Modelo ganador: SVM gaussiano** (`config.MODELO_POR_DEFECTO = "svm_rbf"`). Tiene el mejor F1 y AUC, con pocos ataques
no detectados y pocas falsas alarmas; la validación cruzada estratificada de 5 particiones confirma que la ventaja es
estable (ver notebook `05`).

- El extractor (`src/extractor.py`) reproduce las 22 variables del dataset: `python -m scripts.validar_extractor` → 22/22 ✅.
- Informe final: [`docs/Informe_PhishGuard.pdf`](docs/Informe_PhishGuard.pdf) (versión editable en `.docx`).
- Capturas de la aplicación: [`docs/capturas/`](docs/capturas/).

## 🚀 Instalación y ejecución

```bash
git clone https://github.com/alex171215/Detector-Phishing-ML.git
cd Detector-Phishing-ML
python -m pip install -r requirements.txt   # Python 3.11+ (scikit-learn 1.9.1)
```

Entrenar (desde la raíz del proyecto):

```bash
python -m scripts.entrenar lr       # o svm, svm_rbf, todos
```

Abrir la aplicación:

```bash
python -m streamlit run app.py      # http://localhost:8501
```

La app carga sola los `.pkl` que existan en `models/`. Si hay más de uno, muestra un selector de modelo. Si no hay ninguno, funciona en **modo heurístico** para que nunca se caiga.

## 📊 Métricas

El dataset está desbalanceado (~85,6 % benignas y ~14,4 % phishing, sin duplicados), así que el *Accuracy* por sí solo no basta. Los tres modelos se evalúan con las mismas métricas de la clase phishing:

- **Matriz de confusión:** VP, FP (falsa alarma) y FN (phishing no detectado).
- **Recall:** métrica prioritaria, porque minimiza los falsos negativos.
- **Precision:** evita bloquear sitios legítimos.
- **F1-Score**
- **Curva ROC / AUC**

## ☁️ Despliegue

Ver [`docs/DESPLIEGUE_RENDER.md`](docs/DESPLIEGUE_RENDER.md). Start command:

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
```

## ⚖️ Licencia y responsabilidad

Proyecto con fines exclusivamente académicos. Las predicciones son probabilísticas y no reemplazan soluciones de seguridad empresariales.
