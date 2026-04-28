inventario = []

def registrar_producto():
    nombre = input("Nombre: ")
    precio = float(input("Precio: "))
    cantidad = int(input("Cantidad: "))

    producto = {
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad
    }

    inventario.append(producto)
    print("Producto registrado")

def buscar_producto():
    nombre = input("Buscar nombre: ")

    for p in inventario:
        if p["nombre"] == nombre:
            print("Encontrado:", p)
            return

    print("Producto no encontrado")

def listar_productos():
    if len(inventario) == 0:
        print("Inventario vacio")
    else:
        for p in inventario:
            print(p)

def menu():
    while True:
        print("\n1. Registrar")
        print("2. Buscar")
        print("3. Listar")
        print("4. Salir")

        opcion = input("Opcion: ")

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            buscar_producto()
        elif opcion == "3":
            listar_productos()
        elif opcion == "4":
            break
        else:
            print("Opcion invalida")

menu()
