"""
Comprueba que src/extractor.py calcula las variables IGUAL que el dataset.
Es la prueba más importante antes de conectar un modelo a la app.

Uso (desde la raíz del proyecto):
    python -m scripts.validar_extractor            # 200 filas al azar
    python -m scripts.validar_extractor 1000
"""
import sys

import numpy as np

from src import config, data
from src.extractor import extract_features_from_url, variables_disponibles


def main(n: int = 200):
    df = data.cargar_dataset()
    features = data.obtener_features(df)

    print("Columnas del dataset:\n ", list(df.columns))
    print(f"\nVariables que usará el modelo ({len(features)}):\n ", features)

    faltan = [c for c in features if c not in variables_disponibles()]
    sobran = [c for c in variables_disponibles() if c not in features]
    if sobran:
        print(f"\nℹ️  En el extractor pero NO en el modelo (renombrar o borrar): {sobran}")
    if faltan:
        print(f"\n❌ El extractor aún no calcula: {faltan}")
        print("   Agréguenlas en src/extractor.py con @variable('nombre').")
        return 1

    if config.COLUMNA_URL not in df.columns:
        print(f"\n⚠️  No existe la columna '{config.COLUMNA_URL}' para comparar.")
        return 1

    muestra = df.sample(min(n, len(df)), random_state=config.RANDOM_STATE)
    errores = {c: 0 for c in features}
    ejemplos = {}
    for _, fila in muestra.iterrows():
        calc = extract_features_from_url(str(fila[config.COLUMNA_URL]), columnas=features).iloc[0]
        for c in features:
            if not np.isclose(float(calc[c]), float(fila[c]), atol=1e-3):
                errores[c] += 1
                ejemplos.setdefault(c, (fila[config.COLUMNA_URL], fila[c], calc[c]))

    print(f"\nComparación sobre {len(muestra)} URLs:")
    for c in features:
        estado = "✅" if errores[c] == 0 else f"❌ {errores[c]} diferencias"
        print(f"  {c:<28} {estado}")
        if c in ejemplos:
            u, esperado, obtenido = ejemplos[c]
            print(f"      ej: {u[:70]}  dataset={esperado}  extractor={obtenido}")

    ok = all(v == 0 for v in errores.values())
    print("\n✅ Extractor alineado con el dataset." if ok else "\n❌ Corrijan las variables marcadas.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 200))
