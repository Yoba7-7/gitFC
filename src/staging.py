import json
from pathlib import Path

ARCHIVO_RASTREADO = Path(".gitfc/archivos_rastreados.json")

def add_file(nombre):
	if not  Path(".gitfc").exists():
		print("Repositorio no inicializado")
		return

	if not Path(nombre).exists():
		print("El archivo no existe")
		return

	with open(ARCHIVO_RASTREADO, "r") as a:
		rastreo = json.load(a)

	if nombre in rastreo:
		print("EL archivo ya esta siendo rastreado")
		return

	rastreo.append(nombre)
	
	with open(ARCHIVO_RASTREADO, "w") as a:
		json.dump(rastreo, a, indent=4)
	
	print(f"{nombre} agregado correctamente. ")
