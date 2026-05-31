# Pruebas de Software y Administración de la Configuración 

# Proyecto Final

## Integrantes:<br>
Martínez Hidalgo Paola Mildred - 319300217<br>
otro nombre <br>
otro nombre <br>

# Instrucciones:

## Pasos para crear entorno en Linux
- Crear  un entorno de usuario .venv mediante el siguiente comando
    ```bash
	python3 -m venv .venv
- Activar el entorno de usuario con el comando
    ```bash
	source .venv/bin/activate
- Instalar las bibliotecas necesarias para el funcionamiento del programa
    ```bash
	pip install requirements

## Pasos para crear entorno en Windows
- Crear  un entorno de usuario .venv mediante el siguiente comando
    ```bash
	python -m venv .venv 
- Activar el entorno de usuario con el comando
    ```bash
	.venv\Scripts\activate 
- Instalar las bibliotecas necesarias para el funcionamiento del programa
    ```bash
	pip install -r requirements.txt

## Comados 

Para que estos comandos funcionen de manera correcta nos tenemos que dirigir a la carpeta src, si estamos trabajando dentro de windows puede que nos genere un error si colocamos python3, en este caso sólo colocar python, por ejemplo: python main.py init

- Para poder iniciar un repositorio ingresa el comando 
  ```bash
  python3 main.py init
- Para poder revisar el estado del repositorio ingresa el comando 
  ```bash
  python3 main.py status
- Para poder agregar un archivo al area de staging ingresa el comando 
   ```bash
   python3 main.py add <archivo>
- Para poder hacer commit ingresa el comando 
  ```bash
  python3 main.py commit "<mensaje>"
- Para poder ver el historial de commits ingresa el comando 
  ```bash
  python3 main.py historial
- Para poder crear una linea base ingresa el comando 
  ```bash
  python3 main.py baseline <version>
- Para poder revisar las lineas base creadas ingresa el comando 
  ```bash
  python3 main.py listar_baselines
- Para ver cambios entre versiones ingresa el comando 
  ```bash
  python3 main.py diff commit_001 commit_002
  python3 main.py diff v1.0 v1.1
- Para regresar a una versión específica ingresa el comando 
  ```bash
  python3 main.py checkout commit_002
  python3 main.py checkout v1.0

deff y checkout aceptan tanto IDs de commit como nombres de baseline, es decir ambos comandos funcionan.

## Test 
- Para ejecutar los test dirigete a la carpeta raíz (gitfc) y ejecuta los comandos:
   ```bash
	* python3 -m pytest test/test_repositorio.py
	* python3 -m pytest test/test_status.py

