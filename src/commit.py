import json
import shutil
from pathlib import Path
from datetime import datetime

ARCHIVO_RASTREADO = Path(".gitfc/archivos_rastreados.json")
COMMITS_DIR = Path(".gitfc/commits")
HISTORIAL = Path(".gitfc/historial.json")

def crear_commit(mensaje):
	if not Path(".gitfc").exists():
		print("Repositorio no inicializado")
		return

	with open(ARCHIVO_RASTREADO, "r") as a:
		rastreo = json.load(a)
	
	if not rastreo:
		print("No hay archivos rastreados")
		return

	conteo = len(list(COMMITS_DIR.iterdir())) + 1
	id = f"commit_{conteo:03}"
	commit_path = COMMITS_DIR / id
	archivos_path = commit_path / "archivos"
	
	archivos_path.mkdir(parents=True, exist_ok=True)
	copias = []
	
	for archivo in rastreo:
		src = Path(archivo)
		
		if src.exists():
			destino = archivos_path / src.name
			shutil.copy2(src, destino)
			copias.append(archivo)
	
	metadatos = {
		"id" : id,
		"mensaje" : mensaje,
		"fecha" : str(datetime.now()),
		"archivos" : copias
	}

	with open(commit_path / "metadata.json", "w") as a:
		json.dump(metadatos, a, indent=4)
	
	if HISTORIAL.exists():
		with open(HISTORIAL, "r") as h:
			historial = json.load(h)
	else:
		historial = []
	historial.append(metadatos)
	
	with open(HISTORIAL, "w") as h:
		json.dump(historial, h, indent=4)
	
	print(f"Commit {id} creado correctamente")
