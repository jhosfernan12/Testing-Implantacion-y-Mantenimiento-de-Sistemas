from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import math
import re
import unicodedata


MAX_NOMBRE = 60
MAX_CATEGORIA = 40
MAX_PRECIO = Decimal("999999.99")
MAX_STOCK = 1_000_000
MIN_NOMBRE_LEN = 3


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


def capitalizar_nombre(texto: str) -> str:
    palabras = texto.split()
    palabras_capitalizadas = []
    for palabra in palabras:
        if palabra and len(palabra) > 0:
            palabras_capitalizadas.append(palabra[0].upper() + palabra[1:].lower())
    return " ".join(palabras_capitalizadas)


def validar_nombre_producto(nombre) -> str:
    nombre = limpiar_texto(nombre, "nombre", MAX_NOMBRE)

    if len(nombre) < MIN_NOMBRE_LEN:
        raise ValueError(f"El nombre debe tener al menos {MIN_NOMBRE_LEN} caracteres.")

    if not nombre[0].isalnum():
        raise ValueError("El nombre debe comenzar con una letra o numero.")

    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9 .,'°#%()+\-/]+", nombre):
        raise ValueError("El nombre contiene caracteres no permitidos.")

    if not re.search(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü]", nombre):
        raise ValueError("El nombre debe contener al menos una letra.")

    return capitalizar_nombre(nombre)


def validar_categoria(categoria) -> str:
    categoria = limpiar_texto(categoria, "categoria", MAX_CATEGORIA, permitir_vacio=True)
    if not categoria:
        return "General"

    if len(categoria) < 2:
        raise ValueError("La categoria debe tener al menos 2 caracteres.")

    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9 .,'()+\-/]+", categoria):
        raise ValueError("La categoria contiene caracteres no permitidos.")

    return capitalizar_nombre(categoria)


def validar_precio(precio) -> float:
    if precio is None:
        raise ValueError("El precio no puede estar vacio.")

    texto = str(precio).strip().replace(",", ".")
    
    if not texto:
        raise ValueError("El precio no puede estar vacio.")
    
    if "e" in texto.lower():
        raise ValueError("No se permite notacion cientifica. Use un numero normal como 10.50")

    try:
        valor = Decimal(texto)
    except InvalidOperation:
        raise ValueError("El precio debe ser un numero valido. Use punto decimal, no coma.")

    if not math.isfinite(float(valor)):
        raise ValueError("El precio debe ser un numero valido.")

    if valor <= 0:
        raise ValueError("El precio debe ser mayor que cero.")

    if valor < Decimal("0.01"):
        raise ValueError("El precio no puede ser menor a 0.01.")

    if valor > MAX_PRECIO:
        raise ValueError(f"El precio no puede ser mayor que {MAX_PRECIO}.")

    if valor.as_tuple().exponent < -2:
        raise ValueError("El precio no puede tener mas de 2 decimales.")

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


def validar_stock_minimo(stock_minimo: int, stock_actual: int) -> int:
    stock_minimo = validar_entero_no_negativo(stock_minimo, "stock minimo", MAX_STOCK)
    
    if stock_actual == 0:
        if stock_minimo != 0:
            raise ValueError("Si el stock es 0, el stock minimo tambien debe ser 0.")
    else:
        if stock_minimo >= stock_actual:
            raise ValueError(f"El stock minimo ({stock_minimo}) debe ser menor que el stock actual ({stock_actual}).")
    
    return stock_minimo