"""
Interfaz única entre la app y los modelos.

La app SOLO usa este archivo:
    modelos_disponibles()          → {clave: nombre} de los .pkl que existen
    predecir_url(url, clave=None)  → Prediccion(...)

Si no hay ningún .pkl entrenado, usa un motor heurístico de respaldo para
que la app nunca se rompa.
"""
from dataclasses import dataclass, field

import joblib
import numpy as np

from src import config
from src.extractor import extract_features_from_url, resumen_url
from src.models import MODELOS, ruta_modelo

PALABRAS_SENSIBLES = ["login", "verify", "secure", "account", "update", "bank",
                      "banco", "pago", "free", "bonus", "signin"]

_cache = {}


@dataclass
class Prediccion:
    url: str
    probabilidad: float              # probabilidad de phishing 0–1
    es_phishing: bool
    motor: str                       # nombre del modelo o "Heurístico"
    resumen: dict = field(default_factory=dict)
    palabras_sensibles: list = field(default_factory=list)
    error: str | None = None         # detalle técnico si el modelo falló


def normalizar_url(url: str) -> str:
    url = (url or "").strip()
    # TODO(equipo): verificar si las URLs del dataset traen 'http://'. Si NO lo
    # traen, aquí habría que quitarlo para que el extractor calcule igual.
    return url if "://" in url else "http://" + url


def modelos_disponibles() -> dict:
    """Modelos cuyo .pkl ya existe en models/ → {clave: nombre legible}."""
    return {c: m.NOMBRE for c, m in MODELOS.items() if ruta_modelo(c).exists()}


def cargar_modelo(clave: str):
    if clave not in _cache:
        _cache[clave] = joblib.load(ruta_modelo(clave))
    return _cache[clave]


def _probabilidad(pipeline, X) -> float:
    if hasattr(pipeline, "predict_proba"):
        try:
            return float(pipeline.predict_proba(X)[0][1])
        except AttributeError:
            pass
    margen = float(np.ravel(pipeline.decision_function(X))[0])
    return 1.0 / (1.0 + np.exp(-margen))


def _columnas_del_modelo(pipeline):
    return list(getattr(pipeline, "feature_names_in_", [])) or None


def _heuristica(resumen: dict, n_palabras: int) -> float:
    score = 10
    if not resumen["https"]:
        score += 25
    if resumen["es_ip"]:
        score += 35
    if resumen["longitud"] > 60:
        score += 15
    score += n_palabras * 15
    if resumen["especiales"] > 8:
        score += 10
    return min(max(score / 100.0, 0.01), 0.99)


def predecir_url(url: str, clave: str | None = None) -> Prediccion:
    url = normalizar_url(url)
    resumen = resumen_url(url)
    palabras = [w for w in PALABRAS_SENSIBLES if w in url.lower()]

    disponibles = modelos_disponibles()
    if clave is None:
        clave = config.MODELO_POR_DEFECTO if config.MODELO_POR_DEFECTO in disponibles \
            else next(iter(disponibles), None)

    error = None
    if clave in disponibles:
        try:
            pipeline = cargar_modelo(clave)
            X = extract_features_from_url(url, columnas=_columnas_del_modelo(pipeline))
            prob = _probabilidad(pipeline, X)
            return Prediccion(url, prob, prob >= config.UMBRAL_PHISHING,
                              disponibles[clave], resumen, palabras)
        except Exception as ex:  # el modelo existe pero el extractor no coincide
            error = f"{type(ex).__name__}: {ex}"

    prob = _heuristica(resumen, len(palabras))
    motor = "Heurístico léxico" + (" (error en el modelo)" if error else " (sin modelo entrenado)")
    return Prediccion(url, prob, prob >= config.UMBRAL_PHISHING, motor, resumen, palabras, error)
