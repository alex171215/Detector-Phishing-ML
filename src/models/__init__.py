"""
Registro de los 3 modelos del proyecto.

Cada integrante solo trabaja en SU archivo:
    logistic_regression.py  → Paul Rosero
    random_forest.py        → Alejandro Flores
    linear_svm.py           → Gloria Chushig

Cada archivo define unas constantes (NOMBRE, RESPONSABLE, ESCALAR...) y una
función construir_clasificador() que devuelve el estimador de scikit-learn.
Todo lo demás (preprocesamiento, Pipeline, evaluación, exportación, app)
ya está resuelto y es común.
"""
from sklearn.pipeline import Pipeline

from src.models import linear_svm, logistic_regression, random_forest
from src.preprocessing import construir_preprocesador

MODELOS = {
    "lr": logistic_regression,
    "rf": random_forest,
    "svm": linear_svm,
}


def obtener_modulo(clave: str):
    if clave not in MODELOS:
        raise KeyError(f"Modelo '{clave}' no existe. Opciones: {list(MODELOS)}")
    return MODELOS[clave]


def construir_pipeline(clave: str, features: list[str]) -> Pipeline:
    """Pipeline completo: preprocesador común + clasificador del integrante."""
    modulo = obtener_modulo(clave)
    return Pipeline(steps=[
        ("preprocesador", construir_preprocesador(features, escalar=modulo.ESCALAR)),
        ("modelo", modulo.construir_clasificador()),
    ])


def ruta_modelo(clave: str):
    from src import config
    return config.DIR_MODELOS / obtener_modulo(clave).ARCHIVO
