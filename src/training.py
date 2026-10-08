"""
Flujo de entrenamiento común. Lo usan los notebooks y scripts/entrenar.py.

    entrenar_y_evaluar("rf")  → entrena con 80%, evalúa en 20%, guarda métricas
    exportar_final("rf")      → reentrena con 100% y guarda models/modelo_rf.pkl
"""
import joblib

from src import config, data, evaluation
from src.models import construir_pipeline, obtener_modulo, ruta_modelo


def entrenar_y_evaluar(clave: str, df=None, guardar: bool = True):
    """Devuelve (pipeline_entrenado, metricas, (X_test, y_test))."""
    df = data.cargar_dataset() if df is None else df
    X_train, X_test, y_train, y_test = data.dividir(df)

    pipeline = construir_pipeline(clave, list(X_train.columns))
    pipeline.fit(X_train, y_train)

    metricas = evaluation.evaluar(pipeline, X_test, y_test)
    metricas["modelo"] = obtener_modulo(clave).NOMBRE
    if guardar:
        evaluation.guardar_metricas(clave, metricas)
    return pipeline, metricas, (X_test, y_test)


def exportar_final(clave: str, df=None):
    """Reentrena con el 100% de los datos y exporta el .pkl que usa la app."""
    df = data.cargar_dataset() if df is None else df
    X, y = data.separar_X_y(df)

    pipeline = construir_pipeline(clave, list(X.columns))
    pipeline.fit(X, y)

    config.DIR_MODELOS.mkdir(exist_ok=True)
    ruta = ruta_modelo(clave)
    joblib.dump(pipeline, ruta)
    return ruta
