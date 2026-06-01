import os
import json
import shutil
import pytest
from pathlib import Path

# Importamos la función y las constantes de su código
from src.commit import crear_commit, ARCHIVO_RASTREADO, COMMITS_DIR, HISTORIAL

@pytest.fixture
def entorno_commit():
    """PREPARAR el entorno falso para las pruebas de commit"""
    test_dir = Path(".gitfc")
    archivo_prueba = "archivo_prueba_commit.txt"
    
    # 1. Respaldamos el .gitfc original si existe
    gitfc_existe = test_dir.exists()
    if gitfc_existe:
        os.rename(test_dir, ".gitfc_backup")
        
    #Creamos la estructura base del repositorio
    test_dir.mkdir()
    COMMITS_DIR.mkdir()
    
    #Iniciamos el JSON de archivos rastreados vacío por defecto
    with open(ARCHIVO_RASTREADO, "w") as f:
        json.dump([], f)
        
    #Creamos un archivo real para simular los cambios del usuario
    with open(archivo_prueba, "w") as f:
        f.write("Contenido para el commit")
        
    yield archivo_prueba
    
    """LIMPIAR todo al terminar cada prueba"""
    if test_dir.exists():
        shutil.rmtree(test_dir)
    if Path(archivo_prueba).exists():
        os.remove(archivo_prueba)
        
    # Restauramos el original
    if gitfc_existe:
        os.rename(".gitfc_backup", test_dir)


# --- INICIAN LAS PRUEBAS ---

def test_commit_sin_repo(entorno_commit, capsys):
    # Borramos la carpeta para simular el error
    shutil.rmtree(".gitfc")
    
    crear_commit("Mensaje de prueba")
    
    captura = capsys.readouterr()
    assert "Repositorio no inicializado" in captura.out

def test_commit_sin_archivos_rastreados(entorno_commit, capsys):
    # El fixture ya deja archivos_rastreados.json vacío, así que probamos directo
    crear_commit("Mensaje de prueba")
    
    captura = capsys.readouterr()
    assert "No hay archivos rastreados" in captura.out

def test_commit_exitoso(entorno_commit, capsys):
    archivo_prueba = entorno_commit
    
    #Agregamos el archivo al rastreo (simulando que el usuario hizo 'add')
    with open(ARCHIVO_RASTREADO, "w") as f:
        json.dump([archivo_prueba], f)
        
    #Hacemos el commit
    crear_commit("Mi primer commit")
    
    #El mensaje de éxito en consola
    captura = capsys.readouterr()
    assert "Commit commit_001 creado correctamente" in captura.out
    
    #El archivo se copió adentro de la carpeta del commit
    ruta_archivo_copiado = COMMITS_DIR / "commit_001" / "archivos" / archivo_prueba
    assert ruta_archivo_copiado.exists()
    
    #Se creó el historial correctamente
    assert HISTORIAL.exists()
    with open(HISTORIAL, "r") as h:
        historial = json.load(h)
        assert len(historial) == 1
        assert historial[0]["mensaje"] == "Mi primer commit"
        assert historial[0]["id"] == "commit_001"

def test_multiples_commits_incrementan_id(entorno_commit, capsys):
    archivo_prueba = entorno_commit
    
    with open(ARCHIVO_RASTREADO, "w") as f:
        json.dump([archivo_prueba], f)
        
    # Hacemos el primer commit
    crear_commit("Primer commit")
    
    # Hacemos el segundo commit
    crear_commit("Segundo commit")
    
    captura = capsys.readouterr()
    assert "Commit commit_002 creado correctamente" in captura.out
    
    # Verificamos que el historial tenga ambos registros
    with open(HISTORIAL, "r") as h:
        historial = json.load(h)
        assert len(historial) == 2
        assert historial[1]["id"] == "commit_002"