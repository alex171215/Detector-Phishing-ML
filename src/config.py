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
# TODO(equipo): confirmar con df.columns los nombres reales de estas columnas.
COLUMNAS_EXCLUIDAS = ["url", "dom", "tld"]

# Lista OFICIAL de variables que usan los 3 modelos y que calcula extractor.py.
# Deben llamarse EXACTAMENTE igual que en Dataset.csv.
# TODO(equipo): llenar después de revisar df.columns en el notebook 01.
#   Si se deja vacía, se usan todas las columnas numéricas del dataset
#   (menos label), pero entonces el extractor debe saber calcularlas todas.
FEATURES: list[str] = []

# ------------------------------------------------------------------------------
# Entrenamiento
# ------------------------------------------------------------------------------
RANDOM_STATE = 42
TEST_SIZE = 0.20
UMBRAL_PHISHING = 0.5               # probabilidad a partir de la cual se marca phishing

# Modelo que la app usa por defecto si existe su .pkl
# (se cambia por el ganador cuando terminen la comparación).
MODELO_POR_DEFECTO = "lr"
