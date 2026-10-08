"""
Preprocesamiento común (ColumnTransformer).

Todas las variables que entran al modelo son numéricas (las columnas de texto
se excluyen en config.COLUMNAS_EXCLUIDAS), así que aquí solo se escalan.
"""
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler


def construir_preprocesador(features: list[str], escalar: bool = True) -> ColumnTransformer:
    """
    escalar=True  → StandardScaler (necesario para Regresión Logística y SVM lineal).
    escalar=False → passthrough (los árboles / Random Forest no lo necesitan).
    """
    transformador = StandardScaler() if escalar else "passthrough"
    return ColumnTransformer(
        transformers=[("num", transformador, list(features))],
        remainder="drop",
    )
