import os
import json
import shutil
import pytest
from pathlib import Path

# Importamos las funciones y rutas del archivo
from src.baseline import crear_baseline, listar_baselines, BASELINE, HISTORIAL

@pytest.fixture
def entorno_baseline():
    """PREPARAR el entorno simulado para las baselines"""
    test_dir = Path(".gitfc")
    
    # Respaldamos el .gitfc original si existe
    gitfc_existe = test_dir.exists()
    if gitfc_existe:
        os.rename(test_dir, ".gitfc_backup")
        
    # Creamos la carpeta base
    test_dir.mkdir(exist_ok=True)
    
    yield test_dir
    
    """LIMPIAR todo al terminar cada prueba"""
    if test_dir.exists():
        shutil.rmtree(test_dir)
        
    # Restauramos el original
    if gitfc_existe:
        os.rename(".gitfc_backup", test_dir)


# --- INICIAN LAS PRUEBAS ---

def test_crear_baseline_sin_historial(entorno_baseline, capsys):
    # Sin crear historial.json intentamos hacer un baseline
    crear_baseline("v1.0")
    
    captura = capsys.readouterr()
    assert "No existen commits" in captura.out

def test_crear_baseline_historial_vacio(entorno_baseline, capsys):
    # Creamos un historial.json vacío
    with open(HISTORIAL, "w") as f:
        json.dump([], f)
        
    crear_baseline("v1.0")
    
    captura = capsys.readouterr()
    assert "No existen commits" in captura.out

def test_crear_baseline_primera_vez(entorno_baseline, capsys):
    # Simulamos que tenemos un commit en el historial
    with open(HISTORIAL, "w") as f:
        json.dump([{"id": "commit_001", "mensaje": "Mi primer commit"}], f)
        
    # Ejecutamos
    crear_baseline("v1.0")
    
    captura = capsys.readouterr()
    assert "Baseline 'v1.0' creado en commit_001" in captura.out
    
    # Verificamos que se haya creado el archivo baselines.json
    assert BASELINE.exists()
    with open(BASELINE, "r") as b:
        datos = json.load(b)
        assert "v1.0" in datos
        assert datos["v1.0"] == "commit_001"

def test_crear_baseline_agregando_a_existente(entorno_baseline, capsys):
    # Simulamos un historial con 2 commits
    with open(HISTORIAL, "w") as f:
        json.dump([
            {"id": "commit_001"},
            {"id": "commit_002"}
        ], f)
        
    # Simulamos que YA existe un baseline anterior
    with open(BASELINE, "w") as f:
        json.dump({"v1.0": "commit_001"}, f)
        
    # Ejecutamos crear la nueva
    crear_baseline("v2.0")
    
    # Comprobamos que el archivo ahora tenga AMBAS baselines
    with open(BASELINE, "r") as b:
        datos = json.load(b)
        assert len(datos) == 2
        assert datos["v1.0"] == "commit_001"
        assert datos["v2.0"] == "commit_002"

def test_listar_baselines_sin_datos(entorno_baseline, capsys):
    listar_baselines()
    
    captura = capsys.readouterr()
    assert "No existen baselines" in captura.out

def test_listar_baselines_con_datos(entorno_baseline, capsys):
    # Creamos baselines de prueba
    with open(BASELINE, "w") as f:
        json.dump({
            "v1.0": "commit_001",
            "v2.0": "commit_002"
        }, f)
        
    listar_baselines()
    
    captura = capsys.readouterr()
    assert "Baselines registradas:" in captura.out
    assert "v1.0 -> commit_001" in captura.out
    assert "v2.0 -> commit_002" in captura.out