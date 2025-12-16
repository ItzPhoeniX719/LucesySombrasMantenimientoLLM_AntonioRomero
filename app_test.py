import unittest
import subprocess
import sys
import os

class TestAppPy(unittest.TestCase):
    def run_app(self, inputs):
        """
        Ejecuta app.py con una secuencia de entradas simuladas y captura la salida.
        """
        # Prepara el comando para ejecutar app.py
        cmd = [sys.executable, 'RefactoringAntonioRomero.py']
        # Une las entradas con saltos de línea y agrega un salto final
        input_str = '\n'.join(inputs) + '\n'
        # Ejecuta el proceso
        result = subprocess.run(
            cmd,
            input=input_str.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(os.path.abspath(__file__)),
            timeout=5
        )
        return result.stdout.decode(), result.stderr.decode()

    def test_agregar_empleado_ventas(self):
        salida, error = self.run_app(['1', 'Juan', '1000', '5'])
        self.assertIn('Guardado Ventas.', salida)
        self.assertIn('Salir', salida)
        self.assertEqual(error, '')

    def test_agregar_empleado_it(self):
        salida, error = self.run_app(['2', 'Ana', '1200', '5'])
        self.assertIn('Guardado IT.', salida)
        self.assertIn('Salir', salida)
        self.assertEqual(error, '')

    def test_agregar_empleado_rrhh(self):
        salida, error = self.run_app(['3', 'Luis', '1500', '5'])
        self.assertIn('Guardado RRHH.', salida)
        self.assertIn('Salir', salida)
        self.assertEqual(error, '')

    def test_reporte_vacio(self):
        salida, error = self.run_app(['4', '5'])
        self.assertIn('No hay nadie', salida)
        self.assertEqual(error, '')

    def test_flujo_completo(self):
        # Agrega 3 empleados y muestra el reporte
        entradas = [
            '1', 'Juan', '1000',
            '2', 'Ana', '1200',
            '3', 'Luis', '1500',
            '4', '5'
        ]
        salida, error = self.run_app(entradas)
        self.assertIn('Emp: Juan', salida)
        self.assertIn('Emp: Ana', salida)
        self.assertIn('Emp: Luis', salida)
        self.assertIn('Pago Final:', salida)
        self.assertEqual(error, '')

    def test_opcion_invalida(self):
        salida, error = self.run_app(['9', '5'])
        self.assertIn('Error', salida)
        self.assertEqual(error, '')

if __name__ == "__main__":
    unittest.main()
