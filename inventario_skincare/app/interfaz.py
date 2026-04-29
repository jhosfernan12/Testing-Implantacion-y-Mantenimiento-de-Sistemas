import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from app.servicios import InventarioServicio


class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventario Skincare - Guerra de Testers")
        self.root.geometry("1260x760")
        self.root.minsize(1060, 650)
        self.root.configure(bg="#fff7fb")

        self.servicio = InventarioServicio()
        self.codigo_seleccionado = None

        self.colores = {
            "fondo": "#fff4f8",
            "panel": "#ffffff",
            "panel_suave": "#ffe7f0",
            "panel_muy_suave": "#fff9fc",
            "rosa_pastel": "#ffddea",
            "rosa_claro": "#ffcfe0",
            "rosa_medio": "#f4a8c7",
            "rosa_boton": "#f6a9c8",
            "rosa_boton_hover": "#ee8fb8",
            "rosa_texto": "#8a315d",
            "rosa_oscuro": "#6f244b",
            "texto": "#4a2738",
            "texto_suave": "#7d5870",
            "borde": "#f5bdd5",
            "peligro": "#cf5f7d",
            "peligro_hover": "#bd4d6c",
            "exito": "#507f67",
            "advertencia": "#9a6a00",
        }

        self.var_nombre = tk.StringVar()
        self.var_precio = tk.StringVar()
        self.var_stock = tk.StringVar()
        self.var_categoria = tk.StringVar(value="General")
        self.var_stock_minimo = tk.StringVar(value="5")
        self.var_busqueda = tk.StringVar()

        self._crear_estilos()
        self._crear_interfaz()
        self._cargar_categorias()
        self._listar_productos()
        self._configurar_navegacion()

    def _crear_estilos(self):
        self.estilo = ttk.Style()
        self.estilo.theme_use("clam")

        self.estilo.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=34,
            background=self.colores["panel"],
            fieldbackground=self.colores["panel"],
            foreground=self.colores["texto"],
            bordercolor=self.colores["borde"],
            lightcolor=self.colores["borde"],
            darkcolor=self.colores["borde"],
        )
        self.estilo.map(
            "Treeview",
            background=[("selected", self.colores["rosa_medio"])],
            foreground=[("selected", "white")],
        )
        self.estilo.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background=self.colores["rosa_pastel"],
            foreground=self.colores["rosa_oscuro"],
            relief="flat",
            padding=7,
        )
        self.estilo.map("Treeview.Heading", background=[("active", self.colores["rosa_claro"])])

        self.estilo.configure(
            "Bonito.TEntry",
            font=("Segoe UI", 10),
            padding=7,
            fieldbackground=self.colores["panel_muy_suave"],
            bordercolor=self.colores["borde"],
            lightcolor=self.colores["borde"],
            darkcolor=self.colores["borde"],
        )

        self.estilo.configure(
            "Bonito.TCombobox",
            font=("Segoe UI", 10),
            padding=7,
            fieldbackground=self.colores["panel_muy_suave"],
            background=self.colores["panel_muy_suave"],
            bordercolor=self.colores["borde"],
            arrowcolor=self.colores["rosa_oscuro"],
            lightcolor=self.colores["borde"],
            darkcolor=self.colores["borde"],
        )

    def _crear_interfaz(self):
        contenedor = tk.Frame(self.root, bg=self.colores["fondo"])
        contenedor.pack(fill="both", expand=True, padx=22, pady=18)

        self._crear_encabezado(contenedor)
        self._crear_barra_acciones(contenedor)

        cuerpo = tk.Frame(contenedor, bg=self.colores["fondo"])
        cuerpo.pack(fill="both", expand=True, pady=(14, 0))

        self._crear_panel_formulario(cuerpo)
        self._crear_panel_tabla(cuerpo)

        self.lbl_estado = tk.Label(
            contenedor,
            text="Sistema listo.",
            bg=self.colores["panel_suave"],
            fg=self.colores["rosa_oscuro"],
            font=("Segoe UI", 10, "bold"),
            anchor="w",
            padx=14,
            pady=9,
        )
        self.lbl_estado.pack(fill="x", pady=(12, 0))

    def _crear_encabezado(self, padre):
        encabezado = tk.Frame(
            padre,
            bg=self.colores["rosa_pastel"],
            highlightthickness=1,
            highlightbackground=self.colores["borde"],
        )
        encabezado.pack(fill="x")

        contenido = tk.Frame(encabezado, bg=self.colores["rosa_pastel"])
        contenido.pack(fill="x", padx=20, pady=14)

        tk.Label(
            contenido,
            text="Módulo de Inventario Skincare",
            bg=self.colores["rosa_pastel"],
            fg=self.colores["rosa_oscuro"],
            font=("Segoe UI", 24, "bold"),
        ).pack(anchor="w")


    def _crear_barra_acciones(self, padre):
        barra = tk.Frame(
            padre,
            bg=self.colores["panel"],
            highlightthickness=1,
            highlightbackground=self.colores["borde"],
        )
        barra.pack(fill="x", pady=(12, 0))

        for columna in range(7):
            barra.columnconfigure(columna, weight=1, uniform="acciones")

        botones = [
            ("Nuevo producto", self._limpiar_formulario, self.colores["panel_suave"], self.colores["rosa_oscuro"]),
            ("Registrar producto", self._registrar_producto, self.colores["rosa_boton"], "white"),
            ("Actualizar producto", self._actualizar_producto, self.colores["rosa_claro"], self.colores["rosa_oscuro"]),
            ("Vender", self._vender_producto, "#ffdce9", self.colores["rosa_oscuro"]),
            ("Eliminar", self._eliminar_producto, self.colores["peligro"], "white"),
            ("Stock bajo", self._mostrar_stock_bajo, "#ffe7ba", self.colores["rosa_oscuro"]),
            ("Listar todo", self._listar_productos, self.colores["panel_suave"], self.colores["rosa_oscuro"]),
        ]

        for columna, (texto, comando, fondo, color_texto) in enumerate(botones):
            boton = self._crear_boton(
                barra,
                texto,
                comando,
                fondo,
                color_texto,
                grande=True,
            )
            boton.grid(row=0, column=columna, sticky="ew", padx=6, pady=10)

    def _crear_panel_formulario(self, padre):
        panel = tk.Frame(
            padre,
            bg=self.colores["panel"],
            highlightthickness=1,
            highlightbackground=self.colores["borde"],
            width=405,
        )
        panel.pack(side="left", fill="y", padx=(0, 18))
        panel.pack_propagate(False)

        tk.Label(
            panel,
            text="Datos del producto",
            bg=self.colores["panel"],
            fg=self.colores["rosa_oscuro"],
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w", padx=20, pady=(18, 4))


        self.entrada_nombre = self._agregar_campo(panel, "Nombre del producto", self.var_nombre)
        self.entrada_precio = self._agregar_campo(panel, "Precio", self.var_precio)
        self.entrada_stock = self._agregar_campo(panel, "Stock", self.var_stock)
        self._agregar_combo_categoria(panel)
        self.entrada_stock_minimo = self._agregar_campo(panel, "Stock mínimo", self.var_stock_minimo)

        botones = tk.Frame(panel, bg=self.colores["panel"])
        botones.pack(fill="x", padx=20, pady=(14, 8))

        self._crear_boton(
            botones,
            "Registrar producto",
            self._registrar_producto,
            self.colores["rosa_boton"],
            grande=True,
        ).pack(fill="x", pady=(0, 8))

        self._crear_boton(
            botones,
            "Actualizar producto",
            self._actualizar_producto,
            self.colores["rosa_claro"],
            self.colores["rosa_oscuro"],
            grande=True,
        ).pack(fill="x", pady=(0, 8))

        fila_secundaria_1 = tk.Frame(botones, bg=self.colores["panel"])
        fila_secundaria_1.pack(fill="x", pady=(0, 6))
        self._crear_boton(
            fila_secundaria_1,
            "Vender",
            self._vender_producto,
            "#ffdce9",
            self.colores["rosa_oscuro"],
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))
        self._crear_boton(
            fila_secundaria_1,
            "Eliminar",
            self._eliminar_producto,
            self.colores["peligro"],
        ).pack(side="left", fill="x", expand=True, padx=(5, 0))

        self._crear_boton(
            botones,
            "Limpiar campos",
            self._limpiar_formulario,
            self.colores["panel_suave"],
            self.colores["rosa_oscuro"],
        ).pack(fill="x", pady=(2, 0))


    def _crear_panel_tabla(self, padre):
        panel = tk.Frame(padre, bg=self.colores["fondo"])
        panel.pack(side="right", fill="both", expand=True)

        barra_busqueda = tk.Frame(
            panel,
            bg=self.colores["panel"],
            highlightthickness=1,
            highlightbackground=self.colores["borde"],
        )
        barra_busqueda.pack(fill="x", pady=(0, 12))

        tk.Label(
            barra_busqueda,
            text="Buscar:",
            bg=self.colores["panel"],
            fg=self.colores["rosa_oscuro"],
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=(14, 6), pady=12)

        self.entrada_busqueda = ttk.Entry(barra_busqueda, textvariable=self.var_busqueda, style="Bonito.TEntry")
        self.entrada_busqueda.pack(side="left", fill="x", expand=True, padx=(0, 8), pady=10, ipady=2)
        self.entrada_busqueda.bind("<Return>", lambda _event: self._buscar_producto())

        self._crear_boton(barra_busqueda, "Buscar", self._buscar_producto, self.colores["rosa_boton"]).pack(side="left", padx=4, pady=10)
        self._crear_boton(barra_busqueda, "Listar todo", self._listar_productos, self.colores["panel_suave"], self.colores["rosa_oscuro"]).pack(side="left", padx=4, pady=10)
        self._crear_boton(barra_busqueda, "Stock bajo", self._mostrar_stock_bajo, "#ffdeeb", self.colores["rosa_oscuro"]).pack(side="left", padx=(4, 14), pady=10)

        marco_tabla = tk.Frame(
            panel,
            bg=self.colores["panel"],
            highlightthickness=1,
            highlightbackground=self.colores["borde"],
        )
        marco_tabla.pack(fill="both", expand=True)

        columnas = ("codigo", "nombre", "precio", "stock", "categoria", "stock_minimo", "estado")
        self.tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings")
        self.tabla.heading("codigo", text="Código")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("stock", text="Stock")
        self.tabla.heading("categoria", text="Categoría")
        self.tabla.heading("stock_minimo", text="Stock mín.")
        self.tabla.heading("estado", text="Estado")

        self.tabla.column("codigo", width=80, anchor="center", stretch=False)
        self.tabla.column("nombre", width=250, anchor="w")
        self.tabla.column("precio", width=100, anchor="e", stretch=False)
        self.tabla.column("stock", width=80, anchor="center", stretch=False)
        self.tabla.column("categoria", width=145, anchor="w")
        self.tabla.column("stock_minimo", width=90, anchor="center", stretch=False)
        self.tabla.column("estado", width=130, anchor="center", stretch=False)

        self.tabla.tag_configure("normal", background="#ffffff")
        self.tabla.tag_configure("par", background=self.colores["panel_muy_suave"])
        self.tabla.tag_configure("bajo", background="#fff0d6", foreground=self.colores["advertencia"])
        self.tabla.tag_configure("agotado", background="#ffe1ea", foreground=self.colores["peligro"])

        scroll_y = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla.yview)
        scroll_x = ttk.Scrollbar(marco_tabla, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tabla.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=(10, 0))
        scroll_y.grid(row=0, column=1, sticky="ns", pady=(10, 0), padx=(0, 10))
        scroll_x.grid(row=1, column=0, sticky="ew", padx=(10, 0), pady=(0, 10))

        marco_tabla.rowconfigure(0, weight=1)
        marco_tabla.columnconfigure(0, weight=1)

        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar_producto)
        self.tabla.bind("<Double-1>", lambda _event: self._mostrar_mensaje("Producto cargado en el formulario para editar."))

    def _agregar_campo(self, padre, etiqueta, variable):
        marco = tk.Frame(padre, bg=self.colores["panel"])
        marco.pack(fill="x", padx=20, pady=5)

        tk.Label(
            marco,
            text=etiqueta,
            bg=self.colores["panel"],
            fg=self.colores["rosa_oscuro"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")

        entrada = ttk.Entry(marco, textvariable=variable, style="Bonito.TEntry")
        entrada.pack(fill="x", ipady=3)

        return entrada

    def _agregar_combo_categoria(self, padre):
        marco = tk.Frame(padre, bg=self.colores["panel"])
        marco.pack(fill="x", padx=20, pady=5)

        tk.Label(
            marco,
            text="Categoría",
            bg=self.colores["panel"],
            fg=self.colores["rosa_oscuro"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")

        fila = tk.Frame(marco, bg=self.colores["panel"])
        fila.pack(fill="x")

        self.combo_categoria = ttk.Combobox(
            fila,
            textvariable=self.var_categoria,
            style="Bonito.TCombobox",
            state="readonly",
        )
        self.combo_categoria.pack(side="left", fill="x", expand=True, ipady=3)

        self._crear_boton(
            fila,
            "+ categoría",
            self._agregar_nueva_categoria,
            self.colores["panel_suave"],
            self.colores["rosa_oscuro"],
            ancho=None,
        ).pack(side="left", padx=(8, 0), ipady=1)


    def _crear_boton(self, padre, texto, comando, fondo, texto_color="white", grande=False, ancho=None):
        boton = tk.Button(
            padre,
            text=texto,
            command=comando,
            bg=fondo,
            fg=texto_color,
            activebackground=self.colores["rosa_boton_hover"],
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=14,
            pady=12 if grande else 8,
            width=ancho,
            font=("Segoe UI", 11 if grande else 10, "bold"),
            cursor="hand2",
        )
        hover = self.colores["peligro_hover"] if fondo == self.colores["peligro"] else self.colores["rosa_boton_hover"]
        boton.bind("<Enter>", lambda _e: boton.config(bg=hover))
        boton.bind("<Leave>", lambda _e: boton.config(bg=fondo))
        return boton

    def _configurar_navegacion(self):
        self.root.bind("<Control-f>", lambda _event: self._enfocar_busqueda())
        self.root.bind("<Control-F>", lambda _event: self._enfocar_busqueda())
        self.root.bind("<Control-n>", lambda _event: self._limpiar_formulario())
        self.root.bind("<Control-N>", lambda _event: self._limpiar_formulario())
        self.root.bind("<Escape>", lambda _event: self._limpiar_formulario())
        self.entrada_nombre.focus_set()

    def _enfocar_busqueda(self):
        self.entrada_busqueda.focus_set()
        self.entrada_busqueda.select_range(0, tk.END)

    def _cargar_categorias(self):
        try:
            categorias = self.servicio.obtener_categorias()
        except ValueError:
            categorias = ["General"]

        if not categorias:
            categorias = ["General"]

        self.combo_categoria.configure(values=categorias)

        if self.var_categoria.get() not in categorias:
            self.var_categoria.set(categorias[0])

    def _agregar_nueva_categoria(self):
        try:
            nueva = simpledialog.askstring("Nueva categoría", "Ingrese el nombre de la nueva categoría:")
            if nueva is None:
                return

            categoria = self.servicio.agregar_categoria(nueva)
            self._cargar_categorias()
            self.var_categoria.set(categoria)
            self._mostrar_mensaje(f"Categoría agregada: {categoria}")
        except ValueError as error:
            self._mostrar_error(error)

    def _mostrar_mensaje(self, texto):
        self.lbl_estado.config(text=texto)

    def _mostrar_error(self, error):
        messagebox.showerror("Validación", str(error))
        self._mostrar_mensaje("Revise los datos ingresados.")

    def _mostrar_productos(self, productos):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for posicion, producto in enumerate(productos):
            if producto.stock == 0:
                estado = "Agotado"
                etiqueta = "agotado"
            elif producto.stock <= producto.stock_minimo:
                estado = "Stock bajo"
                etiqueta = "bajo"
            else:
                estado = "Disponible"
                etiqueta = "par" if posicion % 2 == 0 else "normal"

            self.tabla.insert(
                "",
                "end",
                values=(
                    producto.codigo,
                    producto.nombre,
                    f"S/ {producto.precio:.2f}",
                    producto.stock,
                    producto.categoria,
                    producto.stock_minimo,
                    estado,
                ),
                tags=(etiqueta,),
            )

        self._cargar_categorias()
        self._mostrar_mensaje(f"Productos mostrados: {len(productos)}")

    def _listar_productos(self):
        productos = self.servicio.listar_productos()
        self._mostrar_productos(productos)

    def _buscar_producto(self):
        try:
            termino = self.var_busqueda.get()
            if not termino.strip():
                self._listar_productos()
                return

            productos = self.servicio.buscar_producto(termino)
            self._mostrar_productos(productos)
        except ValueError as error:
            self._mostrar_error(error)

    def _registrar_producto(self):
        try:
            producto = self.servicio.registrar_producto(
                self.var_nombre.get(),
                self.var_precio.get(),
                self.var_stock.get(),
                self.var_categoria.get(),
                self.var_stock_minimo.get(),
            )
            messagebox.showinfo("Registro correcto", f"Producto registrado: {producto.nombre}")
            self._limpiar_formulario()
            self._listar_productos()
        except ValueError as error:
            self._mostrar_error(error)

    def _actualizar_producto(self):
        try:
            clave = self.codigo_seleccionado or self.var_nombre.get()
            if not str(clave or "").strip():
                raise ValueError("Seleccione un producto de la tabla o escriba el nombre exacto del producto.")

            producto = self.servicio.actualizar_producto(
                clave,
                self.var_nombre.get(),
                self.var_precio.get(),
                self.var_stock.get(),
                self.var_categoria.get(),
                self.var_stock_minimo.get(),
            )
            messagebox.showinfo(
                "Actualización correcta",
                f"Producto actualizado: {producto.nombre}\nPrecio: S/ {producto.precio:.2f}\nStock: {producto.stock}",
            )
            self.codigo_seleccionado = producto.codigo
            self._listar_productos()
            self._seleccionar_por_codigo(producto.codigo)
        except ValueError as error:
            self._mostrar_error(error)

    def _vender_producto(self):
        try:
            clave = self.codigo_seleccionado or self.var_nombre.get()
            if not str(clave or "").strip():
                raise ValueError("Seleccione un producto para vender.")

            cantidad = simpledialog.askinteger("Venta", "Ingrese la cantidad a vender:", minvalue=1, maxvalue=1000000)
            if cantidad is None:
                return

            producto = self.servicio.vender_producto(clave, cantidad)
            messagebox.showinfo("Venta registrada", f"Venta realizada. Stock actual de {producto.nombre}: {producto.stock}")
            self._listar_productos()
            self._seleccionar_por_codigo(producto.codigo)
        except ValueError as error:
            self._mostrar_error(error)

    def _eliminar_producto(self):
        try:
            clave = self.codigo_seleccionado or self.var_nombre.get()
            if not str(clave or "").strip():
                raise ValueError("Seleccione un producto para eliminar.")

            try:
                producto = self.servicio.eliminar_producto(clave)
            except ValueError as error:
                if "tiene stock" in str(error).lower():
                    confirmar = messagebox.askyesno(
                        "Confirmar eliminación",
                        "El producto todavía tiene stock. ¿Desea eliminarlo de todos modos?",
                    )
                    if not confirmar:
                        return
                    producto = self.servicio.eliminar_producto(clave, forzar=True)
                else:
                    raise

            messagebox.showinfo("Eliminación correcta", f"Producto eliminado: {producto.nombre}")
            self._limpiar_formulario()
            self._listar_productos()
        except ValueError as error:
            self._mostrar_error(error)

    def _mostrar_stock_bajo(self):
        try:
            productos = self.servicio.reporte_stock_bajo()
            self._mostrar_productos(productos)
            if not productos:
                messagebox.showinfo("Stock bajo", "No hay productos con stock bajo.")
        except ValueError as error:
            self._mostrar_error(error)

    def _seleccionar_producto(self, _evento):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            return

        valores = self.tabla.item(seleccionado[0], "values")
        if not valores:
            return

        self.codigo_seleccionado = valores[0]
        self.var_nombre.set(valores[1])
        self.var_precio.set(str(valores[2]).replace("S/", "").strip())
        self.var_stock.set(str(valores[3]))
        self.var_categoria.set(valores[4])
        self.var_stock_minimo.set(str(valores[5]))
        self._mostrar_mensaje(f"Producto seleccionado: {valores[1]} ({valores[0]})")

    def _seleccionar_por_codigo(self, codigo):
        for item in self.tabla.get_children():
            valores = self.tabla.item(item, "values")
            if valores and valores[0] == codigo:
                self.tabla.selection_set(item)
                self.tabla.focus(item)
                self.tabla.see(item)
                self._seleccionar_producto(None)
                return

    def _limpiar_formulario(self):
        self.codigo_seleccionado = None
        self.var_nombre.set("")
        self.var_precio.set("")
        self.var_stock.set("")
        self.var_categoria.set("General")
        self.var_stock_minimo.set("5")
        self.tabla.selection_remove(self.tabla.selection())
        self.entrada_nombre.focus_set()
        self._mostrar_mensaje("Campos listos para registrar un producto.")
