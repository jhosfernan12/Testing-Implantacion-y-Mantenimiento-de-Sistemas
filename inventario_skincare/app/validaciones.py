from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import math
import re
import unicodedata


MAX_NOMBRE = 60
MAX_CATEGORIA = 40
MAX_PRECIO = Decimal("999999.99")
MAX_STOCK = 1_000_000


def quitar_tildes(texto: str) -> str:
    texto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def normalizar_texto(texto: str) -> str:
    texto = str(texto).strip().lower()
    texto = quitar_tildes(texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto


def limpiar_texto(valor, campo: str, max_len: int, permitir_vacio: bool = False) -> str:
    if valor is None:
        valor = ""
    texto = str(valor).strip()
    texto = re.sub(r"\s+", " ", texto)

    if not texto and not permitir_vacio:
        raise ValueError(f"El campo {campo} no puede estar vacio.")

    if len(texto) > max_len:
        raise ValueError(f"El campo {campo} no puede tener mas de {max_len} caracteres.")

    return texto


def validar_nombre_producto(nombre) -> str:
    nombre = limpiar_texto(nombre, "nombre", MAX_NOMBRE)

    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9 .,'°#%()+\-/]+", nombre):
        raise ValueError("El nombre contiene caracteres no permitidos.")

    if not re.search(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9]", nombre):
        raise ValueError("El nombre debe tener letras o numeros.")

    return nombre.title()


def validar_categoria(categoria) -> str:
    categoria = limpiar_texto(categoria, "categoria", MAX_CATEGORIA, permitir_vacio=True)
    if not categoria:
        return "General"

    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9 .,'()+\-/]+", categoria):
        raise ValueError("La categoria contiene caracteres no permitidos.")

    return categoria.title()


def validar_precio(precio) -> float:
    if precio is None:
        raise ValueError("El precio no puede estar vacio.")

    texto = str(precio).strip().replace(",", ".")
    if not texto:
        raise ValueError("El precio no puede estar vacio.")

    try:
        valor = Decimal(texto)
    except InvalidOperation:
        raise ValueError("El precio debe ser un numero valido.")

    if not math.isfinite(float(valor)):
        raise ValueError("El precio debe ser un numero valido.")

    if valor <= 0:
        raise ValueError("El precio debe ser mayor que cero.")

    if valor > MAX_PRECIO:
        raise ValueError(f"El precio no puede ser mayor que {MAX_PRECIO}.")

    valor = valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(valor)


def validar_entero_no_negativo(valor, campo: str, maximo: int = MAX_STOCK) -> int:
    if valor is None:
        raise ValueError(f"El campo {campo} no puede estar vacio.")

    texto = str(valor).strip()
    if not texto:
        raise ValueError(f"El campo {campo} no puede estar vacio.")

    if not re.fullmatch(r"\d+", texto):
        raise ValueError(f"El campo {campo} debe ser un numero entero positivo o cero.")

    numero = int(texto)
    if numero < 0:
        raise ValueError(f"El campo {campo} no puede ser negativo.")

    if numero > maximo:
        raise ValueError(f"El campo {campo} no puede ser mayor que {maximo}.")

    return numero


def validar_entero_positivo(valor, campo: str, maximo: int = MAX_STOCK) -> int:
    numero = validar_entero_no_negativo(valor, campo, maximo)
    if numero == 0:
        raise ValueError(f"El campo {campo} debe ser mayor que cero.")
    return numero