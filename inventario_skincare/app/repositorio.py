import json
import os
from pathlib import Path
from typing import List

from app.modelos import Producto


class InventarioRepositorioJSON:
    def __init__(self, ruta_archivo=None, usar_datos_prueba=True):
        base = Path(__file__).resolve().parents[1]
        self.ruta_archivo = Path(ruta_archivo) if ruta_archivo else base / "datos" / "inventario.json"
        self.usar_datos_prueba = usar_datos_prueba
        self.ruta_archivo.parent.mkdir(parents=True, exist_ok=True)
        self._asegurar_archivo()

    def _datos_prueba(self) -> List[Producto]:
        return [
            Producto("P0001", "Limpiador Facial Suave", 29.90, 15, "Limpieza", 5),
            Producto("P0002", "Serum Vitamina C", 49.90, 8, "Tratamiento", 3),
            Producto("P0003", "Protector Solar Spf 50", 39.90, 20, "Protección", 5),
            Producto("P0004", "Crema Hidratante", 35.50, 12, "Hidratación", 4),
            Producto("P0005", "Tónico Facial", 24.90, 6, "Limpieza", 3),
        ]

    def _asegurar_archivo(self):
        if not self.ruta_archivo.exists():
            datos = self._datos_prueba() if self.usar_datos_prueba else []
            self.guardar_productos(datos)
            return

        try:
            with self.ruta_archivo.open("r", encoding="utf-8") as archivo:
                json.load(archivo)
        except json.JSONDecodeError:
            respaldo = self.ruta_archivo.with_suffix(".json.corrupto")
            os.replace(self.ruta_archivo, respaldo)
            datos = self._datos_prueba() if self.usar_datos_prueba else []
            self.guardar_productos(datos)

    def leer_productos(self) -> List[Producto]:
        self._asegurar_archivo()
        try:
            with self.ruta_archivo.open("r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except (OSError, json.JSONDecodeError):
            return []

        productos = []
        if not isinstance(datos, list):
            return productos

        for item in datos:
            try:
                producto = Producto.from_dict(item)
                if producto.codigo and producto.nombre:
                    productos.append(producto)
            except (TypeError, ValueError):
                # Si alguien dañó una fila del JSON, se ignora esa fila y el programa sigue funcionando.
                continue
        return productos

    def guardar_productos(self, productos: List[Producto]) -> None:
        datos = [producto.to_dict() for producto in productos]
        temporal = self.ruta_archivo.with_suffix(".tmp")
        with temporal.open("w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
        os.replace(temporal, self.ruta_archivo)

    def generar_codigo(self) -> str:
        productos = self.leer_productos()
        mayor = 0
        for producto in productos:
            codigo = producto.codigo.upper().replace("P", "", 1)
            if codigo.isdigit():
                mayor = max(mayor, int(codigo))
        return f"P{mayor + 1:04d}"

    def reiniciar_con_datos_prueba(self) -> None:
        self.guardar_productos(self._datos_prueba())
