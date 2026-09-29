# Plan de acción para el proyecto de Detección de Phishing en URLs

El plan de acción para el proyecto de **Detección de Phishing en URLs** está estructurado conforme a la rúbrica oficial de 12.5 puntos, los requisitos técnicos del documento docente y las buenas prácticas vistas en el taller de regresión logística con scikit-learn.

Tanto la **Regresión Logística** como los **Árboles de Decisión** (o Random Forest) implementan nativamente `.predict_proba()` en scikit-learn, por lo que ambos algoritmos entregan probabilidades de 0 a 100%. El objetivo será entrenar ambos, compararlos con rigor estadístico y desplegar el que mejor balancee precisión y detección de amenazas.

---

## Fase 1: Selección y Preparación del Dataset

- **Dataset base:** [Phishing URL Detection (111K URLs, 22 Features)](https://www.kaggle.com/datasets/sahandnamvar/phishing-url-detection-111k-urls-22-features/code?utm_source=gemini) (116,600 filas y 22 características léxicas/estructurales calculadas).

- **Notebooks de apoyo en Kaggle:**
  - [Phishing URL Detection Using RF & MiniLM + LR](https://www.google.com/search?q=https%3A%2F%2Fwww.kaggle.com%2Fcode%2Fsahandnamvar%2Fphishing-url-detection-using-rf-minilm-lr): demuestra el uso de las 22 variables tabulares, la partición estratificada y el manejo del desbalance.
  - [111k_first_notebook](https://www.google.com/search?q=https%3A%2F%2Fwww.kaggle.com%2Fcode%2Fchinmaykhiste%2F111k-first-notebook): documenta el mapeo de nombres limpios (`url_length`, `domain_length`, `is_ip`, `is_https`, `digit_ratio`, etc.) y la correlación de variables.
  - [Phishusill_2_notebook](https://www.google.com/search?q=https%3A%2F%2Fwww.kaggle.com%2Fcode%2Fchinmaykhiste%2Fphishusill-2-notebook): útil para consultar la deduplicación de registros y la estandarización de esquemas.

- **Carga de datos:** Configurar el notebook en Jupyter o Google Colab importando `Dataset.csv`.

---

## Fase 2: Análisis Exploratorio de Datos (EDA)

*(Criterio 1 de la rúbrica: 2.0 puntos)*

1. **Estructura y diagnóstico inicial:**
   - Ejecutar `.info()`, `.describe()` y `.shape`.
   - Verificar valores nulos: en este dataset existen únicamente 14 valores faltantes en la columna `tld` debido a URLs basadas en direcciones IP puras (e.g., `http://195.191.230.50/...`), las cuales no poseen TLD por definición. Se justifica técnicamente imputarlas como `'none'` o tratarlas numéricamente.

2. **Distribución de la variable objetivo (`label`):**
   - Benignas (`0`): ~85.8% (100,000 muestras).
   - Phishing (`1`): ~14.2% (16,600 muestras).
   - Justificar en el informe que este desbalance refleja la realidad operativa de la web (donde el tráfico legítimo supera al malicioso) y motiva el uso de `stratify=y` y métricas más allá del simple Accuracy.

3. **3 Visualizaciones requeridas:**
   - *Gráfico 1:* Gráfico de barras con la distribución de clases (0 vs 1) en cantidades absolutas y porcentajes.
   - *Gráfico 2:* Heatmap de correlación entre las características léxicas (`url_len`, `digit_ratio`, `special_cnt`, `entropy`) y la etiqueta `label`.
   - *Gráfico 3:* Histogramas o boxplots comparativos de `url_len` y `digit_ratio` segmentados por clase, mostrando cómo las URLs fraudulentas tienden a ser más largas y con mayor entropía.

---

## Fase 3: Preprocesamiento y División de Datos

*(Criterios 1 y 2 de la rúbrica: 4.5 puntos combinados)*

1. **División estratificada:**
   - Separar $X$ (las 22 variables predictoras numéricas/estructurales) e $y$ (`label`).
   - Aplicar `train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)` para garantizar que el 14.2% de phishing se mantenga idéntico en entrenamiento y prueba.

2. **ColumnTransformer:**
   - Columnas numéricas continuas (`url_len`, `dom_len`, `entropy`, `special_cnt`, `digit_ratio`, etc.): procesadas con `StandardScaler()`.
   - Columnas binarias o categóricas (`is_ip`, `is_https`, etc.): passthrough directo o `OneHotEncoder(drop='first', handle_unknown='ignore')`.

3. **Construcción de Pipelines:**
   - Crear dos objetos `Pipeline` independientes de scikit-learn que encapsulen el `ColumnTransformer` junto con el clasificador correspondiente para evitar fuga de información (*data leakage*).

4. **Desarrollo y Validación del Extractor (`extractor.py`):**
   - No dejen esto para el final (Fase 5). En esta fase, cuando preparen los datos, deben programar las funciones de extracción de texto para calcular las métricas.
   - Validar que, si le pasan una URL manual, su función devuelva exactamente los mismos valores (o en el mismo formato) que las 22 columnas que usaron para entrenar. Si el extractor falla en producción, la app web fallará.

---

## Fase 4: Modelado, Comparación y Evaluación

*(Criterios 2 y 3 de la rúbrica: 5.0 puntos)*

1. **Entrenamiento de los modelos obligatorios:**
   - **Modelo 1 (Regresión Logística):** `LogisticRegression(solver='lbfgs', max_iter=1000, class_weight='balanced', random_state=42)`.
   - **Modelo 2 (Árbol de Decisión o Random Forest):** `DecisionTreeClassifier(max_depth=10, random_state=42)` o `RandomForestClassifier(n_estimators=100, random_state=42)`.

2. **Evaluación de rendimiento en el conjunto de prueba:**
   - Generar la **Matriz de Confusión** para cada modelo, interpretando Verdaderos Positivos, Falsos Positivos (falsa alarma al usuario) y Falsos Negativos (dejar pasar phishing no detectado).
   - Generar el **Classification Report** comparando: Precision, Recall y F1-Score para la clase 1 (Phishing).
   - Graficar las **Curvas ROC superpuestas** y reportar el valor del **AUC**.

3. **Selección del modelo ganador:**
   - Justificar cuál modelo ofrece el mejor equilibrio. En ciberseguridad, un alto **Recall** en la clase 1 minimiza las víctimas de phishing, mientras que una **Precision** adecuada evita bloquear sitios seguros innecesariamente.

4. **Reentrenamiento y Exportación:**
   - Reentrenar el pipeline ganador con el 100% del dataset.
   - Exportar el artefacto único con `joblib.dump(pipeline_ganador, 'modelo_phishing.pkl')`.

---

## Fase 5: Desarrollo de la Aplicación Web

*(Criterio 4 de la rúbrica: 3.5 puntos)*

- **Framework:** **Streamlit** (permite ejecución local rápida con `streamlit run app.py`).

- **Estructura del proyecto:**

```text
proyecto-phishing/
├── app.py                     # Interfaz web y lógica de inferencia
├── modelo_phishing.pkl        # Pipeline exportado con joblib
├── requirements.txt           # streamlit, scikit-learn, pandas, numpy
└── extractor.py               # Función auxiliar validada en Fase 3
```

- **Diseño funcional de la interfaz:**
  1. Un campo de texto principal: `st.text_input("Ingrese la URL a inspeccionar:")`.
  2. Uso del extractor automático en Python (`extractor.py` de la Fase 3) para calcular al instante las métricas clave de la cadena (longitud, recuento de puntos, presencia de IP, si usa HTTPS, ratio de dígitos).
  3. Formulación directa de un `pd.DataFrame` con los nombres exactos de columnas de entrenamiento.
  4. Llamada directa a `pipeline.predict()` y `pipeline.predict_proba()`.
  5. Tarjetas visuales de resultado: alerta roja con nivel de riesgo para sitios fraudulentos y tarjeta verde para sitios benignos.

---

## Fase 6: Entregables y Preparación de la Sustentación

*(Criterio 5 y documentación: 2.0 puntos)*

1. **Notebook (`.ipynb`):** Ordenado secuencialmente de EDA a exportación, sin errores de ejecución de principio a fin.

2. **Informe de la aplicación (PDF, máx. 5 páginas):**
   - Resumen del problema y contexto de seguridad.
   - Arquitectura de la solución (datos → pipeline → exportación → Streamlit).
   - Tabla comparativa de métricas (Regresión Logística vs. Árbol de Decisión).
   - Capturas de pantalla de la aplicación web evaluando enlaces reales.
   - Instrucciones de instalación local (`pip install -r requirements.txt`).

3. **Demo en vivo (5 a 10 minutos):**
   - Presentación de las métricas clave y justificación del modelo seleccionado.
   - Demostración en vivo en el equipo local probando una URL benigna oficial y una URL sospechosa simulada.

---

## Cronograma de Trabajo Recomendado

| Etapa | Actividades Principales | Fecha Sugerida |
| --- | --- | --- |
| **Etapa 1** | Descarga del dataset, configuración del entorno e inspección inicial de variables. | Días 1 – 2 |
| **Etapa 2** | Análisis exploratorio (EDA), generación de las 3 gráficas y análisis de valores nulos. | Días 3 – 5 |
| **Etapa 3** | Construcción de `ColumnTransformer`, pipelines y entrenamiento comparativo de modelos. | Días 6 – 8 |
| **Etapa 4** | Generación de matrices de confusión, curvas ROC, selección y exportación `.pkl`. | Días 9 – 10 |
| **Etapa 5** | Programación de la aplicación en Streamlit y pruebas locales de inferencia. | Días 11 – 13 |
| **Etapa 6** | Redacción del informe PDF (máx. 5 págs), armado del repositorio y ensayo de la demo. | Hasta el 11 de octubre |