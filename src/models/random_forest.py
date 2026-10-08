"""
Modelo 2 — Random Forest
Responsable: Alejandro Flores
"""
from src import config  # noqa: F401  (usar config.RANDOM_STATE)

CLAVE = "rf"
NOMBRE = "Random Forest"
RESPONSABLE = "Alejandro Flores"
ARCHIVO = "modelo_rf.pkl"     # se guarda en models/
ESCALAR = False               # los árboles no necesitan escalado


def construir_clasificador():
    """Devuelve el clasificador SIN entrenar (el Pipeline lo arma models/__init__.py)."""
    # TODO(Alejandro): implementar. Debe devolver un estimador de scikit-learn
    # con .predict_proba(), por ejemplo un RandomForestClassifier.
    # Recordar random_state=config.RANDOM_STATE y pensar en el desbalance (class_weight).
    raise NotImplementedError("Random Forest pendiente (Alejandro)")
