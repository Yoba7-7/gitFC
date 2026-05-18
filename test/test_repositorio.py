import os
import shutil

from src.repositorio import *
from src.status import *

def setup_function():
	'''
	Limpia repositorios previos para iniciar las pruebas
	en limpio (se ejecuta antes de las pruebas)
	'''
	if os.path.exists(".gitfc"):
		shutil.rmtree(".gitfc")

def teardown_function():
	'''
	Limpia repositorios creados con las pruebas
	(se ejecuta después de las pruebas)
	'''
	if os.path.exists(".gitfc"):
		shutil.rmtree(".gitfc")

def test_crea_directorio_repo():
	'''
	función para probar si se creo el directorio .gitfc
	al ejecutar el comando init
	'''
	iniciar_repositorio()
	assert os.path.exists(".gitfc")

def test_crea_directorio_commits():
	'''
	funcion para probar si se creo el directorio de commits
	'''
	iniciar_repositorio()
	assert os.path.exists(".gitfc/commits")

def test_crea_directorio_staging():
	'''
	funcion para probar si se creo el directorio del area de staging
	(archivos para ser cargados)
	'''
	iniciar_repositorio()
	assert os.path.exists(".gitfc/staging")

def test_metadata_creado():
	'''
	funcion para probar si se crea el archivo que da seguimiento
	a los metadatos del repositorio
	'''
	iniciar_repositorio()
	assert os.path.exists(".gitfc/metadata.json")

def test_archivos_rastreados():
	'''
	funcion para verificar que se crea el archivo de seguimiento
	de archivos
	'''
	iniciar_repositorio()
	assert os.path.exists(".gitfc/archivos_rastreados.json")
