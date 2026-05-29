Instrucciones:

- Crear  un entorno de usuario .venv mediante el siguiente comando
	python3 -m venv .venv
- Activar el entorno de usuario con el comando
	source .venv/bin/activate
- Instalar las bibliotecas necesarias para el funcionamiento del programa
	pip install requirements

- Para poder iniciar un repositorio ingresa el comando (python3 main.py init)
- Para poder revisar el estado del repositorio ingresa el comando (python3 main.py status)
- Para poder agregar un archivo al area de staging ingresa el comando (python3 main.py add <archivo>)
- Para poder hacer commit ingresa el comando (python3 main.py commit "<mensaje>")
- Para poder ver el historial de commits ingresa el comando (python3 main.py historial)
- Para poder crear una linea base ingresa el comando (python3 main.py baseline <version>)
- Para poder revisar las lineas base creadas ingresa el comando (python3 main listar_baselines)
- Para ejecutar los test dirigete a la carpeta raíz (gitfc) y ejecuta los comandos:
	* python3 -m pytest test/test_repositorio.py
	* python3 -m pytest test/test_status.py
