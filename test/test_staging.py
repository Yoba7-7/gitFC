import unittest
import json
import os
import shutil
import io
from unittest.mock import patch

# Importamos la función de su archivo. 
from src.staging import add_file, ARCHIVO_RASTREADO

class TestStaging(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = ".gitfc"
        self.archivo_rastreado = ARCHIVO_RASTREADO
        
        # Respaldamos el .gitfc original si existe
        self.gitfc_existe = os.path.exists(self.test_dir)
        if self.gitfc_existe:
            os.rename(self.test_dir, ".gitfc_backup")
            
        #  Creamos un repositorio simulado vacío
        os.makedirs(self.test_dir)
        
        #  Creamos el archivo JSON inicial con una lista vacía
        with open(self.archivo_rastreado, "w") as f:
            json.dump([], f)
            
        # Creamos un archivo de texto real para usar en las pruebas
        self.archivo_prueba = "archivo_prueba_test.txt"
        with open(self.archivo_prueba, "w") as f:
            f.write("Contenido de prueba para staging")

    def tearDown(self):
        
        # Borramos el entorno simulado
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
            
        # Borramos el archivo de prueba
        if os.path.exists(self.archivo_prueba):
            os.remove(self.archivo_prueba)
            
        # Restauramos el .gitfc original si lo respaldamos
        if self.gitfc_existe:
            os.rename(".gitfc_backup", self.test_dir)

    # ---CASOS DE PRUEBA ---

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_repositorio_no_inicializado(self, mock_stdout):
        #Borramos la carpeta simulada para que la función crea que no hay repo
        shutil.rmtree(self.test_dir)
        add_file(self.archivo_prueba)
        
        # Revisamos qué imprimió la consola
        self.assertIn("Repositorio no inicializado", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_archivo_no_existe(self, mock_stdout):
        #Intentamos agregar un archivo inventado
        add_file("archivo_fantasma.txt")
        
        # COMPROBAR
        self.assertIn("El archivo no existe", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_agregar_archivo_exitoso(self, mock_stdout):
        #Agregamos el archivo real de prueba
        add_file(self.archivo_prueba)
        
        #Revisamos el mensaje de éxito
        self.assertIn(f"{self.archivo_prueba} agregado correctamente", mock_stdout.getvalue())
        
        # Leemos el JSON y verificamos que el archivo esté adentro
        with open(self.archivo_rastreado, "r") as f:
            rastreo = json.load(f)
        self.assertIn(self.archivo_prueba, rastreo)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_archivo_ya_rastreado(self, mock_stdout):
        #Metemos el archivo al JSON manualmente para simular que ya estaba rastreado
        with open(self.archivo_rastreado, "w") as f:
            json.dump([self.archivo_prueba], f)
            
        # Intentamos agregarlo de nuevo usando la función
        add_file(self.archivo_prueba)
        
        # COMPROBAR
        self.assertIn("EL archivo ya esta siendo rastreado", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()