"""
Entrena, evalúa y exporta un modelo desde la terminal (alternativa al notebook).

Uso (desde la raíz del proyecto):
    python -m scripts.entrenar lr          # Paul
    python -m scripts.entrenar rf          # Alejandro
    python -m scripts.entrenar svm         # Gloria
    python -m scripts.entrenar todos
"""
import sys

from src import data
from src.models import MODELOS
from src.training import entrenar_y_evaluar, exportar_final


def main(claves):
    df = data.cargar_dataset()
    for clave in claves:
        print(f"\n=== {MODELOS[clave].NOMBRE} ({MODELOS[clave].RESPONSABLE}) ===")
        try:
            _, m, _ = entrenar_y_evaluar(clave, df)
        except NotImplementedError as ex:
            print(f"  ⏭  Saltado: {ex}")
            continue
        print(m["reporte"])
        print(f"  AUC = {m['auc']:.4f}")
        print(f"  ✔ Exportado: {exportar_final(clave, df)}")


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "todos"
    if arg != "todos" and arg not in MODELOS:
        sys.exit(f"Opciones: {list(MODELOS)} o 'todos'")
    main(list(MODELOS) if arg == "todos" else [arg])
