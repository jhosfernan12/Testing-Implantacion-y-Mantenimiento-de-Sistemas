import json
import os
from pathlib import Path
from typing import List

from app.validaciones import normalizar_texto, validar_categoria


class CategoriaRepositorioJSON:
    def __init__(self, ruta_archivo=None):
        base = Path(__file__).resolve().parents[1]
        self.ruta_archivo = Path(ruta_archivo) if ruta_archivo else base / "datos" / "categorias.json"
        self.ruta_archivo.parent.mkdir(parents=True, exist_ok=True)
        self._asegurar_archivo()

    def _categorias_iniciales(self) -> List[str]:
        return [
            "General",
            "Limpieza",
            "Hidratación",
            "Tratamiento",
            "Protección",
            "Mascarillas",
            "Tónicos",
        ]

    def _ordenar(self, categorias: List[str]) -> List[str]:
        unicas = {}
        for categoria in categorias:
            try:
                categoria_limpia = validar_categoria(categoria)
            except ValueError:
                continue
            clave = normalizar_texto(categoria_limpia)
            if clave:
                unicas[clave] = categoria_limpia

        ordenadas = sorted(unicas.values(), key=normalizar_texto)
        if "general" in unicas:
            ordenadas = [unicas["general"]] + [c for c in ordenadas if normalizar_texto(c) != "general"]
        return ordenadas or ["General"]

    def _asegurar_archivo(self):
        if not self.ruta_archivo.exists():
            self.guardar_categorias(self._categorias_iniciales())
            return

        try:
            with self.ruta_archivo.open("r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            if not isinstance(datos, list):
                raise ValueError("El archivo de categorias no tiene una lista.")
        except (OSError, json.JSONDecodeError, ValueError):
            respaldo = self.ruta_archivo.with_suffix(".json.corrupto")
            try:
                os.replace(self.ruta_archivo, respaldo)
            except OSError:
                pass
            self.guardar_categorias(self._categorias_iniciales())

    def leer_categorias(self) -> List[str]:
        self._asegurar_archivo()
        try:
            with self.ruta_archivo.open("r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except (OSError, json.JSONDecodeError):
            return self._categorias_iniciales()

        if not isinstance(datos, list):
            return self._categorias_iniciales()

        return self._ordenar(datos)

    def guardar_categorias(self, categorias: List[str]) -> None:
        datos = self._ordenar(categorias)
        temporal = self.ruta_archivo.with_suffix(".tmp")
        with temporal.open("w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
        os.replace(temporal, self.ruta_archivo)

    def agregar_categoria(self, categoria) -> str:
        categoria = validar_categoria(categoria)
        categorias = self.leer_categorias()
        if normalizar_texto(categoria) not in [normalizar_texto(c) for c in categorias]:
            categorias.append(categoria)
            self.guardar_categorias(categorias)
        return categoria
