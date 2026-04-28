# modulo inventario - version simple pero organizada

class Producto:
    def __init__(self, nombre, precio, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def __str__(self):
        return f"Nombre: {self.nombre} | Precio: {self.precio} | Cantidad: {self.cantidad}"


class Inventario:
    def __init__(self):
        self.productos = []

    # datos de prueba
    def cargar_datos_prueba(self):
        self.productos.append(Producto("Laptop", 2500, 5))
        self.productos.append(Producto("Mouse", 50, 20))
        self.productos.append(Producto("Teclado", 120, 10))

    # funcionalidad 1
    def registrar_producto(self):
        nombre = input("Nombre: ")
        
        try:
            precio = float(input("Precio: "))
            cantidad = int(input("Cantidad: "))
        except:
            print("Error en los datos")
            return

        nuevo = Producto(nombre, precio, cantidad)
        self.productos.append(nuevo)
        print("Producto registrado")

    # funcionalidad 2
    def buscar_producto(self):
        nombre = input("Buscar nombre: ")

        for p in self.productos:
            if p.nombre == nombre:
                print("Producto encontrado:")
                print(p)
                return

        print("Producto no encontrado")

    # funcionalidad 3
    def listar_productos(self):
        if len(self.productos) == 0:
            print("Inventario vacio")
            return

        print("\nLista de productos:")
        for i, p in enumerate(self.productos):
            print(f"{i+1}. {p}")


def menu():
    inventario = Inventario()
    inventario.cargar_datos_prueba()

    while True:
        print("\n--- MENU INVENTARIO ---")
        print("1. Registrar producto")
        print("2. Buscar producto")
        print("3. Listar productos")
        print("4. Salir")

        opcion = input("Opcion: ")

        if opcion == "1":
            inventario.registrar_producto()
        elif opcion == "2":
            inventario.buscar_producto()
        elif opcion == "3":
            inventario.listar_productos()
        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opcion invalida")


if __name__ == "__main__":
    menu()
