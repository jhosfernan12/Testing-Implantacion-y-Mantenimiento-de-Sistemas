from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Producto:
    codigo: str
    nombre: str
    precio: float
    stock: int
    categoria: str = "General"
    stock_minimo: int = 5
    fecha_registro: str = ""

    def __post_init__(self):
        if not self.fecha_registro:
            self.fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            codigo=str(data.get("codigo", "")).strip(),
            nombre=str(data.get("nombre", "")).strip(),
            precio=float(data.get("precio", 0)),
            stock=int(data.get("stock", 0)),
            categoria=str(data.get("categoria", "General")).strip() or "General",
            stock_minimo=int(data.get("stock_minimo", 5)),
            fecha_registro=str(data.get("fecha_registro", "")).strip(),
        )
