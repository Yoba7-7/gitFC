import argparse

from repositorio import *

parser = argparse.ArgumentParser()
parser.add_argument("command")
arg = parser.parse_args()

if arg.command == "init":
	init_repository()

elif arg.command == "status":
	show_status()

else:
	print("Comando no valido")
