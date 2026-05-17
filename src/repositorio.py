import os
import json
from pathlib import Path

REPO_PATH = Path(".gitfc")

def iniciar_repositorio():
	os.makedirs(".gitfc/commits", exist_ok=True)
	os.makedirs(".gitfc/commits", exist_ok=True)

	with open(".gitfc/archivos_rastreados.json", "w") as f:
		json.dump([], f)

	with open(".gitfc/metadata.json", "w") as f:
		json.dump({}, f)

	print("Repositorio inicializado")

def existe_repo():
	return REPO_PATH.exists()
