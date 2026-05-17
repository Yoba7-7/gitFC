'''
Para que no se haga tan larag la clase sólo será el parser de los comandos 
LLama a la función correspondiente de cada módulo

Borrar o mejorar este comentario ya en entrega final 
'''

import argparse

from repositorio import *

parser = argparse.ArgumentParser(description="SBAC - Sistema Básico de Administración de Configuración")
parser.add_argument("command", help="Comando a ejecutar")
parser.add_argument("args", nargs="*", help="Argumentos del comando")
args = parser.parse_args()

if args.command == "init":
    init_repository()

elif args.command == "status":
    show_status()

elif args.command == "add":
    if not args.args:
        print("Uso: python main.py add <archivo>")
    else:
        add_file(args.args[0])

else:
    print(f"Comando no válido: {args.command}")