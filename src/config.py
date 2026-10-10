"""
Configuración central del proyecto PhishGuard.

Todo lo que se comparte entre notebooks, scripts y la app vive aquí:
rutas, nombre de la columna objetivo, columnas que NO entran al modelo
y la lista oficial de variables (FEATURES).

Si cambian algo aquí, cambia para todos (notebooks, entrenamiento y app).
"""
from pathlib import Path

# ------------------------------------------------------------------------------
# Rutas
# ------------------------------------------------------------------------------
RAIZ = Path(__file__).resolve().parent.parent
DIR_DATOS = RAIZ / "data"
DIR_MODELOS = RAIZ / "models"

RUTA_DATASET = DIR_DATOS / "Dataset.csv"
RUTA_METRICAS = DIR_MODELOS / "metricas.json"

# ------------------------------------------------------------------------------
# Datos
# ------------------------------------------------------------------------------
COLUMNA_OBJETIVO = "label"          # 0 = benigna, 1 = phishing
COLUMNA_URL = "url"                 # URL cruda (solo se usa para validar el extractor)

# Columnas de texto que NUNCA deben entrar al modelo.
# (La URL completa haría que el OneHotEncoder cree una columna por cada URL.)
# Confirmado con df.columns: son las 3 columnas de texto del dataset.
COLUMNAS_EXCLUIDAS = ["url", "dom", "tld"]

# Lista OFICIAL de variables que usan los 3 modelos y que calcula extractor.py.
# Deben llamarse EXACTAMENTE igual que en Dataset.csv.
# Son las 22 variables numéricas del dataset (confirmadas con df.columns).
FEATURES: list[str] = [
    # Longitudes y estructura
    "url_len", "dom_len", "tld_len", "subdom_cnt", "path_len", "query_len",
    # Indicadores binarios (0/1)
    "is_ip", "is_https",
    # Conteos de caracteres
    "letter_cnt", "digit_cnt", "special_cnt", "eq_cnt", "qm_cnt", "amp_cnt",
    "dot_cnt", "dash_cnt", "under_cnt", "slash_cnt",
    # Proporciones y entropía
    "letter_ratio", "digit_ratio", "spec_ratio", "entropy",
]

# ------------------------------------------------------------------------------
# Entrenamiento
# ------------------------------------------------------------------------------
RANDOM_STATE = 42
TEST_SIZE = 0.20
UMBRAL_PHISHING = 0.5               # probabilidad a partir de la cual se marca phishing

# Modelo que la app usa por defecto: el ganador de la comparación (notebook 05).
# SVM gaussiano (RBF) → mejor F1 y AUC de los tres modelos.
MODELO_POR_DEFECTO = "svm_rbf"
