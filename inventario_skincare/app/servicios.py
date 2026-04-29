from typing import List

from app.categorias import CategoriaRepositorioJSON
from app.modelos import Producto
from app.repositorio import InventarioRepositorioJSON
from app.validaciones import (
    normalizar_texto,
    validar_categoria,
    validar_entero_no_negativo,
    validar_entero_positivo,
    validar_nombre_producto,
    validar_precio,
)


class InventarioServicio:
    def __init__(
        self,
        repositorio: InventarioRepositorioJSON | None = None,
        categoria_repositorio: CategoriaRepositorioJSON | None = None,
    ):
        self.repositorio = repositorio or InventarioRepositorioJSON()
        self.categoria_repositorio = categoria_repositorio or CategoriaRepositorioJSON()

    def registrar_producto(self, nombre, precio, stock, categoria="General", stock_minimo=5) -> Producto:
        nombre = validar_nombre_producto(nombre)
        precio = validar_precio(precio)
        stock = validar_entero_no_negativo(stock, "stock")
        categoria = validar_categoria(categoria)
        stock_minimo = validar_entero_no_negativo(stock_minimo, "stock mínimo")

        productos = self.repositorio.leer_productos()
        nombre_normalizado = normalizar_texto(nombre)

        if any(normalizar_texto(p.nombre) == nombre_normalizado for p in productos):
            raise ValueError("Ya existe un producto registrado con ese nombre.")

        producto = Producto(
            codigo=self.repositorio.generar_codigo(),
            nombre=nombre,
            precio=precio,
            stock=stock,
            categoria=categoria,
            stock_minimo=stock_minimo,
        )

        productos.append(producto)
        self.repositorio.guardar_productos(productos)
        self.categoria_repositorio.agregar_categoria(categoria)
        return producto

    def listar_productos(self, filtro="") -> List[Producto]:
        productos = self.repositorio.leer_productos()
        filtro = normalizar_texto(filtro)

        if filtro:
            productos = [
                p for p in productos
                if filtro in normalizar_texto(p.nombre)
                or filtro in normalizar_texto(p.categoria)
                or filtro == normalizar_texto(p.codigo)
            ]

        return sorted(productos, key=lambda p: (normalizar_texto(p.nombre), p.codigo))

    def buscar_producto(self, termino) -> List[Producto]:
        termino = str(termino or "").strip()

        if not termino:
            raise ValueError("Ingrese un nombre, código o categoría para buscar.")

        resultados = self.listar_productos(termino)

        if not resultados:
            raise ValueError("No se encontró ningún producto con ese dato.")

        return resultados

    def actualizar_stock(self, codigo_o_nombre, nuevo_stock) -> Producto:
        nuevo_stock = validar_entero_no_negativo(nuevo_stock, "nuevo stock")
        productos = self.repositorio.leer_productos()
        indice = self._buscar_indice_exacto(productos, codigo_o_nombre)
        productos[indice].stock = nuevo_stock
        self.repositorio.guardar_productos(productos)
        return productos[indice]

    def actualizar_producto(self, codigo_o_nombre, nombre, precio, stock, categoria="General", stock_minimo=5) -> Producto:
        nombre = validar_nombre_producto(nombre)
        precio = validar_precio(precio)
        stock = validar_entero_no_negativo(stock, "stock")
        categoria = validar_categoria(categoria)
        stock_minimo = validar_entero_no_negativo(stock_minimo, "stock mínimo")

        productos = self.repositorio.leer_productos()
        indice = self._buscar_indice_exacto(productos, codigo_o_nombre)
        nombre_normalizado = normalizar_texto(nombre)

        for posicion, producto in enumerate(productos):
            if posicion != indice and normalizar_texto(producto.nombre) == nombre_normalizado:
                raise ValueError("Ya existe otro producto registrado con ese nombre.")

        productos[indice].nombre = nombre
        productos[indice].precio = precio
        productos[indice].stock = stock
        productos[indice].categoria = categoria
        productos[indice].stock_minimo = stock_minimo

        self.repositorio.guardar_productos(productos)
        self.categoria_repositorio.agregar_categoria(categoria)
        return productos[indice]

    def eliminar_producto(self, codigo_o_nombre, forzar=False) -> Producto:
        productos = self.repositorio.leer_productos()
        indice = self._buscar_indice_exacto(productos, codigo_o_nombre)
        producto = productos[indice]

        if producto.stock > 0 and not forzar:
            raise ValueError("El producto tiene stock. Para eliminarlo, confirme la eliminación forzada.")

        eliminado = productos.pop(indice)
        self.repositorio.guardar_productos(productos)
        return eliminado

    def vender_producto(self, codigo_o_nombre, cantidad) -> Producto:
        cantidad = validar_entero_positivo(cantidad, "cantidad a vender")
        productos = self.repositorio.leer_productos()
        indice = self._buscar_indice_exacto(productos, codigo_o_nombre)
        producto = productos[indice]

        if cantidad > producto.stock:
            raise ValueError("No hay stock suficiente para realizar la venta.")

        producto.stock -= cantidad
        self.repositorio.guardar_productos(productos)
        return producto

    def reporte_stock_bajo(self, limite=None) -> List[Producto]:
        productos = self.repositorio.leer_productos()

        if limite is not None and str(limite).strip() != "":
            limite = validar_entero_no_negativo(limite, "límite de stock")
            return sorted([p for p in productos if p.stock <= limite], key=lambda p: (p.stock, p.nombre))

        return sorted([p for p in productos if p.stock <= p.stock_minimo], key=lambda p: (p.stock, p.nombre))

    def obtener_categorias(self) -> List[str]:
        categorias = self.categoria_repositorio.leer_categorias()
        productos = self.repositorio.leer_productos()

        for producto in productos:
            categoria = validar_categoria(producto.categoria)
            if normalizar_texto(categoria) not in [normalizar_texto(c) for c in categorias]:
                categorias.append(categoria)

        self.categoria_repositorio.guardar_categorias(categorias)
        return self.categoria_repositorio.leer_categorias()

    def agregar_categoria(self, categoria) -> str:
        return self.categoria_repositorio.agregar_categoria(categoria)

    def _buscar_indice_exacto(self, productos: List[Producto], codigo_o_nombre) -> int:
        dato = str(codigo_o_nombre or "").strip()

        if not dato:
            raise ValueError("Seleccione o escriba el nombre/código del producto.")

        dato_normalizado = normalizar_texto(dato)
        coincidencias = []

        for i, producto in enumerate(productos):
            if dato_normalizado == normalizar_texto(producto.codigo) or dato_normalizado == normalizar_texto(producto.nombre):
                coincidencias.append(i)

        if not coincidencias:
            raise ValueError("El producto no existe o no fue seleccionado correctamente.")

        if len(coincidencias) > 1:
            raise ValueError("Hay más de una coincidencia. Use el código exacto del producto.")

        return coincidencias[0]
