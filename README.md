# 🛡️ PhishGuard: detector de phishing en URLs con Machine Learning

Sistema que clasifica URLs como **benignas (0)** o **phishing (1)** a partir de sus características léxicas y estructurales. Compara tres modelos de scikit-learn y despliega el ganador en una aplicación web con **Streamlit**.

*Proyecto académico de Inteligencia Artificial (Semestre 6): clasificación supervisada y ciberseguridad.*

## 👥 Equipo y reparto

| Integrante | Modelo | Archivo de lógica | Notebook |
| --- | --- | --- | --- |
| **Paul Rosero** | Regresión Logística | `src/models/logistic_regression.py` | `notebooks/02_regresion_logistica.ipynb` |
| **Alejandro Flores** | Random Forest | `src/models/random_forest.py` | `notebooks/03_random_forest.ipynb` |
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
│   ├── modelo_rf.pkl
│   ├── modelo_svm.pkl
│   └── metricas.json           # métricas de prueba (las muestra la app)
│
├── notebooks/
│   ├── 01_eda_preprocesamiento.ipynb   # común: EDA, 3 gráficos, división
│   ├── 02_regresion_logistica.ipynb    # Paul
│   ├── 03_random_forest.ipynb          # Alejandro
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
│       ├── random_forest.py
│       └── linear_svm.py
│
├── scripts/
│   ├── entrenar.py             # python -m scripts.entrenar rf
│   └── validar_extractor.py    # python -m scripts.validar_extractor
│
└── docs/
    ├── Plan de acción.md
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

## ✅ Pendientes

1. **Todos:** poner `Dataset.csv` en `data/` y correr el notebook `01`.
2. **Todos (antes de entrenar):** revisar `df.columns` y llenar en `src/config.py` las listas `FEATURES` y `COLUMNAS_EXCLUIDAS`. Después, completar `src/extractor.py` hasta que `python -m scripts.validar_extractor` salga todo en ✅.
3. **Paul:** revisar `logistic_regression.py` (ya trae la configuración original) y completar el notebook `02`.
4. **Alejandro:** implementar `random_forest.py` y completar el notebook `03`.
5. **Gloria:** implementar `linear_svm.py` y completar el notebook `04`.
6. **Todos:** notebook `05`, elegir el ganador y poner su clave en `config.MODELO_POR_DEFECTO`.
7. Completar las interpretaciones (`TODO`) en los notebooks, el gráfico 3 del EDA, el informe PDF y la demo.

Pueden buscar todo lo pendiente con: `grep -rn "TODO" src notebooks`.

## 🚀 Instalación y ejecución

```bash
git clone https://github.com/alex171215/Detector-Phishing-ML.git
cd Detector-Phishing-ML
python -m pip install -r requirements.txt
```

Entrenar (desde la raíz del proyecto):

```bash
python -m scripts.entrenar lr       # o rf, svm, todos
```

Abrir la aplicación:

```bash
python -m streamlit run app.py      # http://localhost:8501
```

La app carga sola los `.pkl` que existan en `models/`. Si hay más de uno, muestra un selector de modelo. Si no hay ninguno, funciona en **modo heurístico** para que nunca se caiga.

## 📊 Métricas

El dataset está desbalanceado (~85.8% benignas y ~14.2% phishing), así que el *Accuracy* por sí solo no basta. Los tres modelos se evalúan con las mismas métricas de la clase phishing:

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
