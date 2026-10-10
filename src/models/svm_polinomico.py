"""
Modelo 3 — SVM con kernel polinómico
Responsable: Alejandro Flores
"""
from sklearn.svm import SVC

from src import config

CLAVE = "svm_poly"
NOMBRE = "SVM polinómico"
RESPONSABLE = "Alejandro Flores"
ARCHIVO = "modelo_svm_poly.pkl"   # se guarda en models/
ESCALAR = True                    # los SVM son sensibles a la escala → StandardScaler


def construir_clasificador():
    """Devuelve el clasificador SIN entrenar (el Pipeline lo arma models/__init__.py)."""
    return SVC(
        kernel="poly",
        degree=3,                  # polinomio de grado 3: capta interacciones entre hasta 3 variables
        coef0=1.0,                 # incluye también los términos de grado 1 y 2 (kernel no homogéneo)
        C=1.0,                     # mismo C que el SVM lineal, para comparar en igualdad de condiciones
        gamma="scale",
        class_weight="balanced",   # compensa el desbalance (~14 % de phishing)
        probability=True,          # probabilidades 0–100 % (escalado de Platt) para la app
        cache_size=1000,           # MB de caché del kernel: acelera el entrenamiento
        random_state=config.RANDOM_STATE,
    )
