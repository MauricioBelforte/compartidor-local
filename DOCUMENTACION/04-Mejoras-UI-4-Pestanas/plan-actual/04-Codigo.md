# Código - Mejoras UI 4 Pestañas

## Archivos involucrados
- `notas_compartidas.py` - Archivo principal a modificar
- `DOCUMENTACION/README.md` - Actualizar número de componente
- `DOCUMENTACION/04-Mejoras-UI-4-Pestanas/plan-actual/*` - Actualizar después de implementar

## Funciones clave a agregar/modificar

### Nuevas constantes
```python
MI_PUERTO_MENSAJES = 50508
PUERTO_MENSAJES_OTRA = 50508
```

### Nuevo socket UDP para mensajes
```python
sock_mensajes = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_mensajes.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_mensajes.bind(("0.0.0.0", MI_PUERTO_MENSAJES))
```

### Indicador visual de conexión
```python
canvas_indicador = tk.Canvas(frame_barra, width=20, height=20, bg="#ececec", highlightthickness=0)
circulo_conexion = canvas_indicador.create_oval(2, 2, 18, 18, fill="#CCCCCC", outline="")

def actualizar_indicador():
    color = "#4CAF50" if IP_OTRA_PC else "#CCCCCC"
    canvas_indicador.itemconfig(circulo_conexion, fill=color)
```

### Pestaña "Enviar y recibir texto"
```python
frame_mensajes = ttk.Frame(notebook)
notebook.add(frame_mensajes, text="  Enviar y recibir texto  ")

# Frame input
frame_input = tk.Frame(frame_mensajes)
frame_input.pack(fill="both", expand=True, padx=8, pady=8)

input_mensaje = scrolledtext.ScrolledText(frame_input, height=5, wrap=tk.WORD, font=("Consolas", 11))
input_mensaje.pack(fill="both", expand=True)

btn_enviar_mensaje = tk.Button(frame_input, text="Enviar", command=enviar_mensaje_rapido)
btn_enviar_mensaje.pack(pady=4)

# Frame recepción
frame_recepcion = tk.Frame(frame_mensajes)
frame_recepcion.pack(fill="both", expand=True, padx=8, pady=8)

area_recepcion = scrolledtext.ScrolledText(frame_recepcion, height=5, wrap=tk.WORD, font=("Consolas", 11))
area_recepcion.pack(fill="both", expand=True)

btn_copiar = tk.Button(frame_recepcion, text="Copiar", command=copiar_recepcion)
btn_copiar.pack(pady=4)
```

### Pestaña "Historial"
```python
frame_historial = ttk.Frame(notebook)
notebook.add(frame_historial, text="  Historial  ")

caja_historial = scrolledtext.ScrolledText(frame_historial, wrap=tk.WORD, font=("Consolas", 11))
caja_historial.pack(expand=True, fill="both", padx=8, pady=8)
```

### Funciones de lógica
```python
def enviar_mensaje_rapido():
    if not IP_OTRA_PC:
        mostrar_mensaje("No hay conexión")
        return
    contenido = input_mensaje.get("1.0", "end-1c")
    if not contenido.strip():
        return
    timestamp = datetime.now().strftime("%H:%M:%S")
    mensaje = f"{timestamp}|||{contenido}"
    try:
        sock_mensajes.sendto(mensaje.encode("utf-8"), (IP_OTRA_PC, PUERTO_MENSAJES_OTRA))
        input_mensaje.delete("1.0", tk.END)
        agregar_historial(timestamp, contenido, "enviado")
    except OSError as e:
        print("Error al enviar:", e)

def escuchar_mensajes():
    while True:
        try:
            datos, _ = sock_mensajes.recvfrom(65535)
        except OSError:
            break
        mensaje = datos.decode("utf-8", errors="replace")
        partes = mensaje.split("|||", 1)
        if len(partes) == 2:
            timestamp, contenido = partes
            ventana.after(0, mostrar_recepcion, contenido)
            ventana.after(0, agregar_historial, timestamp, contenido, "recibido")

def mostrar_recepcion(contenido):
    area_recepcion.delete("1.0", tk.END)
    area_recepcion.insert(tk.END, contenido)

def copiar_recepcion():
    contenido = area_recepcion.get("1.0", "end-1c")
    ventana.clipboard_clear()
    ventana.clipboard_append(contenido)
    area_recepcion.delete("1.0", tk.END)

def agregar_historial(timestamp, contenido, tipo):
    etiqueta = ">>>" if tipo == "enviado" else "<<<"
    linea = f"[{timestamp}] {etiqueta} {contenido}\n"
    caja_historial.insert("1.0", linea)
```

### Remover mensajes de "[PC encontrada: IP]"
Modificar las funciones que insertan texto en la caja de texto en vivo para no mostrar estos mensajes.

## Logs relacionados
- Logs/ULTIMO_NUMERO.txt - Para generar el nuevo log
- Logs/NN-MEJORAS-UI-4-PESTANAS-AAAA-MM-DD_HH-MM-SS.md - Log de cambios
