"""
Modelo 3 — SVM con kernel gaussiano (RBF)
Responsable: Alejandro Flores
"""
from sklearn.svm import SVC

from src import config

CLAVE = "svm_rbf"
NOMBRE = "SVM gaussiano (RBF)"
RESPONSABLE = "Alejandro Flores"
ARCHIVO = "modelo_svm_rbf.pkl"    # se guarda en models/
ESCALAR = True                    # los SVM son sensibles a la escala → StandardScaler


def construir_clasificador():
    """Devuelve el clasificador SIN entrenar (el Pipeline lo arma models/__init__.py)."""
    return SVC(
        kernel="rbf",              # kernel gaussiano: K(x, x') = exp(-gamma · ||x − x'||²)
        C=1.0,                     # mismo C que el SVM lineal, para comparar en igualdad de condiciones
        gamma="scale",             # gamma = 1 / (n_variables · varianza de X)
        class_weight="balanced",   # compensa el desbalance (~14 % de phishing)
        probability=True,          # probabilidades 0–100 % (escalado de Platt) para la app
        cache_size=1000,           # MB de caché del kernel: acelera el entrenamiento
        random_state=config.RANDOM_STATE,
    )
