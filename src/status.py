import json
from pathlib import Path

REPO_PATH = Path(".gitfc")
ARCHIVOS_RASTREADOS = Path(".git/archivos_rastreados.json")
HISTORIAL = Path(".gitfc/historial.json")


def mostrar_status():
	verificar_repo()
	archivos_rastreados()
	verificar_commits()
	archivos_en_repo()

def verificar_repo():
	'''
	Se hace una revisión para verficar si un repositorio
	(directorio .gitfc) se ha creado o no se ha creado
	'''
	estado = ""
	if not REPO_PATH.exists():
		print("No existe un repositorio")
		estado = "No existe un repositorio"
		return estado
	print("Repositorio activo")
	estado = "Repositorio activo"
	return estado

def archivos_rastreados():
	'''
	Revisa la carpeta de commits del repositorio para 
	llevar el siguimiento de los commits registrados
	'''
	archivo_rastreado = REPO_PATH / "archivos_rastreados.json"
	
	if archivo_rastreado.exists():
		with open(archivo_rastreado, "r") as a:
			archs_rastreados = json.load(a)
	else:
		archs_rastreados = []
	
	print(f"Archivos rastreados: {len(archs_rastreados)}")

def verificar_commits():
	commits_path = REPO_PATH / "commits"
	
	if commits_path.exists():
		commits = list(commits_path.iterdir())
		print(f"Commits registrados: {len(commits)}")
	else:
		print("Sin commits aun")

def archivos_en_repo():
	archivos = [
		a.name for a in Path(".").iterdir()
		if a.is_file() and a.name != "main.py"
	]

	print("\nArchivos en el repositorio: ")
	
	for archivo in archivos:
		print(f"- {archivo}")
