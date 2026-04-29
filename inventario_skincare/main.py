import tkinter as tk

from app.interfaz import InventarioApp


def main():
    root = tk.Tk()
    InventarioApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
