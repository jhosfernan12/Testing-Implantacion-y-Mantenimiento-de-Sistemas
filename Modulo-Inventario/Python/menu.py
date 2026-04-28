from inventario import registrar_producto, listar_productos
from busqueda import buscar_producto

def iniciar_menu(inventario):
    while True:
        print("\n--- MENU INVENTARIO ---")
        print("1. Registrar producto")
        print("2. Buscar producto")
        print("3. Listar productos")
        print("4. Salir")

        opcion = input("Opcion: ")

        if opcion == "1":
            registrar_producto(inventario)
        elif opcion == "2":
            buscar_producto(inventario)
        elif opcion == "3":
            listar_productos(inventario)
        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opcion invalida")
