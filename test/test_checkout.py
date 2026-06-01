import os
import json
import shutil
import pytest
from pathlib import Path

# Importamos la función de su código
from src.checkout import hacer_checkout, COMMITS_DIR, BASELINES

@pytest.fixture
def entorno_checkout():
    """PREPARAR el entorno falso para las pruebas de checkout"""
    test_dir = Path(".gitfc")
    nombre_archivo = "archivo_restaurado.txt"
    
    # Respaldamos el .gitfc original si existe
    gitfc_existe = test_dir.exists()
    if gitfc_existe:
        os.rename(test_dir, ".gitfc_backup")
        
    # Creamos la estructura base
    test_dir.mkdir()
    COMMITS_DIR.mkdir()
    
    # Creamos un commit VÁLIDO simulado (commit_001)
    commit_valido = COMMITS_DIR / "commit_001"
    commit_valido.mkdir()
    archivos_path = commit_valido / "archivos"
    archivos_path.mkdir()
    
    # Metemos un archivo adentro de ese commit
    with open(archivos_path / nombre_archivo, "w") as f:
        f.write("Contenido del pasado")
        
    # Le creamos su metadata
    with open(commit_valido / "metadata.json", "w") as f:
        json.dump({"mensaje": "Commit de prueba", "fecha": "2023-11-01"}, f)
        
    # Creamos un baseline simulado apuntando a ese commit
    with open(BASELINES, "w") as f:
        json.dump({"v1.0": "commit_001"}, f)
        
    yield nombre_archivo
    
    """LIMPIAR todo al terminar cada prueba"""
    if test_dir.exists():
        shutil.rmtree(test_dir)
        
    # Borramos el archivo que el checkout copió a nuestra carpeta principal
    if Path(nombre_archivo).exists():
        os.remove(nombre_archivo)
        
    # Restauramos el original
    if gitfc_existe:
        os.rename(".gitfc_backup", test_dir)


# --- INICIAN LAS PRUEBAS ---

def test_checkout_sin_repositorio(entorno_checkout, capsys):
    shutil.rmtree(COMMITS_DIR) # Borramos la carpeta
    
    hacer_checkout("commit_001")
    
    captura = capsys.readouterr()
    assert "No existe un repositorio inicializado" in captura.out

def test_checkout_referencia_no_encontrada(entorno_checkout, capsys):
    # Intentamos buscar un commit que no existe
    hacer_checkout("fantasma_004")
    
    captura = capsys.readouterr()
    assert "No se encontró la versión: fantasma_004" in captura.out

def test_checkout_commit_sin_carpeta_archivos(entorno_checkout, capsys):
    # Creamos un commit roto a propósito (sin carpeta 'archivos')
    (COMMITS_DIR / "commit_roto").mkdir()
    
    hacer_checkout("commit_roto")
    
    captura = capsys.readouterr()
    assert "El commit commit_roto no tiene archivos guardados" in captura.out

def test_checkout_commit_vacio(entorno_checkout, capsys):
    # Creamos un commit que sí tiene carpeta, pero no tiene archivos adentro
    c_vacio = COMMITS_DIR / "commit_vacio"
    c_vacio.mkdir()
    (c_vacio / "archivos").mkdir()
    # Le ponemos metadata para que no falle antes de tiempo
    with open(c_vacio / "metadata.json", "w") as f:
        json.dump({"mensaje": "Vacio", "fecha": "2023"}, f)
        
    hacer_checkout("commit_vacio")
    
    captura = capsys.readouterr()
    assert "El commit commit_vacio no contiene archivos" in captura.out

def test_checkout_exitoso_por_id(entorno_checkout, capsys):
    nombre_archivo = entorno_checkout
    
    # Hacemos checkout usando directamente el ID del commit
    hacer_checkout("commit_001")
    
    captura = capsys.readouterr()
    assert "Regresando a commit_001" in captura.out
    assert "Checkout completado" in captura.out
    
    # Comprobamos que el archivo haya aparecido en nuestra carpeta actual
    assert Path(nombre_archivo).exists()

def test_checkout_exitoso_por_baseline(entorno_checkout, capsys):
    nombre_archivo = entorno_checkout
    
    # Hacemos checkout usando el nombre de la línea base
    hacer_checkout("v1.0")
    
    captura = capsys.readouterr()
    assert "Regresando a v1.0 (commit_001)" in captura.out
    
    # Comprobamos que el archivo se restauró correctamente
    assert Path(nombre_archivo).exists()