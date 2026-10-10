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
import tldextract

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

# tldextract separa subdominio / dominio / sufijo usando la lista oficial de
# sufijos públicos (Public Suffix List). Así 'www.rmit.edu.au' se separa en
# subdominio='www', dominio='rmit', sufijo='edu.au', igual que en el dataset.
# suffix_list_urls=() → usa la copia que trae la librería (no necesita Internet).
_TLD = tldextract.TLDExtract(suffix_list_urls=())


def _dominio(url: str):
    """Devuelve (dominio_registrado, tld, n_subdominios, es_ip) como en el dataset."""
    host = (_partes(url).hostname or "").lower()
    if _PATRON_IP.match(host):
        return host, "", 0, 1           # IP pura: sin TLD ni subdominios
    e = _TLD(url)
    dominio = ".".join(p for p in (e.domain, e.suffix) if p)
    n_sub = len(e.subdomain.split(".")) if e.subdomain else 0
    return dominio, e.suffix, n_sub, 0


def _contar(url: str, condicion) -> int:
    return sum(1 for c in url if condicion(c))


def _ratio(cantidad: int, url: str) -> float:
    return cantidad / len(url) if url else 0.0


def _es_especial(c: str) -> bool:
    return not c.isalnum()          # todo lo que no es letra ni número (':', '/', '.', '-', ...)


# ==============================================================================
# VARIABLES (22) · nombres EXACTOS de las columnas de Dataset.csv
# Todas se calculan sobre la URL completa, incluido el esquema 'http(s)://'.
# Validado con: python -m scripts.validar_extractor  → 22/22 ✅
# ==============================================================================

# --- Longitudes y estructura ---------------------------------------------------
@variable("url_len")
def _url_len(url: str):
    return len(url)


@variable("dom_len")
def _dom_len(url: str):
    return len(_dominio(url)[0])


@variable("tld_len")
def _tld_len(url: str):
    return len(_dominio(url)[1])


@variable("subdom_cnt")
def _subdom_cnt(url: str):
    return _dominio(url)[2]


@variable("path_len")
def _path_len(url: str):
    return len(_partes(url).path)


@variable("query_len")
def _query_len(url: str):
    return len(_partes(url).query)


# --- Indicadores binarios ------------------------------------------------------
@variable("is_ip")
def _is_ip(url: str):
    return _dominio(url)[3]


@variable("is_https")
def _is_https(url: str):
    return int(_partes(url).scheme.lower() == "https")


# --- Conteos de caracteres -----------------------------------------------------
@variable("letter_cnt")
def _letter_cnt(url: str):
    return _contar(url, str.isalpha)


@variable("digit_cnt")
def _digit_cnt(url: str):
    return _contar(url, str.isdigit)


@variable("special_cnt")
def _special_cnt(url: str):
    return _contar(url, _es_especial)


@variable("eq_cnt")
def _eq_cnt(url: str):
    return url.count("=")


@variable("qm_cnt")
def _qm_cnt(url: str):
    return url.count("?")


@variable("amp_cnt")
def _amp_cnt(url: str):
    return url.count("&")


@variable("dot_cnt")
def _dot_cnt(url: str):
    return url.count(".")


@variable("dash_cnt")
def _dash_cnt(url: str):
    return url.count("-")


@variable("under_cnt")
def _under_cnt(url: str):
    return url.count("_")


@variable("slash_cnt")
def _slash_cnt(url: str):
    return url.count("/")


# --- Proporciones y entropía ---------------------------------------------------
@variable("letter_ratio")
def _letter_ratio(url: str):
    return _ratio(_letter_cnt(url), url)


@variable("digit_ratio")
def _digit_ratio(url: str):
    return _ratio(_digit_cnt(url), url)


@variable("spec_ratio")
def _spec_ratio(url: str):
    return _ratio(_special_cnt(url), url)


@variable("entropy")
def _entropy(url: str):
    """Entropía de Shannon (bits por carácter) de la URL completa."""
    if not url:
        return 0.0
    n = len(url)
    return -sum((k / n) * math.log2(k / n) for k in Counter(url).values())


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
        "especiales": _special_cnt(url),
    }


if __name__ == "__main__":
    prueba = "http://secure-update-banco.com/login?id=82349"
    print("URL:", prueba)
    print(extract_features_from_url(prueba).T)
