import json
from pathlib import Path

#ruta del archivo donde se guarda el historial
HISTORIAL = Path(".gitfc/historial.json")

def cargar_historial():
	'''
	Carga el historial completo desde historial.json
	'''
	if not HISTORIAL.exists():
		return []
	
	with open(HISTORIAL, "r") as h:
		return json.load(h)

def mostrar_historial():
	'''
	Muestra todos los commits registrados
	'''

	historial = cargar_historial()

	if not historial:
		print("No hay commits registrados")
		return
	print("\n==== HISTORIAL DE COMMITS ====\n")
	for commit in historial:
	
		print(f"ID:  {commit['id']}")
		print(f"Mensaje: {commit['mensaje']}")
		print(f"Fecha: {commit['fecha']}")
		
		print("Archivos: ")
		
		for archivo in commit["archivos"]:
			print(f" - {archivo}")
		
		print("\n------------------------------\n")

def obtener_ultimo_commit():
	'''
	regresa ultimo commit realizado
	'''
	
	historial = cargar_historial()
	
	if not historial:
		return None
	return historial[-1]
