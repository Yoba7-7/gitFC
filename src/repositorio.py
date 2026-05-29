import os
import json
from pathlib import Path

REPO_PATH = Path(".gitfc")

def iniciar_repositorio():
	os.makedirs(".gitfc/commits", exist_ok=True)
	os.makedirs(".gitfc/staging", exist_ok=True)

	with open(".gitfc/archivos_rastreados.json", "w") as a:
		json.dump([], a)

	with open(".gitfc/metadata.json", "w") as m:
		json.dump({}, m)

	with open(".gitfc/historial.json", "w") as h:
		json.dump([], h)

	with open(".gitfc/baselines.json", "w") as b:
		json.dump({}, b)

	print("Repositorio inicializado")

def existe_repo():
	return REPO_PATH.exists()
