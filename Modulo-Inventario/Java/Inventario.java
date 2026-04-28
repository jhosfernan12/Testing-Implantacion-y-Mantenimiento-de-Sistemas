import java.util.ArrayList;
import java.util.Scanner;

class Producto {
    String nombre;
    double precio;
    int cantidad;

    public Producto(String nombre, double precio, int cantidad) {
        this.nombre = nombre;
        this.precio = precio;
        this.cantidad = cantidad;
    }

    public String toString() {
        return "Nombre: " + nombre + ", Precio: " + precio + ", Cantidad: " + cantidad;
    }
}

public class Inventario {

    static ArrayList<Producto> inventario = new ArrayList<>();
    static Scanner sc = new Scanner(System.in);

    public static void registrarProducto() {
        System.out.print("Nombre: ");
        String nombre = sc.nextLine();

        System.out.print("Precio: ");
        double precio = sc.nextDouble();

        System.out.print("Cantidad: ");
        int cantidad = sc.nextInt();
        sc.nextLine();

        Producto p = new Producto(nombre, precio, cantidad);
        inventario.add(p);

        System.out.println("Producto registrado");
    }

    public static void buscarProducto() {
        System.out.print("Buscar nombre: ");
        String nombre = sc.nextLine();

        for (Producto p : inventario) {
            if (p.nombre.equals(nombre)) {
                System.out.println("Encontrado: " + p);
                return;
            }
        }

        System.out.println("Producto no encontrado");
    }

    public static void listarProductos() {
        if (inventario.isEmpty()) {
            System.out.println("Inventario vacio");
        } else {
            for (Producto p : inventario) {
                System.out.println(p);
            }
        }
    }

    public static void menu() {
        while (true) {
            System.out.println("\n1. Registrar");
            System.out.println("2. Buscar");
            System.out.println("3. Listar");
            System.out.println("4. Salir");

            System.out.print("Opcion: ");
            int opcion = sc.nextInt();
            sc.nextLine();

            if (opcion == 1) {
                registrarProducto();
            } else if (opcion == 2) {
                buscarProducto();
            } else if (opcion == 3) {
                listarProductos();
            } else if (opcion == 4) {
                break;
            } else {
                System.out.println("Opcion invalida");
            }
        }
    }

    public static void main(String[] args) {
        menu();
    }
}
