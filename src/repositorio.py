'''
En esta clase se va a implementar todo lo relacionado con el estado 
general del repo
- init_repository
- show_status
- add_file

Borrar o mejorar este comentario ya en entrega final
'''


import os
import json
from pathlib import Path

REPO_PATH = Path(".gitfc")
TRACKED_FILES = REPO_PATH / "tracked_files.json"
METADATA = REPO_PATH / "metadata.json"


def init_repository():
	# Antes de crear un repo se verifica que no haya uno ya creado 
	if REPO_PATH.exists():
		print("Ya existe un repositorio en este directorio")
		return
	
	os.makedirs(REPO_PATH / "commits", exist_ok=True)
	os.makedirs(REPO_PATH / "baselines", exist_ok=True)

    # Se crean dos archivos JSON iniciales
	# tracked_files.json va a almacenar archivos rastreados 
	# metadata.json va a almacenar los commits creados  
	with open(TRACKED_FILES, "w") as f:
		json.dump([], f)

	with open(METADATA, "w") as f:
		json.dump({"total_commits": 0}, f)

	print("Repositorio inicializado")

# Función para agregar un nuevo archivo
def add_file(filepath):
	if not REPO_PATH.exists():
		print("No hay repositorio. Usa: python main.py init")
		return
	
	path = Path(filepath)
	if not path.exists():
		print(f"Archivo no encontrado: {filepath}")
		return
	
	with open(TRACKED_FILES, "r") as f:
		tracked = json.load(f)

    # si el archivoo ya está en la lista no lo agrega de nuevo, esto para evitar duplicados 
	if str(path) in tracked:
		print(f"El archivo ya está en seguimiento: {filepath}")
		return
	
	#Agrega el arccchivo a la lista y lo guarda en el json
	tracked.append(str(path))
	with open(TRACKED_FILES, "w") as f:
		json.dump(tracked, f, indent=2)


def show_status():
    # verifica si existe el repo
    if not REPO_PATH.exists():
        print("No existe un repositorio. Usa: python main.py init")
        return

    print("Repositorio activo\n")

    with open(TRACKED_FILES, "r") as f:
        tracked = json.load(f)

    print(f"Archivos rastreados: {len(tracked)}")

    for archivo in tracked:
        print(f"  - {archivo}")

    commits_path = REPO_PATH / "commits"
    commits = [c for c in commits_path.iterdir() if c.is_dir()]

    print(f"Commits registrados: {len(commits)}")
