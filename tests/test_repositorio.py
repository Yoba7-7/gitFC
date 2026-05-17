import os
import shutil
import pytest
from src.repositorio import init_repository, add_file, show_status

@pytest.fixture(autouse=True)
def limpiar_repo():
    # limpia cualquier .gitfc que haya quedado de una prueba anterior.
    if os.path.exists(".gitfc"):
        shutil.rmtree(".gitfc")
    yield
    #  limpia lo que ese test haya creado.
    if os.path.exists(".gitfc"):
        shutil.rmtree(".gitfc")


# --- init ---

def test_init_crea_carpeta():
    init_repository()
    assert os.path.exists(".gitfc")

def test_init_crea_carpeta_commits():
    init_repository()
    assert os.path.exists(".gitfc/commits")

def test_init_crea_carpeta_baselines():
    init_repository()
    assert os.path.exists(".gitfc/baselines")

def test_init_crea_tracked_files():
    init_repository()
    assert os.path.exists(".gitfc/tracked_files.json")

def test_init_crea_metadata():
    init_repository()
    assert os.path.exists(".gitfc/metadata.json")

def test_init_dos_veces_no_falla(capsys):
    init_repository()
    init_repository()
    salida = capsys.readouterr().out
    assert "Ya existe" in salida


# --- add ---

def test_add_archivo_existente(tmp_path):
    init_repository()
    archivo = tmp_path / "prueba.py"
    archivo.write_text("print('hola')")
    add_file(str(archivo))
    import json
    with open(".gitfc/tracked_files.json") as f:
        tracked = json.load(f)
    assert str(archivo) in tracked

def test_add_archivo_no_existente(capsys):
    init_repository()
    add_file("no_existe.py")
    salida = capsys.readouterr().out
    assert "no encontrado" in salida

def test_add_duplicado_no_repite(tmp_path, capsys):
    init_repository()
    archivo = tmp_path / "prueba.py"
    archivo.write_text("x = 1")
    add_file(str(archivo))
    add_file(str(archivo))
    salida = capsys.readouterr().out
    assert "ya está en seguimiento" in salida

def test_add_sin_repo(capsys):
    add_file("cualquier.py")
    salida = capsys.readouterr().out
    assert "No hay repositorio" in salida


# --- status ---

def test_status_sin_repo(capsys):
    show_status()
    salida = capsys.readouterr().out
    assert "No existe" in salida

def test_status_repo_vacio(capsys):
    init_repository()
    show_status()
    salida = capsys.readouterr().out
    assert "Archivos rastreados: 0" in salida
