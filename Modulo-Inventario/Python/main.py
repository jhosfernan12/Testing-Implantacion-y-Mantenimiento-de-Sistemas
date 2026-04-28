from menu import iniciar_menu
from datos_prueba import cargar_datos

if __name__ == "__main__":
    inventario = []
    cargar_datos(inventario)
    iniciar_menu(inventario)
