import json
import shutil
from pathlib import Path

COMMITS_DIR = Path(".gitfc/commits")
BASELINES   = Path(".gitfc/baselines.json")


def _resolver_id(referencia):
    """
    Recibe un commit_id o un nombre de baseline y devuelve el commit_id real.
    Devuelve None si no se encuentra.
    """
    # Si ya es un commit_id directo
    if (COMMITS_DIR / referencia).exists():
        return referencia

    # Intentar resolverlo como nombre de baseline
    if BASELINES.exists():
        with open(BASELINES, "r") as b:
            baselines = json.load(b)
        if referencia in baselines:
            return baselines[referencia]

    return None


def hacer_checkout(referencia):
    if not COMMITS_DIR.exists():
        print("No existe un repositorio inicializado")
        return

    commit_id = _resolver_id(referencia)

    if commit_id is None:
        print(f"No se encontró la versión: {referencia}")
        return

    archivos_path = COMMITS_DIR / commit_id / "archivos"
    meta_path     = COMMITS_DIR / commit_id / "metadata.json"

    if not archivos_path.exists():
        print(f"El commit {commit_id} no tiene archivos guardados")
        return

    with open(meta_path, "r") as m:
        meta = json.load(m)

    archivos = list(archivos_path.iterdir())

    if not archivos:
        print(f"El commit {commit_id} no contiene archivos")
        return

    print(f"\nRegresando a {referencia} ({commit_id})...")
    print(f"Mensaje del commit: {meta['mensaje']}")
    print(f"Fecha: {meta['fecha']}\n")

    for archivo in archivos:
        destino = Path(".") / archivo.name
        shutil.copy2(archivo, destino)
        print(f"  Restaurado: {archivo.name}")

    print(f"\nCheckout completado. Tu directorio de trabajo ahora refleja {referencia}.")
    print("Los commits anteriores siguen intactos en .gitfc/commits/\n")