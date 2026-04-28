from producto import crear_producto
from utils import mostrar_producto

def registrar_producto(inventario):
    nombre = input("Nombre: ")
    precio = float(input("Precio: "))
    cantidad = int(input("Cantidad: "))

    producto = crear_producto(nombre, precio, cantidad)
    inventario.append(producto)

    print("Producto registrado")

def listar_productos(inventario):
    if len(inventario) == 0:
        print("Inventario vacio")
        return

    print("\nLista de productos:")
    for p in inventario:
        mostrar_producto(p)
