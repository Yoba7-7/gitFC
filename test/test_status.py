import os
import shutil

from src.repositorio import *
from src.status import *

def setup_function():
	'''
	funcion para limpiar los directorios .gitfc creados en
	pruebas anteriores (antes de ejecucion de test)
	'''
	if os.path.exists(".gitfc"):
		shutil.rmtree(".gitfc")

def teardown_function():
	'''
	funcion para limpiar los directorios .gitfc creados despues
	de ejecutar una prueba (después de la ejecución del test)
	'''
	if os.path.exists(".gitfc"):
		shutil.rmtree(".gitfc")

def test_repo_existe_despues_init():
	'''
	debe detectar el repositorio después del init
	'''
	iniciar_repositorio()
	assert existe_repo() is True

def test_repositorio_no_existe():
	'''
	verificar que no exista un repositorio incialmente
	'''
	assert existe_repo() is False

def test_status_cuando_existe_repo():
	'''
	Debe mostrar mensaje de correcto cuando existe el repositorio
	'''
	iniciar_repositorio()
	resultado =  verificar_repo()
	assert resultado == "Repositorio activo"

def test_status_cuando_no_existe_repo():
	'''
	Debe mostrar mensaje correcto cuando NO existe repositorio
	'''
	resultado = verificar_repo()
	assert resultado == "No existe un repositorio"


# Aca van los demás test que prueban el resto de funciones de  status.py
