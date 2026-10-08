"""
Evaluación común: las mismas métricas y gráficos para los 3 modelos,
para que la comparación sea justa.
"""
import json

import numpy as np
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    f1_score, precision_score, recall_score, roc_auc_score, roc_curve,
)

from src import config

ETIQUETAS = ["Benigna (0)", "Phishing (1)"]


def puntajes(pipeline, X) -> np.ndarray:
    """Probabilidad de phishing (0–1) para cualquier modelo."""
    if hasattr(pipeline, "predict_proba"):
        try:
            return pipeline.predict_proba(X)[:, 1]
        except AttributeError:
            pass
    # Modelos sin predict_proba (p. ej. LinearSVC): sigmoide del margen.
    return 1.0 / (1.0 + np.exp(-pipeline.decision_function(X)))


def evaluar(pipeline, X_test, y_test, umbral: float = config.UMBRAL_PHISHING) -> dict:
    """Devuelve un diccionario con todas las métricas de la clase 1 (phishing)."""
    proba = puntajes(pipeline, X_test)
    y_pred = (proba >= umbral).astype(int)
    return {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1": float(f1_score(y_test, y_pred, zero_division=0)),
        "auc": float(roc_auc_score(y_test, proba)),
        "matriz_confusion": confusion_matrix(y_test, y_pred).tolist(),
        "reporte": classification_report(y_test, y_pred, target_names=ETIQUETAS, zero_division=0),
    }


# ------------------------------------------------------------------------------
# Gráficos (matplotlib se importa adentro para que la app no lo necesite)
# ------------------------------------------------------------------------------

def graficar_matriz_confusion(metricas: dict, titulo: str = "Matriz de Confusión"):
    import matplotlib.pyplot as plt
    import seaborn as sns

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(
        metricas["matriz_confusion"], annot=True, fmt="d", cmap="Blues", ax=ax,
        xticklabels=["Benigna predicha", "Phishing predicho"],
        yticklabels=["Benigna real", "Phishing real"],
    )
    ax.set_title(titulo)
    fig.tight_layout()
    return fig


def graficar_roc(modelos: dict, X_test, y_test, titulo: str = "Curvas ROC"):
    """modelos = {"Nombre": pipeline_entrenado, ...} → curvas superpuestas."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 5))
    for nombre, pipe in modelos.items():
        proba = puntajes(pipe, X_test)
        fpr, tpr, _ = roc_curve(y_test, proba)
        ax.plot(fpr, tpr, lw=2, label=f"{nombre} (AUC = {roc_auc_score(y_test, proba):.3f})")
    ax.plot([0, 1], [0, 1], "--", color="gray", label="Azar (AUC = 0.5)")
    ax.set_xlabel("Tasa de Falsos Positivos (FPR)")
    ax.set_ylabel("Tasa de Verdaderos Positivos (Recall)")
    ax.set_title(titulo)
    ax.legend(loc="lower right")
    fig.tight_layout()
    return fig


# ------------------------------------------------------------------------------
# Métricas guardadas (las lee la página "Modelos IA" de la app)
# ------------------------------------------------------------------------------

def leer_metricas() -> dict:
    if config.RUTA_METRICAS.exists():
        return json.loads(config.RUTA_METRICAS.read_text(encoding="utf-8"))
    return {}


def guardar_metricas(clave: str, metricas: dict):
    """Guarda/actualiza las métricas de un modelo en models/metricas.json."""
    todas = leer_metricas()
    todas[clave] = {k: v for k, v in metricas.items() if k != "reporte"}
    config.DIR_MODELOS.mkdir(exist_ok=True)
    config.RUTA_METRICAS.write_text(json.dumps(todas, indent=2, ensure_ascii=False), encoding="utf-8")
