import os
import json
import shutil
import pytest
from pathlib import Path

# Importamos las funciones y la constante de tu archivo
from src.historial import cargar_historial, mostrar_historial, obtener_ultimo_commit, HISTORIAL

@pytest.fixture
def entorno_historial():
    """PREPARAR el entorno falso para las pruebas de historial"""
    test_dir = Path(".gitfc")
    
    # Respaldamos el .gitfc original si existe
    gitfc_existe = test_dir.exists()
    if gitfc_existe:
        os.rename(test_dir, ".gitfc_backup")
        
    # Creamos la carpeta base simulada
    test_dir.mkdir(exist_ok=True)
    
    yield test_dir
    
    """LIMPIAR todo al terminar cada prueba"""
    if test_dir.exists():
        shutil.rmtree(test_dir)
        
    # Restauramos el original
    if gitfc_existe:
        os.rename(".gitfc_backup", test_dir)


# --- INICIAN LAS PRUEBAS ---

def test_historial_vacio(entorno_historial, capsys):
    # En este punto NO hemos creado historial.json
    
    # Probar cargar_historial()
    assert cargar_historial() == []
    
    # Probar obtener_ultimo_commit()
    assert obtener_ultimo_commit() is None
    
    # Probar mostrar_historial()
    mostrar_historial()
    captura = capsys.readouterr()
    assert "No hay commits registrados" in captura.out

def test_historial_con_datos(entorno_historial, capsys):
    # PREPARAR: Creamos datos falsos simulando 2 commits
    datos_falsos = [
        {
            "id": "commit_001",
            "mensaje": "Primer commit de prueba",
            "fecha": "2023-11-01 10:00:00",
            "archivos": ["main.py"]
        },
        {
            "id": "commit_002",
            "mensaje": "Segundo commit de prueba",
            "fecha": "2023-11-01 11:00:00",
            "archivos": ["main.py", "utils.py"]
        }
    ]
    
    # Escribimos los datos falsos en el JSON
    with open(HISTORIAL, "w") as f:
        json.dump(datos_falsos, f)
        
    # Probar cargar_historial()
    historial_cargado = cargar_historial()
    assert len(historial_cargado) == 2
    assert historial_cargado[0]["id"] == "commit_001"
    
    # Probar obtener_ultimo_commit()
    ultimo = obtener_ultimo_commit()
    assert ultimo["id"] == "commit_002"
    assert ultimo["mensaje"] == "Segundo commit de prueba"
    
    # Probar mostrar_historial()
    mostrar_historial()
    captura = capsys.readouterr()
    
    # Verificamos que se imprimió el formato y los datos correctos
    assert "==== HISTORIAL DE COMMITS ====" in captura.out
    assert "ID:  commit_001" in captura.out
    assert "Mensaje: Primer commit de prueba" in captura.out
    assert "ID:  commit_002" in captura.out
    assert " - utils.py" in captura.out