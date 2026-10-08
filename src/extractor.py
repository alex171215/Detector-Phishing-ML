"""
Extractor de características: convierte una URL cruda en la MISMA fila de
variables con la que se entrenaron los modelos.

Cómo funciona
-------------
Cada variable es una función pequeña registrada con @variable("nombre_columna").
El nombre debe ser EXACTAMENTE el de la columna en Dataset.csv.
extract_features_from_url() arma el DataFrame en el orden de config.FEATURES
(o del modelo cargado) y avisa claramente si falta alguna.

Para comprobar que coincide con el dataset:
    python -m scripts.validar_extractor
"""
import math
import re
import urllib.parse
from collections import Counter

import pandas as pd

from src import config

_REGISTRO = {}


def variable(nombre: str):
    """Decorador para registrar el cálculo de una columna."""
    def _registrar(func):
        _REGISTRO[nombre] = func
        return func
    return _registrar


def variables_disponibles() -> list[str]:
    return list(_REGISTRO)


def _partes(url: str):
    return urllib.parse.urlparse(url)


_PATRON_IP = re.compile(r"^[0-9]+(?:\.[0-9]+){3}$")


# ==============================================================================
# VARIABLES
# Las de abajo son las que ya existían en el proyecto. Sus nombres son
# PROVISIONALES: renómbrenlas al nombre exacto de la columna del dataset
# (p. ej. 'url_length' → 'url_len') y agreguen las que falten hasta cubrir
# las 22. Revisen también CÓMO las calcula el dataset (¿con o sin 'http://'?,
# ¿qué cuenta como carácter especial?, ¿la entropía es de Shannon?).
# ==============================================================================

@variable("url_length")            # TODO(equipo): nombre real en el dataset
def _url_length(url: str):
    return len(url)


@variable("domain_length")         # TODO(equipo): nombre real en el dataset
def _domain_length(url: str):
    return len(_partes(url).netloc)


@variable("is_ip")                 # TODO(equipo): nombre real en el dataset
def _is_ip(url: str):
    return int(bool(_PATRON_IP.match(_partes(url).hostname or "")))


@variable("is_https")              # TODO(equipo): nombre real en el dataset
def _is_https(url: str):
    return int(_partes(url).scheme.lower() == "https")


@variable("digit_ratio")           # TODO(equipo): nombre real en el dataset
def _digit_ratio(url: str):
    return sum(c.isdigit() for c in url) / len(url) if url else 0.0


@variable("special_char_count")    # TODO(equipo): nombre real en el dataset
def _special_char_count(url: str):
    return sum(not c.isalnum() for c in url)


@variable("entropy")               # TODO(equipo): confirmar nombre y fórmula
def _entropy(url: str):
    if not url:
        return 0.0
    n = len(url)
    return -sum((k / n) * math.log2(k / n) for k in Counter(url).values())


# TODO(equipo): agregar aquí el resto de variables del dataset, por ejemplo:
# @variable("nombre_exacto_columna")
# def _mi_variable(url: str):
#     return ...


# ==============================================================================
# API pública
# ==============================================================================

def extract_features_from_url(url: str, columnas: list[str] | None = None) -> pd.DataFrame:
    """
    Devuelve un DataFrame de 1 fila con las columnas pedidas, en ese orden.
    columnas=None → usa config.FEATURES (o todas las registradas si está vacía).
    """
    columnas = list(columnas or config.FEATURES or _REGISTRO)
    faltantes = [c for c in columnas if c not in _REGISTRO]
    if faltantes:
        raise KeyError(
            "extractor.py no sabe calcular estas columnas que el modelo necesita: "
            f"{faltantes}. Agréguenlas con @variable('nombre')."
        )
    return pd.DataFrame([{c: _REGISTRO[c](url) for c in columnas}], columns=columnas)


def resumen_url(url: str) -> dict:
    """Datos legibles para mostrar en la app (no los usa el modelo)."""
    p = _partes(url)
    host = p.hostname or ""
    return {
        "host": host,
        "https": p.scheme.lower() == "https",
        "es_ip": bool(_PATRON_IP.match(host)),
        "longitud": len(url),
        "especiales": sum(not c.isalnum() for c in url),
    }


if __name__ == "__main__":
    prueba = "http://secure-update-banco.com/login?id=82349"
    print("URL:", prueba)
    print(extract_features_from_url(prueba).T)
