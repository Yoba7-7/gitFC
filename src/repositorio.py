import os
import json
from pathlib import Path

REPO_PATH = Path(".gitfc")

def init_repository():
	os.makedirs(".gitfc/commits", exist_ok=True)
	os.makedirs(".gitfc/commits", exist_ok=True)

	with open(".gitfc/archivos_rastreados.json", "w") as f:
		json.dump([], f)

	with open(".gitfc/metadata.json", "w") as f:
		json.dump({}, f)

	print("Repositorio inicializado")

def show_status():
	#verifica si existe el repo
	if not REPO_PATH.exists():
		print("No existe un repositorio")
		return
	print("Repositorio activo\n")

	#Leer archivos en seguimiento
	tracked_file = REPO_PATH / "tracked_files.json"

	if tracked_file.exists():
		with open(tracked_file, "r") as f:
			tracked_files = json.load(f)
	else:
		tracked_files = []

	print(f"Archivos rastreados:  {len(tracked_files)}")

	#verificar commits
	commits_path = REPO_PATH / "commits"
	
	if commits_path.exists():
		commits = list(commits_path.iterdir())
		print(f"Commits registrados:  {len(commits)}")
	else:
		print("Sin commits aún")
