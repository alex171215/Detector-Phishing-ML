"""
Carga, limpieza y división del dataset. Común para los 3 modelos:
así todos entrenan y evalúan EXACTAMENTE con la misma partición.
"""
import pandas as pd
from sklearn.model_selection import train_test_split

from src import config


def cargar_dataset(ruta=None) -> pd.DataFrame:
    """Lee Dataset.csv y aplica la limpieza mínima acordada."""
    ruta = ruta or config.RUTA_DATASET
    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró {ruta}. Descarguen el dataset de Kaggle y "
            f"guárdenlo como data/Dataset.csv (ver data/README.md)."
        )
    df = pd.read_csv(ruta)

    # Las URLs que son IP pura no tienen TLD → vienen nulas. Se imputan con 'none'.
    if "tld" in df.columns:
        df["tld"] = df["tld"].fillna("none")

    # TODO(equipo): ¿eliminar duplicados? df = df.drop_duplicates(subset=config.COLUMNA_URL)
    return df


def obtener_features(df: pd.DataFrame) -> list[str]:
    """Devuelve la lista de variables que entran al modelo."""
    if config.FEATURES:
        faltantes = [c for c in config.FEATURES if c not in df.columns]
        if faltantes:
            raise KeyError(f"config.FEATURES tiene columnas que no están en el dataset: {faltantes}")
        return list(config.FEATURES)

    excluir = set(config.COLUMNAS_EXCLUIDAS) | {config.COLUMNA_OBJETIVO}
    return [c for c in df.select_dtypes(include="number").columns if c not in excluir]


def separar_X_y(df: pd.DataFrame):
    features = obtener_features(df)
    return df[features], df[config.COLUMNA_OBJETIVO]


def dividir(df: pd.DataFrame):
    """Partición estratificada 80/20 compartida por todos los modelos."""
    X, y = separar_X_y(df)
    return train_test_split(
        X, y,
        test_size=config.TEST_SIZE,
        random_state=config.RANDOM_STATE,
        stratify=y,
    )
