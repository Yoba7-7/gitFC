=============================================
Ejecución de prueba 
=============================================

REQUISITOS PREVIOS
  - Python 3.8 o superior instalado
  - Tener el proyecto clonado localmente

PASOS PARA EJECUTAR

  1. Abrir terminal en la carpeta raíz del proyecto

  2. Crear entorno virtual:
        python3 -m venv .venv

  3. Activar entorno virtual:
        Linux/macOS:  source .venv/bin/activate
        Windows:      .venv\Scripts\activate

  4. Instalar dependencias:
        pip install -r requirements.txt

  5. Correr las pruebas:
        pytest tests/ -v

  6. Verificar que todas dicen PASSED en la salida

INTERPRETACIÓN DE RESULTADOS
  PASSED → el caso de prueba pasó correctamente
  FAILED → encontró un error, revisar el mensaje debajo
  ERROR  → el test no pudo ejecutarse, problema en el código del test

  **Nota: Si vamos a probarlo igual de manera manual (hacer commits, ver versiones, etc) poner los comandos necesarios 