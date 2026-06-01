import os
import json
import shutil
import pytest
from pathlib import Path

# Importamos la función de su código
from src.diff import mostrar_diff, COMMITS_DIR, BASELINES

@pytest.fixture
def entorno_diff():
    """PREPARAR el entorno falso para probar el motor de diferencias"""
    test_dir = Path(".gitfc")
    
    #Respaldamos el .gitfc original si existe
    gitfc_existe = test_dir.exists()
    if gitfc_existe:
        os.rename(test_dir, ".gitfc_backup")
        
    #Creamos la estructura base
    test_dir.mkdir()
    COMMITS_DIR.mkdir()
    
    # --- CREAMOS EL COMMIT 1 ---
    c1 = COMMITS_DIR / "commit_001"
    c1.mkdir()
    (c1 / "archivos").mkdir()
    
    # Archivos del commit 1
    with open(c1 / "archivos" / "igual.txt", "w") as f: f.write("Linea 1\nLinea 2\n")
    with open(c1 / "archivos" / "modificado.txt", "w") as f: f.write("A\nB\nC\n")
    with open(c1 / "archivos" / "eliminado.txt", "w") as f: f.write("Adios\n")
    
    # Metadata del commit 1
    with open(c1 / "metadata.json", "w") as f:
        json.dump({"archivos": ["igual.txt", "modificado.txt", "eliminado.txt"]}, f)

    # --- CREAMOS EL COMMIT 2 ---
    c2 = COMMITS_DIR / "commit_002"
    c2.mkdir()
    (c2 / "archivos").mkdir()
    
    # Archivos del commit 2 (B se cambia por X, se añade D)
    with open(c2 / "archivos" / "igual.txt", "w") as f: f.write("Linea 1\nLinea 2\n")
    with open(c2 / "archivos" / "modificado.txt", "w") as f: f.write("A\nX\nC\nD\n")
    with open(c2 / "archivos" / "nuevo.txt", "w") as f: f.write("Hola\n")
    
    # Metadata del commit 2
    with open(c2 / "metadata.json", "w") as f:
        json.dump({"archivos": ["igual.txt", "modificado.txt", "nuevo.txt"]}, f)

    # --- CREAMOS UN BASELINE apuntando al commit 1 ---
    with open(BASELINES, "w") as f:
        json.dump({"v1.0": "commit_001"}, f)
        
    yield
    
    """LIMPIAR todo al terminar cada prueba"""
    if test_dir.exists():
        shutil.rmtree(test_dir)
        
    # Restauramos el original
    if gitfc_existe:
        os.rename(".gitfc_backup", test_dir)


# --- INICIAN LAS PRUEBAS ---

def test_diff_sin_repositorio(entorno_diff, capsys):
    shutil.rmtree(COMMITS_DIR)
    
    mostrar_diff("commit_001", "commit_002")
    
    captura = capsys.readouterr()
    assert "No existe un repositorio inicializado" in captura.out

def test_diff_referencia_no_encontrada(entorno_diff, capsys):
    # Falla la primera referencia
    mostrar_diff("fantasma", "commit_002")
    captura = capsys.readouterr()
    assert "No se encontró la versión: fantasma" in captura.out
    
    # Falla la segunda referencia
    mostrar_diff("commit_001", "fantasma")
    captura = capsys.readouterr()
    assert "No se encontró la versión: fantasma" in captura.out

def test_diff_commits_vacios(entorno_diff, capsys):
    # Creamos dos commits sin archivos
    for i in [3, 4]:
        c = COMMITS_DIR / f"commit_00{i}"
        c.mkdir()
        (c / "archivos").mkdir()
        with open(c / "metadata.json", "w") as f:
            json.dump({"archivos": []}, f)
            
    mostrar_diff("commit_003", "commit_004")
    
    captura = capsys.readouterr()
    assert "Ninguna versión contiene archivos." in captura.out

def test_diff_completo(entorno_diff, capsys):
    # Evalúa que difflib funcione usando una mezcla 
    # de un ID directo y un nombre de baseline ("v1.0" = "commit_001")
    mostrar_diff("v1.0", "commit_002")
    
    captura = capsys.readouterr()
    salida = captura.out
    
    # Verificamos archivo intacto
    assert "--- Archivo: igual.txt ---" in salida
    assert "Sin cambios en este archivo." in salida
    
    # Verificamos archivo eliminado
    assert "--- Archivo: eliminado.txt ---" in salida
    assert "Solo existe en v1.0 — eliminado en commit_002" in salida
    
    # Verificamos archivo nuevo
    assert "--- Archivo: nuevo.txt ---" in salida
    assert "Solo existe en commit_002 — nuevo en commit_002" in salida
    
    # Verificamos archivo modificado (líneas cambiadas y añadidas)
    assert "--- Archivo: modificado.txt ---" in salida
    assert "Líneas eliminadas:" in salida
    assert "[2]   B" in salida  # La B se eliminó
    assert "Líneas añadidas:" in salida
    assert "[2]   X" in salida  # La X tomó su lugar
    assert "[4]   D" in salida  # La D se insertó al final