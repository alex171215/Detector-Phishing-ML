"""
Modelo 2 — Random Forest
Responsable: Alejandro Flores
"""
from sklearn.ensemble import RandomForestClassifier

from src import config

CLAVE = "rf"
NOMBRE = "Random Forest"
RESPONSABLE = "Alejandro Flores"
ARCHIVO = "modelo_rf.pkl"     # se guarda en models/
ESCALAR = False               # los árboles no necesitan escalado


def construir_clasificador():
    """Devuelve el clasificador SIN entrenar (el Pipeline lo arma models/__init__.py)."""
    return RandomForestClassifier(
        n_estimators=100,            # 100 árboles: buen equilibrio entre rendimiento y tiempo
        class_weight="balanced",     # compensa el desbalance (~14 % de phishing)
        max_depth=20,                # limita la profundidad → menos sobreajuste y un .pkl liviano
        min_samples_leaf=2,          # evita hojas con una sola URL (memorizar casos aislados)
        n_jobs=-1,                   # usa todos los núcleos del procesador
        random_state=config.RANDOM_STATE,
    )
