inventario = [
    {"nombre": "lapiz", "precio": 1.5, "cantidad": 100},
    {"nombre": "cuaderno", "precio": 5.0, "cantidad": 50}
]

def registrar_producto():
    print("\n--- Registrar producto ---")
    nombre = input("Nombre: ")
    precio = float(input("Precio: "))
    cantidad = int(input("Cantidad: "))

    producto = {
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad
    }

    inventario.append(producto)
    print("Producto registrado correctamente")

def buscar_producto():
    print("\n--- Buscar producto ---")
    nombre = input("Ingrese nombre: ")

    for p in inventario:
        if p["nombre"] == nombre:
            print("Producto encontrado:")
            print("Nombre:", p["nombre"])
            print("Precio:", p["precio"])
            print("Cantidad:", p["cantidad"])
            return

    print("Producto no encontrado")

def listar_productos():
    print("\n--- Lista de productos ---")
    
    if len(inventario) == 0:
        print("Inventario vacio")
    else:
        for i, p in enumerate(inventario, start=1):
            print(i, "-", p["nombre"], "| Precio:", p["precio"], "| Cantidad:", p["cantidad"])

def menu():
    while True:
        print("\n===== MENU INVENTARIO =====")
        print("1. Registrar producto")
        print("2. Buscar producto")
        print("3. Listar productos")
        print("4. Salir")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            buscar_producto()
        elif opcion == "3":
            listar_productos()
        elif opcion == "4":
            print("Saliendo del sistema...")
            break
        else:
            print("Opcion invalida")

if __name__ == "__main__":
    menu()
