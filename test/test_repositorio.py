import os
import shutil

from src.repositorio import *

def inicio():
	'''
	Se ejecuta antes de cada test
	Limpia cualquier repo previo
	'''
	if os.path.exists(".gitfc"):
		shutil.rmtree(".gitfc")

# aca van pruebas de las demás funciones 

