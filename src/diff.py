import json
import difflib
from pathlib import Path

COMMITS_DIR = Path(".gitfc/commits")
HISTORIAL   = Path(".gitfc/historial.json")
BASELINES   = Path(".gitfc/baselines.json")


def _resolver_id(referencia):
    if (COMMITS_DIR / referencia).exists():
        return referencia

    if BASELINES.exists():
        with open(BASELINES, "r") as b:
            baselines = json.load(b)
        if referencia in baselines:
            return baselines[referencia]

    return None


def _leer_archivo(commit_id, nombre_archivo):
    ruta = COMMITS_DIR / commit_id / "archivos" / nombre_archivo
    if not ruta.exists():
        return []
    with open(ruta, "r", errors="replace") as f:
        return f.readlines()


def mostrar_diff(ref1, ref2):
    if not COMMITS_DIR.exists():
        print("No existe un repositorio inicializado")
        return

    id1 = _resolver_id(ref1)
    id2 = _resolver_id(ref2)

    if id1 is None:
        print(f"No se encontró la versión: {ref1}")
        return
    if id2 is None:
        print(f"No se encontró la versión: {ref2}")
        return

    meta1_path = COMMITS_DIR / id1 / "metadata.json"
    meta2_path = COMMITS_DIR / id2 / "metadata.json"

    with open(meta1_path, "r") as m:
        meta1 = json.load(m)
    with open(meta2_path, "r") as m:
        meta2 = json.load(m)

    archivos1 = set(Path(a).name for a in meta1["archivos"])
    archivos2 = set(Path(a).name for a in meta2["archivos"])
    todos     = sorted(archivos1 | archivos2)

    print(f"\n{'='*50}")
    print(f"  DIFF: {ref1}  →  {ref2}")
    print(f"{'='*50}")

    if not todos:
        print("  Ninguna versión contiene archivos.")
        return

    for nombre in todos:
        print(f"\n--- Archivo: {nombre} ---\n")

        en_v1 = nombre in archivos1
        en_v2 = nombre in archivos2

        if en_v1 and not en_v2:
            print(f"  [Solo existe en {ref1} — eliminado en {ref2}]")
            continue
        if not en_v1 and en_v2:
            print(f"  [Solo existe en {ref2} — nuevo en {ref2}]")
            continue

        lineas1 = _leer_archivo(id1, nombre)
        lineas2 = _leer_archivo(id2, nombre)

        # Calcular líneas eliminadas y añadidas
        eliminadas = []
        añadidas   = []

        matcher = difflib.SequenceMatcher(None, lineas1, lineas2)
        for op, i1, i2, j1, j2 in matcher.get_opcodes():
            if op == "replace":
                for idx, linea in enumerate(lineas1[i1:i2], start=i1+1):
                    eliminadas.append((idx, linea.rstrip()))
                for idx, linea in enumerate(lineas2[j1:j2], start=j1+1):
                    añadidas.append((idx, linea.rstrip()))
            elif op == "delete":
                for idx, linea in enumerate(lineas1[i1:i2], start=i1+1):
                    eliminadas.append((idx, linea.rstrip()))
            elif op == "insert":
                for idx, linea in enumerate(lineas2[j1:j2], start=j1+1):
                    añadidas.append((idx, linea.rstrip()))

        if not eliminadas and not añadidas:
            print("  Sin cambios en este archivo.")
            continue

        print("  Líneas eliminadas:")
        if eliminadas:
            for num, linea in eliminadas:
                print(f"    [{num}]   {linea}")
        else:
            print("    (ninguna)")

        print()
        print("  Líneas añadidas:")
        if añadidas:
            for num, linea in añadidas:
                print(f"    [{num}]   {linea}")
        else:
            print("    (ninguna)")

    print(f"\n{'='*50}\n")