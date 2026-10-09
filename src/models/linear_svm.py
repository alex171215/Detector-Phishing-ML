"""
Modelo 3 — SVM lineal
Responsable: Gloria Chushig
"""
from src import config  # noqa: F401  (usar config.RANDOM_STATE)

from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC

CLAVE = "svm"
NOMBRE = "SVM lineal"
RESPONSABLE = "Gloria Chushig"
ARCHIVO = "modelo_svm.pkl"    # se guarda en models/
ESCALAR = True                # SVM es sensible a la escala → StandardScaler


def construir_clasificador():
    clasificador = LinearSVC(
        C=1.0,
        class_weight="balanced",
        random_state=config.RANDOM_STATE,
        max_iter=5000,
    )
    return CalibratedClassifierCV(
        estimator=clasificador,
        method="sigmoid",
        cv=5,
    )
