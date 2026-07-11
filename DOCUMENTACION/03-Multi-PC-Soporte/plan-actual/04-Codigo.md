# Código — Multi-PC Soporte

Documentación del componente **Multi-PC Soporte**: soporte para más de 2 PCs en la red con selección manual de destino.

## Archivos involucrados
| Archivo | Rol |
|---|---|
| `notas_compartidas.py` | App unificada existente. Se modificarán funciones de descubrimiento y se agregarán nuevas funciones de selección. |
| `config.json` | Archivo de configuración existente. Sin cambios en formato. |

## Funciones a Modificar

### `autodescubrir_continuo()`
**Ubicación:** Módulo de descubrimiento en `notas_compartidas.py`

**Cambio actual:**
```python
if encontradas:
    ventana.after(0, lambda: aplicar_ip(encontradas[0]))
```

**Cambio nuevo:**
```python
if len(encontradas) == 1:
    ventana.after(0, lambda: aplicar_ip(encontradas[0]))
elif len(encontradas) > 1:
    ventana.after(0, lambda: mostrar_dialogo_seleccion(encontradas))
```

**Descripción:** Verificar cantidad de PCs encontradas. Si hay más de una, mostrar diálogo de selección en lugar de usar automáticamente la primera.

## Funciones a Agregar

### `mostrar_dialogo_seleccion(ips)`
**Descripción:** Crea y muestra un diálogo con lista de PCs disponibles para selección.

**Parámetros:**
- `ips` (list): Lista de direcciones IP encontradas

**Comportamiento:**
- Crea ventana `Toplevel` con título "Seleccionar PC destino"
- Muestra lista de IPs con nombres de host si es posible
- Permite al usuario seleccionar una IP
- Al seleccionar, llama a `aplicar_ip()` con la IP elegida
- Cierra el diálogo

**Código de ejemplo:**
```python
def mostrar_dialogo_seleccion(ips):
    """Muestra diálogo para seleccionar PC destino cuando hay múltiples."""
    dialogo = tk.Toplevel(ventana)
    dialogo.title("Seleccionar PC destino")
    dialogo.geometry("300x250")
    dialogo.transient(ventana)  # Hacerlo modal
    dialogo.grab_set()  # Capturar foco
    
    lbl = tk.Label(dialogo, text="Seleccione la PC destino:")
    lbl.pack(pady=10)
    
    lista = tk.Listbox(dialogo)
    lista.pack(fill="both", expand=True, padx=10, pady=5)
    
    for ip in ips:
        try:
            nombre = socket.gethostbyaddr(ip)[0]
            lista.insert(tk.END, f"{ip} ({nombre})")
        except:
            lista.insert(tk.END, ip)
    
    def seleccionar():
        seleccion = lista.curselection()
        if seleccion:
            ip_seleccionada = ips[seleccion[0]]
            aplicar_ip(ip_seleccionada)
            dialogo.destroy()
    
    btn = tk.Button(dialogo, text="Seleccionar", command=seleccionar)
    btn.pack(pady=10)
    
    # Centrar diálogo
    dialogo.update_idletasks()
    x = ventana.winfo_x() + (ventana.winfo_width() - dialogo.winfo_width()) // 2
    y = ventana.winfo_y() + (ventana.winfo_height() - dialogo.winfo_height()) // 2
    dialogo.geometry(f"+{x}+{y}")
```

### `cambiar_destino()`
**Descripción:** Permite cambiar el destino en cualquier momento mediante botón en la interfaz.

**Comportamiento:**
- Ejecuta `buscar_pc()` con timeout de 4s
- Si no hay PCs, muestra mensaje de error
- Si hay 1 PC, la selecciona automáticamente
- Si hay múltiples PCs, muestra diálogo de selección
- Actualiza etiquetas de estado después de cambiar

**Código de ejemplo:**
```python
def cambiar_destino():
    """Permite cambiar el destino en cualquier momento."""
    lbl_buscar.config(text="Buscando PCs...")
    btn_cambiar.config(state=tk.DISABLED)
    
    def _cambiar():
        encontradas = buscar_pc(timeout=4)
        ventana.after(0, lambda: lbl_buscar.config(text=""))
        ventana.after(0, lambda: btn_cambiar.config(state=tk.NORMAL))
        
        if not encontradas:
            ventana.after(0, lambda: mostrar_mensaje("No se encontraron PCs en la red"))
            return
        
        if len(encontradas) == 1:
            ventana.after(0, lambda: aplicar_ip(encontradas[0]))
            ventana.after(0, lambda: mostrar_mensaje(f"Conectado a {encontradas[0]}"))
        else:
            ventana.after(0, lambda: mostrar_dialogo_seleccion(encontradas))
    
    threading.Thread(target=_cambiar, daemon=True).start()
```

## Objetos Globales a Agregar

### `btn_cambiar`
**Tipo:** `tk.Button`

**Descripción:** Botón en la barra inferior para cambiar el destino.

**Ubicación:** Barra inferior, junto a "Buscar PC" y "IP manual"

**Código de creación:**
```python
btn_cambiar = tk.Button(frame_barra, text="Cambiar destino", command=cambiar_destino, padx=8)
btn_cambiar.pack(side=tk.LEFT, padx=(0, 6))
```

## Modificaciones a la Interfaz

### Barra Inferior
Agregar botón `btn_cambiar` en la barra inferior existente.

**Orden actual:**
1. `btn_buscar` - "Buscar PC"
2. `btn_config` - "IP manual"
3. `lbl_buscar` - Etiqueta de estado

**Nuevo orden:**
1. `btn_buscar` - "Buscar PC"
2. `btn_config` - "IP manual"
3. `btn_cambiar` - "Cambiar destino" (NUEVO)
4. `lbl_buscar` - Etiqueta de estado

## Consideraciones de Threading

- `cambiar_destio()` ejecuta `buscar_pc()` en un hilo separado para no bloquear la UI
- `mostrar_dialogo_seleccion()` se ejecuta en el hilo principal (vía `ventana.after`)
- El diálogo es modal (`grab_set()`) para evitar interacción con la ventana principal mientras se selecciona

## Manejo de Errores

- Si `socket.gethostbyaddr()` falla, mostrar solo IP sin nombre
- Si `buscar_pc()` retorna lista vacía, mostrar mensaje informativo
- Si usuario cierra diálogo sin seleccionar, no cambiar configuración
- Timeout de 4s para cambio manual (mayor que 2s de autodescubrimiento)

## Logs

No se requiere logging adicional. Se usará `mostrar_mensaje()` para informar al usuario de cambios de destino.

## Testing

- **Caso 1 PC:** Autodescubrimiento debe conectar automáticamente sin diálogo
- **Caso 2 PCs:** Autodescubrimiento debe conectar automáticamente sin diálogo
- **Caso 3+ PCs:** Autodescubrimiento debe mostrar diálogo de selección
- **Caso cambio manual:** Botón "Cambiar destino" debe funcionar en cualquier momento
- **Caso sin PCs:** Debe mostrar mensaje "No se encontraron PCs"
- **Caso gethostbyaddr falla:** Debe mostrar solo IP sin crash
