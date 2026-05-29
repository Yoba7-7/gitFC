import json
from pathlib import Path

BASELINE = Path(".gitfc/baselines.json")
HISTORIAL = Path(".gitfc/historial.json")

def crear_baseline(nombre):
	if not HISTORIAL.exists():
		print("No existen commits")
		return
	
	with open(HISTORIAL, "r") as h:
		historial = json.load(h)

	if not historial:
		print("No existen commits")
		return
	
	ultimo_commit = historial[-1]["id"]
	
	if BASELINE.exists():
		with open(BASELINE, "r") as b:
			baselines = json.load(b)
	else:
		baselines = {}
	
	baselines[nombre] = ultimo_commit
	
	with open(BASELINE, "w") as b:
		json.dump(baselines, b, indent=4)
	
	print(f"Baseline '{nombre}' creado en {ultimo_commit}")

def listar_baselines():
	if not BASELINE.exists():
		print("No existen baselines")
		return
	
	with open(BASELINE, "r") as b:
		baselines = json.load(b)
	
	print("\nBaselines registradas:\n")
	
	for nombre, commit in baselines.items():
		print(f"{nombre} -> {commit}")
