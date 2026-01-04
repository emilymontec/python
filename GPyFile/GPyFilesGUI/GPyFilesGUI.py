import os
import time
import hashlib
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import stat
import platform

class GPyFilesGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GPyFiles - GUI")
        self.geometry("1300x700")
        self.configure(bg="#000000")
        
        # Variables
        self.current_dir = None
        self.search_var = tk.StringVar(value="")
        self.ext_filter_var = tk.StringVar(value="")
        self.show_hidden_var = tk.BooleanVar(value=False)
        
        self.setup_styles()
        self._create_menu()
        self._create_widgets()
        self._create_bindings()
        self._create_context_menu()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configuración de Treeview
        style.configure("Minimal.Treeview",
                       background="#000000",
                       foreground="#FFFFFF",
                       fieldbackground="#000000",
                       borderwidth=0,
                       relief="flat",
                       rowheight=30)
        style.configure("Minimal.Treeview.Heading",
                       background="#1a1a1a",
                       foreground="#FFD700",
                       borderwidth=0,
                       relief="flat",
                       font=('Segoe UI', 10, 'bold'))
        style.map("Minimal.Treeview",
                 background=[('selected', '#333333')],
                 foreground=[('selected', '#FFD700')])

    def _create_menu(self):
        menubar = tk.Menu(self, bg="#000000", fg="#FFD700", 
                         activebackground="#FFD700", activeforeground="#000000",
                         borderwidth=0, relief="flat", font=('Segoe UI', 9))
        self.config(menu=menubar)
        
        archivo_menu = tk.Menu(menubar, tearoff=0, bg="#1a1a1a", fg="#FFFFFF",
                              activebackground="#FFD700", activeforeground="#000000",
                              font=('Segoe UI', 9))
        menubar.add_cascade(label="Archivo", menu=archivo_menu)
        archivo_menu.add_command(label="Abrir carpeta...", command=self._choose_directory)
        archivo_menu.add_command(label="Refrescar", command=self._refresh)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.quit)
        
        herramientas_menu = tk.Menu(menubar, tearoff=0, bg="#1a1a1a", fg="#FFFFFF",
                                    activebackground="#FFD700", activeforeground="#000000",
                                    font=('Segoe UI', 9))
        menubar.add_cascade(label="Herramientas", menu=herramientas_menu)
        herramientas_menu.add_command(label="Renombrar archivo", command=self._rename_selected)
        herramientas_menu.add_command(label="Eliminar archivo", command=self._delete_selected)
        herramientas_menu.add_separator()
        herramientas_menu.add_command(label="Renombrado por lotes", command=self._batch_rename_selected)
        herramientas_menu.add_command(label="Buscar duplicados...", command=self._find_duplicates)
        herramientas_menu.add_command(label="Propiedades", command=self._file_properties)
        herramientas_menu.add_command(label="Crear carpeta nueva", command=self._new_folder)
        herramientas_menu.add_command(label="Crear archivo...", command=self._new_file)
        herramientas_menu.add_command(label="Mover a...", command=self._move_selected)
        
        ayuda_menu = tk.Menu(menubar, tearoff=0, bg="#1a1a1a", fg="#FFFFFF",
                            activebackground="#FFD700", activeforeground="#000000",
                            font=('Segoe UI', 9))
        menubar.add_cascade(label="Ayuda", menu=ayuda_menu)
        ayuda_menu.add_command(label="Acerca de", command=self._about)

    def _create_widgets(self):
        # Toolbar
        toolbar = tk.Frame(self, bg="#000000", height=60)
        toolbar.pack(fill=tk.X, padx=15, pady=15)
        
        btn_style = {
            'bg': '#FFD700',
            'fg': '#000000',
            'font': ('Segoe UI', 9, 'bold'),
            'relief': 'flat',
            'borderwidth': 0,
            'padx': 20,
            'pady': 10,
            'cursor': 'hand2',
            'activebackground': '#FFC700',
            'activeforeground': '#000000'
        }
        
        buttons = [
            ("Abrir carpeta", self._choose_directory),
            ("Nuevo archivo", self._new_file),
            ("Refrescar", self._refresh),
            ("Renombrar", self._rename_selected),
            ("Eliminar", self._delete_selected),
            ("Copiar", self._copy_selected)
        ]
        
        for i, (text, cmd) in enumerate(buttons):
            btn = tk.Button(toolbar, text=text, command=cmd, **btn_style)
            btn.pack(side=tk.LEFT, padx=3)
        
        # Búsqueda
        search_frame = tk.Frame(toolbar, bg="#000000")
        search_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(search_frame, text="Buscar:", bg="#000000", fg="#FFD700",
                font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=5)
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                               bg="#1a1a1a", fg="#FFFFFF", relief="flat",
                               borderwidth=0, font=('Segoe UI', 9),
                               insertbackground="#FFD700")
        search_entry.pack(side=tk.LEFT, ipadx=5, ipady=5)
        
        tk.Button(search_frame, text="Ir", command=self._search,
                 bg="#FFD700", fg="#000000", relief="flat", borderwidth=0,
                 font=('Segoe UI', 9, 'bold'), padx=15, pady=5,
                 cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        # Filtro y opciones
        filter_frame = tk.Frame(toolbar, bg="#000000")
        filter_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Button(filter_frame, text="Limpiar", command=self._clear_search,
                 bg="#FFD700", fg="#000000", relief="flat", borderwidth=0,
                 font=('Segoe UI', 9, 'bold'), padx=15, pady=5,
                 cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        tk.Label(filter_frame, text="Ext(s):", bg="#000000", fg="#FFD700",
                font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=5)
        
        ext_entry = tk.Entry(filter_frame, textvariable=self.ext_filter_var,
                            bg="#1a1a1a", fg="#FFFFFF", relief="flat",
                            borderwidth=0, font=('Segoe UI', 9), width=10,
                            insertbackground="#FFD700")
        ext_entry.pack(side=tk.LEFT, ipadx=5, ipady=5)
        
        tk.Checkbutton(filter_frame, text="Mostrar ocultos",
                      variable=self.show_hidden_var, command=self._refresh,
                      bg="#000000", fg="#FFFFFF", selectcolor="#1a1a1a",
                      activebackground="#000000", activeforeground="#FFD700",
                      font=('Segoe UI', 9), relief="flat", borderwidth=0,
                      cursor='hand2').pack(side=tk.LEFT, padx=10)
        
        # Main area
        main_frame = tk.Frame(self, bg="#000000")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Panel izquierdo - Lista de archivos
        left_frame = tk.Frame(main_frame, bg="#000000")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        columns = ('name', 'type', 'size', 'modified')
        self.tree = ttk.Treeview(left_frame, columns=columns, show='headings',
                                style="Minimal.Treeview", selectmode='extended')
        
        self.tree.heading('name', text='Nombre')
        self.tree.heading('type', text='Tipo')
        self.tree.heading('size', text='Tamaño')
        self.tree.heading('modified', text='Modificado')
        
        self.tree.column('name', width=300)
        self.tree.column('type', width=100)
        self.tree.column('size', width=100)
        self.tree.column('modified', width=150)
        
        # Scrollbar
        vsb = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Panel derecho - Previsualización
        right_frame = tk.Frame(main_frame, bg="#000000", width=500)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(15, 0))
        right_frame.pack_propagate(False)
        
        tk.Label(right_frame, text="Previsualización / Registro",
                bg="#1a1a1a", fg="#FFD700", font=('Segoe UI', 11, 'bold'),
                pady=10).pack(fill=tk.X)
        
        self.preview_text = tk.Text(right_frame, bg="#000000", fg="#FFFFFF",
                                   relief="flat", borderwidth=0,
                                   font=('Consolas', 9), wrap=tk.WORD,
                                   insertbackground="#FFD700")
        self.preview_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Status bar
        self.status_var = tk.StringVar(value="Listo")
        status = tk.Label(self, textvariable=self.status_var, bg="#1a1a1a", fg="#FFD700",
                         anchor=tk.W, font=('Segoe UI', 9), pady=5, padx=15)
        status.pack(side=tk.BOTTOM, fill=tk.X)

    def _create_bindings(self):
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-1>", self._on_open)
        self.tree.bind("<Button-3>", self._on_right_click)
        # Keybindings: backspace or Alt+Up to go up to parent folder
        self.bind('<BackSpace>', lambda e: self._go_up())
        self.bind('<Alt-Up>', lambda e: self._go_up())
        # Create new file shortcut
        self.bind('<Control-n>', lambda e: self._new_file())
        # Enter to open
        self.bind('<Return>', lambda e: self._on_open(event=None))

    def _create_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0, bg="#1a1a1a", fg="#FFFFFF",
                                   activebackground="#FFD700", activeforeground="#000000",
                                   font=('Segoe UI', 9))
        self.context_menu.add_command(label="Abrir", command=lambda: self._on_open())
        self.context_menu.add_command(label="Abrir carpeta contenedora", command=self._open_containing_folder)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Renombrar", command=self._rename_selected)
        self.context_menu.add_command(label="Eliminar", command=self._delete_selected)
        self.context_menu.add_command(label="Copiar", command=self._copy_selected)
        self.context_menu.add_command(label="Mover a...", command=self._move_selected)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Propiedades", command=self._file_properties)
        self.context_menu.add_command(label="Nuevo archivo", command=self._new_file)
        self.context_menu.add_command(label="Buscar duplicados a partir de carpeta", command=self._find_duplicates)

    def _choose_directory(self):
        path = filedialog.askdirectory(initialdir=os.path.expanduser("~"), title="Selecciona carpeta")
        if path:
            self.current_dir = path
            self._refresh()

    def _refresh(self):
        if not self.current_dir:
            self.status_var.set("Ninguna carpeta seleccionada.")
            return
        self._populate_tree(self.current_dir)

    def _populate_tree(self, folder):
        # Limpiar
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            entries = os.listdir(folder)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo listar carpeta: {e}")
            return
        # Aplica filtro de extension y búsqueda
        ext_filter = [e.strip().lower() for e in (self.ext_filter_var.get() or "").split(",") if e.strip()]
        search = (self.search_var.get() or "").lower()
        show_hidden = bool(self.show_hidden_var.get())

        # Primera fila: acceso a carpeta padre (como '...')
        parent = os.path.dirname(folder)
        if parent and parent != folder:
            try:
                # Only insert the parent row if it isn't already a child
                self.tree.insert("", 0, iid=parent, tags=('parent',), values=("...", "Carpeta", "", ""))
            except Exception:
                pass

        for name in sorted(entries, key=str.lower):
            full = os.path.join(folder, name)
            if not show_hidden and name.startswith('.') and not os.path.isdir(full):
                continue
            if ext_filter and not os.path.isdir(full):
                nodot = name.lower()
                if not any(nodot.endswith(ext if ext.startswith('.') else '.' + ext) for ext in ext_filter):
                    continue
            if search and search not in name.lower():
                continue
            try:
                stats = os.stat(full)
                size = stats.st_size
                mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stats.st_mtime))
                ftype = "Carpeta" if os.path.isdir(full) else "Archivo"
                self.tree.insert("", tk.END, iid=full, values=(name, ftype, self._human_size(size), mtime))
            except FileNotFoundError:
                continue
        self.status_var.set(f"Mostrando {len(self.tree.get_children())} elementos en {folder}")

    def _on_select(self, event=None):
        items = self.tree.selection()
        if items:
            # Preview del primer seleccionado
            self._preview_file(items[0])

    def _on_open(self, event=None):
        # Prefer the row under the mouse event (for double-clicks), fall back to selection
        iid = None
        if event is not None:
            try:
                iid = self.tree.identify_row(event.y)
            except Exception:
                iid = None
        if not iid:
            items = self.tree.selection()
            if not items:
                return
            iid = items[0]

        if not iid:
            return
        full = iid
        if os.path.isdir(full):
            self.current_dir = full
            self._refresh()
        else:
            self._open_file_with_default_app(full)

    def _go_up(self):
        if not self.current_dir:
            return
        parent = os.path.dirname(self.current_dir)
        if not parent or parent == self.current_dir:
            # Already at top
            self.status_var.set("No hay carpeta superior.")
            return
        self.current_dir = parent
        self._refresh()

    def _preview_file(self, filepath):
        if os.path.isdir(filepath):
            text = f"...: {filepath}\n"
            try:
                n = len(os.listdir(filepath))
                text += f"Contiene {n} elementos.\n"
            except Exception as e:
                text += f"Error al listar: {e}\n"
        else:
            text = f"Archivo: {filepath}\n"
            try:
                with open(filepath, "rb") as f:
                    data = f.read(4096)  # mostrar primeros bytes
                # intentar decodificar como utf-8
                try:
                    text += data.decode("utf-8", errors="replace")
                except Exception:
                    text += f"(Contenido binario, {len(data)} bytes mostrados)\n"
            except Exception as e:
                text += f"Error leyendo archivo: {e}\n"

        self._log_preview(text)

    def _log_preview(self, text):
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert(tk.END, text)
        self.preview_text.configure(state="disabled")

    def _open_file_with_default_app(self, filepath):
        try:
            os.startfile(filepath)  # Windows
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")

    def _get_selected_paths(self):
        return list(self.tree.selection())

    def _on_right_click(self, event):
        iid = self.tree.identify_row(event.y)
        if iid:
            # select row on right click
            if iid not in self.tree.selection():
                self.tree.selection_set(iid)
            self.context_menu.tk_popup(event.x_root, event.y_root)
        else:
            # click on empty area
            pass

    def _rename_selected(self):
        sel = self._get_selected_paths()
        if not sel:
            messagebox.showinfo("Renombrar", "Selecciona un archivo para renombrar.")
            return
        if len(sel) > 1:
            messagebox.showinfo("Renombrar", "Selecciona solo un archivo para renombrar.")
            return
        src = sel[0]
        basename = os.path.basename(src)
        new_name = simpledialog.askstring("Renombrar", "Nuevo nombre:", initialvalue=basename)
        if not new_name:
            return
        dst = os.path.join(os.path.dirname(src), new_name)
        try:
            os.rename(src, dst)
            self._refresh()
            self.status_var.set(f"Renombrado: {basename} -> {new_name}")
        except Exception as e:
            messagebox.showerror("Error al renombrar", str(e))

    def _delete_selected(self):
        sel = self._get_selected_paths()
        if not sel:
            messagebox.showinfo("Eliminar", "Selecciona al menos un archivo o carpeta.")
            return
        if not messagebox.askyesno("Eliminar", f"¿Eliminar {len(sel)} elemento(s)?"):
            return
        errors = []
        for p in sel:
            try:
                if os.path.isdir(p):
                    shutil.rmtree(p)
                else:
                    os.remove(p)
            except Exception as e:
                errors.append((p, str(e)))
        self._refresh()
        if errors:
            messagebox.showwarning("Errores", "\n".join(f"{p}: {e}" for p, e in errors))
        else:
            self.status_var.set("Eliminación completada.")

    def _copy_selected(self):
        sel = self._get_selected_paths()
        if not sel:
            messagebox.showinfo("Copiar", "Selecciona al menos un archivo para copiar.")
            return
        dest = filedialog.askdirectory(title="Carpeta destino")
        if not dest:
            return
        errors = []
        for p in sel:
            try:
                if os.path.isdir(p):
                    base = os.path.basename(p)
                    shutil.copytree(p, os.path.join(dest, base))
                else:
                    shutil.copy2(p, dest)
            except Exception as e:
                errors.append((p, str(e)))
        self._refresh()
        if errors:
            messagebox.showwarning("Errores", "\n".join(f"{p}: {e}" for p, e in errors))
        else:
            self.status_var.set("Copia completada.")

    def _search(self):
        # Force refresh to apply filter
        if not self.current_dir:
            messagebox.showinfo("Buscar", "Selecciona una carpeta primero.")
            return
        self._refresh()

    def _clear_search(self):
        self.search_var.set("")
        self.ext_filter_var.set("")
        self._refresh()

    def _file_properties(self):
        sel = self._get_selected_paths()
        if not sel:
            messagebox.showinfo("Propiedades", "Selecciona un archivo o carpeta.")
            return
        p = sel[0]
        try:
            stats = os.stat(p)
            size = stats.st_size
            mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stats.st_mtime))
            mode = stats.st_mode
            perm = stat.filemode(mode)
            ftype = '...' if os.path.isdir(p) else 'Archivo'
            text = f"{ftype}: {p}\n\nTamaño: {self._human_size(size)}\nModificado: {mtime}\nPermisos: {perm}\n"
            if platform.system() == 'Windows':
                try:
                    # no getpw* on windows, but we can show attributes
                    attrs = []
                    if os.path.isdir(p):
                        attrs.append('Directorio')
                    if not os.access(p, os.W_OK):
                        attrs.append('Solo lectura')
                    text += '\n'.join([a for a in attrs])
                except Exception:
                    pass
            messagebox.showinfo("Propiedades", text)
        except Exception as e:
            messagebox.showerror("Propiedades", str(e))

    def _open_containing_folder(self):
        sel = self._get_selected_paths()
        if not sel:
            messagebox.showinfo("Abrir carpeta", "Selecciona un archivo o carpeta.")
            return
        p = sel[0]
        folder = p if os.path.isdir(p) else os.path.dirname(p)
        try:
            if platform.system() == 'Windows':
                os.startfile(folder)
            elif platform.system() == 'Darwin':
                os.system(f'open "{folder}"')
            else:
                os.system(f'xdg-open "{folder}"')
        except Exception as e:
            messagebox.showerror("Abrir carpeta", str(e))

    def _new_folder(self):
        if not self.current_dir:
            messagebox.showinfo("Nueva carpeta", "Selecciona una carpeta primero.")
            return
        name = simpledialog.askstring("Crear carpeta", "Nombre de la nueva carpeta:")
        if not name:
            return
        newp = os.path.join(self.current_dir, name)
        try:
            os.mkdir(newp)
            self._refresh()
            self.status_var.set(f"Carpeta creada: {newp}")
        except Exception as e:
            messagebox.showerror("Crear carpeta", str(e))

    def _new_file(self):
        if not self.current_dir:
            messagebox.showinfo("Nuevo archivo", "Selecciona una carpeta primero.")
            return
        name = simpledialog.askstring("Crear archivo", "Nombre del archivo:", initialvalue="nuevo.txt")
        if not name:
            return
        name = os.path.basename(name)
        newp = os.path.join(self.current_dir, name)
        if os.path.exists(newp):
            if not messagebox.askyesno("Crear archivo", f'El archivo {name} existe. ¿Sobrescribir?'):
                return
        try:
            with open(newp, 'w', encoding='utf-8') as f:
                # create empty file
                pass
            self._refresh()
            self.status_var.set(f"Archivo creado: {newp}")
        except Exception as e:
            messagebox.showerror("Crear archivo", str(e))

    def _move_selected(self):
        sel = self._get_selected_paths()
        if not sel:
            messagebox.showinfo("Mover", "Selecciona al menos un archivo o carpeta.")
            return
        dest = filedialog.askdirectory(title="Carpeta destino")
        if not dest:
            return
        errors = []
        for p in sel:
            try:
                shutil.move(p, dest)
            except Exception as e:
                errors.append((p, str(e)))
        self._refresh()
        if errors:
            messagebox.showwarning("Errores", "\n".join(f"{p}: {e}" for p, e in errors))
        else:
            self.status_var.set("Movimiento completado.")

    def _batch_rename_selected(self):
        sel = self._get_selected_paths()
        if not sel:
            messagebox.showinfo("Renombrado por lotes", "Selecciona al menos un archivo.")
            return
        # Simple pattern renaming: find/replace or pattern with {n}
        mode = simpledialog.askstring("Renombrado por lotes", "Modo (replace|pattern):", initialvalue="replace")
        if not mode:
            return
        if mode.lower() == 'replace':
            find = simpledialog.askstring("Renombrado por lotes", "Texto a buscar:")
            replace = simpledialog.askstring("Renombrado por lotes", "Texto de reemplazo:")
            if find is None or replace is None:
                return
            errors = []
            for p in sel:
                base = os.path.basename(p)
                newbase = base.replace(find, replace)
                dst = os.path.join(os.path.dirname(p), newbase)
                try:
                    os.rename(p, dst)
                except Exception as e:
                    errors.append((p, str(e)))
            self._refresh()
            if errors:
                messagebox.showwarning("Errores", "\n".join(f"{p}: {e}" for p, e in errors))
            else:
                self.status_var.set("Renombrado por lotes completado.")
        else:
            # pattern mode: prefix_{n}{ext}
            pattern = simpledialog.askstring("Renombrado por lotes", "Patrón (use {n} para el contador, {name} para nombre base):", initialvalue="file_{n}")
            if not pattern:
                return
            errors = []
            counter = 1
            for p in sel:
                base = os.path.basename(p)
                name, ext = os.path.splitext(base)
                newbase = pattern.replace('{n}', str(counter)).replace('{name}', name) + ext
                dst = os.path.join(os.path.dirname(p), newbase)
                try:
                    os.rename(p, dst)
                except Exception as e:
                    errors.append((p, str(e)))
                counter += 1
            self._refresh()
            if errors:
                messagebox.showwarning("Errores", "\n".join(f"{p}: {e}" for p, e in errors))
            else:
                self.status_var.set("Renombrado por lotes completado.")

    def _find_duplicates(self, path=None):
        # Find duplicate files in current_dir or given path
        folder = path or self.current_dir
        if not folder:
            messagebox.showinfo("Duplicados", "Selecciona una carpeta primero.")
            return
        self.status_var.set("Buscando duplicados...")
        # Walk folder and collect files by size
        files_by_size = {}
        for root, dirs, files in os.walk(folder):
            for name in files:
                full = os.path.join(root, name)
                try:
                    size = os.path.getsize(full)
                except Exception:
                    continue
                files_by_size.setdefault(size, []).append(full)

        duplicates = []
        # For sizes with more than one file, compute hashes
        for size, files in files_by_size.items():
            if len(files) < 2:
                continue
            hash_map = {}
            for f in files:
                try:
                    h = self._file_checksums(f)[1]  # use sha1
                    hash_map.setdefault(h, []).append(f)
                except Exception:
                    continue
            for h, group in hash_map.items():
                if len(group) > 1:
                    duplicates.append((h, group))

        # Display results
        if not duplicates:
            self._log_preview("No se encontraron duplicados.")
            self.status_var.set("Búsqueda de duplicados completada: 0 encontrados.")
            return
        out = []
        for h, group in duplicates:
            out.append(f"HASH {h} ({len(group)} archivos):")
            for f in group:
                out.append(f"  {f}")
            out.append("")
        self._log_preview('\n'.join(out))
        self.status_var.set(f"Búsqueda de duplicados completada: {sum(len(g) for _, g in duplicates)} archivos duplicados.")

    def _file_checksums(self, filepath):
        h_md5 = hashlib.md5()
        h_sha1 = hashlib.sha1()
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                h_md5.update(chunk)
                h_sha1.update(chunk)
        return h_md5.hexdigest(), h_sha1.hexdigest()

    def _human_size(self, n):
        # tamaño legible
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if n < 1024.0:
                return f"{n:3.1f} {unit}"
            n /= 1024.0
        return f"{n:.1f} PB"

    def _about(self):
        messagebox.showinfo("Acerca de GPyFiles", "GPyFiles GUI\nInterfaz básica con Tkinter\nHecha para integración con GPyFiles.")

def main():
    app = GPyFilesGUI()
    app.mainloop()

if __name__ == "__main__":
    main()