import tempfile
import unittest
from pathlib import Path

from app.categorias import CategoriaRepositorioJSON
from app.repositorio import InventarioRepositorioJSON
from app.servicios import InventarioServicio


class TestInventarioServicio(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        ruta_inventario = Path(self.temporal.name) / "inventario_test.json"
        ruta_categorias = Path(self.temporal.name) / "categorias_test.json"
        repo = InventarioRepositorioJSON(ruta_archivo=ruta_inventario, usar_datos_prueba=False)
        repo_categorias = CategoriaRepositorioJSON(ruta_archivo=ruta_categorias)
        self.servicio = InventarioServicio(repo, repo_categorias)

    def tearDown(self):
        self.temporal.cleanup()

    def test_registrar_producto_valido(self):
        producto = self.servicio.registrar_producto("crema facial", "25.50", "10", "hidratación", "3")
        self.assertEqual(producto.nombre, "Crema Facial")
        self.assertEqual(producto.precio, 25.50)
        self.assertEqual(producto.stock, 10)

    def test_no_registra_nombre_repetido(self):
        self.servicio.registrar_producto("serum niacinamida", "30", "5")
        with self.assertRaises(ValueError):
            self.servicio.registrar_producto("SERUM NIACINAMIDA", "32", "8")

    def test_no_registra_precio_negativo(self):
        with self.assertRaises(ValueError):
            self.servicio.registrar_producto("bloqueador", "-10", "5")

    def test_no_registra_stock_negativo(self):
        with self.assertRaises(ValueError):
            self.servicio.registrar_producto("bloqueador", "40", "-2")

    def test_buscar_producto_existente(self):
        self.servicio.registrar_producto("protector solar", "40", "7")
        resultados = self.servicio.buscar_producto("solar")
        self.assertEqual(len(resultados), 1)

    def test_actualizar_stock(self):
        producto = self.servicio.registrar_producto("tonico facial", "20", "4")
        actualizado = self.servicio.actualizar_stock(producto.codigo, "15")
        self.assertEqual(actualizado.stock, 15)

    def test_actualizar_producto_precio_y_categoria(self):
        producto = self.servicio.registrar_producto("limpiador gel", "20", "4")
        actualizado = self.servicio.actualizar_producto(
            producto.codigo,
            "limpiador gel suave",
            "22.90",
            "12",
            "Limpieza diaria",
            "4",
        )
        self.assertEqual(actualizado.nombre, "Limpiador Gel Suave")
        self.assertEqual(actualizado.precio, 22.90)
        self.assertEqual(actualizado.stock, 12)
        self.assertEqual(actualizado.categoria, "Limpieza Diaria")

    def test_agregar_categoria_nueva(self):
        categoria = self.servicio.agregar_categoria("Cuidado de ojos")
        categorias = self.servicio.obtener_categorias()
        self.assertEqual(categoria, "Cuidado De Ojos")
        self.assertIn("Cuidado De Ojos", categorias)

    def test_vender_producto_descuenta_stock(self):
        producto = self.servicio.registrar_producto("limpiador", "18", "10")
        actualizado = self.servicio.vender_producto(producto.codigo, "3")
        self.assertEqual(actualizado.stock, 7)

    def test_no_vende_si_no_hay_stock_suficiente(self):
        producto = self.servicio.registrar_producto("mascarilla", "15", "2")
        with self.assertRaises(ValueError):
            self.servicio.vender_producto(producto.codigo, "5")

    def test_stock_bajo(self):
        self.servicio.registrar_producto("gel", "10", "1", "limpieza", "3")
        productos = self.servicio.reporte_stock_bajo()
        self.assertEqual(len(productos), 1)

    def test_eliminar_producto_sin_stock(self):
        producto = self.servicio.registrar_producto("producto vacio", "10", "0")
        eliminado = self.servicio.eliminar_producto(producto.codigo)
        self.assertEqual(eliminado.codigo, producto.codigo)
        self.assertEqual(len(self.servicio.listar_productos()), 0)


if __name__ == "__main__":
    unittest.main()
