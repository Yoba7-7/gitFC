import argparse

from repositorio import *
from status import *

parser = argparse.ArgumentParser()
parser.add_argument("command")
arg = parser.parse_args()

if arg.command == "init":
	iniciar_repositorio()

elif arg.command == "status":
	mostrar_status()

else:
	print("Comando no valido")
