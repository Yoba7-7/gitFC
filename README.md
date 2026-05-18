Instrucciones:

- Crear  un entorno de usuario .venv mediante el siguiente comando
	python3 -m venv .venv
- Activar el entorno de usuario con el comando
	source .venv/bin/activate
- Instalar las bibliotecas necesarias para el funcionamiento del programa
	pip install requirements

- Para poder iniciar un repositorio ingresa el comando (python3 main.py init)
- Para poder revisar el estado del repositorio ingresa el comando (python3 main.py status)
- Para ejecutar los test dirigete a la carpeta raíz (gitfc) y ejecuta los comandos:
	* python3 -m pytest test/test_repositorio.py
	* python3 -m pytest test/test_status.py
