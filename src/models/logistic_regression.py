"""
Modelo 1 — Regresión Logística
Responsable: Paul Rosero
"""
from sklearn.linear_model import LogisticRegression

from src import config

CLAVE = "lr"
NOMBRE = "Regresión Logística"
RESPONSABLE = "Paul Rosero"
ARCHIVO = "modelo_lr.pkl"     # se guarda en models/
ESCALAR = True                # modelo lineal → necesita StandardScaler


def construir_clasificador():
    """Devuelve el clasificador SIN entrenar (el Pipeline lo arma models/__init__.py)."""
    # Configuración del plan de acción: lbfgs con regularización L2 por defecto (C=1.0)
    # y class_weight="balanced" para compensar el desbalance de clases.
    return LogisticRegression(
        solver="lbfgs",
        max_iter=1000,
        class_weight="balanced",
        random_state=config.RANDOM_STATE,
    )
