from producto import crear_producto

def cargar_datos(inventario):
    inventario.append(crear_producto("Tonico Facial", 80.0, 10))
    inventario.append(crear_producto("Limpiador Facial", 100.0, 20))
    inventario.append(crear_producto("Crema Hidratante", 250.0, 5))
