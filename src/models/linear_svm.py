"""
Modelo 3 — SVM lineal
Responsable: Gloria Chushig
"""
from src import config  # noqa: F401  (usar config.RANDOM_STATE)

CLAVE = "svm"
NOMBRE = "SVM lineal"
RESPONSABLE = "Gloria Chushig"
ARCHIVO = "modelo_svm.pkl"    # se guarda en models/
ESCALAR = True                # SVM es sensible a la escala → StandardScaler


def construir_clasificador():
    """Devuelve el clasificador SIN entrenar (el Pipeline lo arma models/__init__.py)."""
    # TODO(Gloria): implementar. Debe devolver un estimador de scikit-learn.
    #
    # Ojo: LinearSVC NO tiene .predict_proba(). La app igual funciona (convierte
    # el decision_function a 0–1), pero para tener probabilidades reales y una
    # comparación justa con los otros modelos conviene envolverlo en
    # sklearn.calibration.CalibratedClassifierCV.
    raise NotImplementedError("SVM lineal pendiente (Gloria)")
