import os
import json
import shutil
import pytest
from pathlib import Path

from src.repositorio import iniciar_repositorio
from src.staging import add_file
from src.commit import crear_commit, HISTORIAL
from src.baseline import crear_baseline, BASELINE
from src.checkout import hacer_checkout


@pytest.fixture
def entorno_integracion():

    # Limpiar todo lo anterior ejecutado en el entorno
    if Path(".gitfc").exists():
        shutil.rmtree(".gitfc")

    archivo = "integracion.txt"

    if Path(archivo).exists():
        Path(archivo).unlink()

    yield archivo

    
    if Path(".gitfc").exists():
        shutil.rmtree(".gitfc")

    if Path(archivo).exists():
        Path(archivo).unlink()

@pytest.fixture(autouse=True)
def limpiar_archivos():

    yield

    # Archivos temporales
    for archivo in [
        "archivo.txt",
        "documento.txt",
        "error.txt"
    ]:
        if Path(archivo).exists():
            os.remove(archivo)

    # Repositorio temporal
    if Path(".gitfc").exists():
        shutil.rmtree(".gitfc")


def test_flujo_completo(entorno_integracion, capsys):

    archivo = entorno_integracion

    # PASO 1: INIT

    iniciar_repositorio()

    assert Path(".gitfc").exists()

        # Creación del archivo

    with open(archivo, "w") as f:
        f.write("Version 1")

    # Ejecutar add

    add_file(archivo)

    captura = capsys.readouterr()

    assert "agregado correctamente" in captura.out

    # Crear el commit

    crear_commit("Primer commit")

    captura = capsys.readouterr()

    assert "commit_001" in captura.out

    # Se crea el baseline

    crear_baseline("v1.0")

    captura = capsys.readouterr()

    assert "Baseline 'v1.0'" in captura.out

    # Verificación del historial

    with open(HISTORIAL, "r") as h:
        historial = json.load(h)

    assert len(historial) == 1
    assert historial[0]["id"] == "commit_001"

    # Modificar archivo

    with open(archivo, "w") as f:
        f.write("Version 2")

    crear_commit("Segundo commit")

    # Checkout -> Baseline
    hacer_checkout("v1.0")

    with open(archivo, "r") as f:
        contenido = f.read()

    assert contenido == "Version 1"

def test_flujo_completo_sistema(capsys):

     # 1-Inicializar repositorio
    iniciar_repositorio()

    # 2-Crear archivo
    with open("documento.txt", "w") as f:
        f.write("Version inicial")

    # 3-Agregar al staging
    add_file("documento.txt")

    # 4-Commit inicial
    crear_commit("Commit inicial")

    # 5-Crear baseline
    crear_baseline("entrega1")

    # 6-Modificar archivo
    with open("documento.txt", "w") as f:
        f.write("Version modificada")

    # 7-Segundo commit
        crear_commit("Commit actualizado")

    # 8-Verificar historial
    with open(HISTORIAL, "r") as h:
        historial = json.load(h)

    assert len(historial) == 2

    # 9-Verificar baseline
    with open(BASELINE, "r") as b:
        baselines = json.load(b)

    assert baselines["entrega1"] == "commit_001"

    # 10-Restaurar versión inicial
    hacer_checkout("entrega1")

    with open("documento.txt", "r") as f:
        contenido = f.read()

    assert contenido == "Version inicial"


#------------- PRUEBAS EDGE CASES -------------------

# Comprobar que no el sistema note el error de hacer un commit sin antes haber hecho add
def test_commit_sin_add(capsys):

    iniciar_repositorio()

    with open("error.txt", "w") as f:
        f.write("contenido")

    crear_commit("Intento inválido")

    salida = capsys.readouterr().out

    assert "No hay archivos rastreados" in salida

    with open(HISTORIAL, "r") as h:
        historial = json.load(h)

    assert len(historial) == 0

# Comprobar que no se pueda ver un archivo o versión que no existe en el sistema
def test_checkout_version_inexistente(capsys):

    iniciar_repositorio()

    hacer_checkout("version_inexistente")

    salida = capsys.readouterr().out

    assert "No se encontró la versión" in salida

#Comprobar que no se creen dos baseline con el mismo nombre
def test_baseline_duplicada():

    iniciar_repositorio()

    with open("archivo.txt", "w") as f:
        f.write("contenido")

    add_file("archivo.txt")
    crear_commit("Primer commit")

    crear_baseline("v1.0")

    # Crear la misma baseline otra vez
    crear_baseline("v1.0")

    with open(BASELINE, "r") as b:
        baselines = json.load(b)

    # Debería existir solo una entrada
    assert len(baselines) == 1

# Comprobar marcar el error cuando se hace add y luego se borra el archivo antes de hacer commit
def test_archivo_borrado_despuesDelAdd(capsys):

    iniciar_repositorio()

    with open("archivo.txt", "w") as f:
        f.write("contenido")

    add_file("archivo.txt")

    Path("archivo.txt").unlink()

    crear_commit("Commit no válido")

    salida = capsys.readouterr().out

    assert "archivo" in salida.lower()

# Intentar revisar un commit viejo después de varios commits
def test_checkout_commit_antiguo():

    # Crear repositorio 
    iniciar_repositorio()

    # Commit 1
    with open("archivo.txt", "w") as f:
        f.write("V1")

    add_file("archivo.txt")
    crear_commit("V1")

    # Obtener el ID real del primer commit
    with open(HISTORIAL, "r") as h:
        historial = json.load(h)

    primer_commit = historial[0]["id"]

    with open("archivo.txt", "w") as f:
        f.write("V2")

    crear_commit("V2")

    with open("archivo.txt", "w") as f:
        f.write("V3")

    crear_commit("V3")

    # Regresamos al primer commit
    hacer_checkout(primer_commit)

    # Verificar contenido restaurado
    with open("archivo.txt", "r") as f:
        contenido = f.read()

    assert contenido == "V1"

#Comprobar que no se hagan commits vacíos
def test_commit_vacio():

    iniciar_repositorio()

    with open("archivo.txt", "w") as f:
        f.write("contenido")

    add_file("archivo.txt")

    crear_commit("")

    with open(HISTORIAL, "r") as h:
        historial = json.load(h)

    assert len(historial) == 1
