# Plan de implementación final (entrega: 11 de octubre)

- [x] **Bloque 1 · Preparar:** sincronizar `alejo` con `main` (SVM de Gloria) y conseguir `Dataset.csv`.
- [x] **Bloque 2 · Definir los datos:** mover `Dataset.csv` a `data/`, decidir duplicados en `src/data.py`, llenar `FEATURES` y `COLUMNAS_EXCLUIDAS` en `src/config.py`, ejecutar el notebook `01` (gráfico 3 + interpretaciones).
- [x] **Bloque 3 · Extractor:** `src/extractor.py` con las 22 variables y nombres reales hasta que `python -m scripts.validar_extractor` salga todo en ✅; revisar `http://` en `src/predictor.py`.
- [x] **Bloque 4 · Modelos:** `random_forest.py` + notebook `03`; ejecutar notebook `02` (LR); volver a ejecutar notebook `04` (SVM) si cambiaron datos/columnas.
- [x] **Bloque 5 · Comparación:** notebook `05` (tabla, ROC superpuestas, ganador); `config.MODELO_POR_DEFECTO` y `models/metricas.json`.
- [x] **Bloque 6 · App y limpieza:** probar `streamlit run app.py` con URL benigna y sospechosa, capturas; notebooks sin errores y sin `TODO`.
- [ ] **Bloque 7 · Entregables:** informe PDF (máx. 5 págs.), commit + merge a `main` + README, ensayo de la demo (Render opcional).
