import argparse

from repositorio import *
from status import *
from staging import *
from commit import *
from historial import *
from baseline import *
from diff import *
from checkout import *

parser = argparse.ArgumentParser()

parser.add_argument("command")
parser.add_argument("arg1", nargs="?")
parser.add_argument("arg2", nargs="?")

args = parser.parse_args()

if args.command == "init":
	iniciar_repositorio()

elif args.command == "status":
	mostrar_status()

elif args.command == "add":
	add_file(args.arg1)

elif args.command == "commit":
	crear_commit(args.arg1)

elif args.command == "historial":
	mostrar_historial()

elif args.command == "baseline":
	crear_baseline(args.arg1)

elif args.command == "listar_baselines":
	listar_baselines()

elif args.command == "diff":
    mostrar_diff(args.arg1, args.arg2)

elif args.command == "checkout":
    hacer_checkout(args.arg1)
	
else:
	print("Comando no valido")
