from utils import mostrar_producto

def buscar_producto(inventario):
    nombre = input("Buscar nombre: ")

    for p in inventario:
        if p["nombre"] == nombre:
            print("Producto encontrado:")
            mostrar_producto(p)
            return

    print("Producto no encontrado")
