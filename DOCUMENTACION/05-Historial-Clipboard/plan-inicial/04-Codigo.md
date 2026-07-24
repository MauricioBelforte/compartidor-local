# Código - Historial de Clipboard

## Archivos involucrados
- `notas_compartidas.py` - Archivo principal a modificar
- `DOCUMENTACION/README.md` - Actualizar número de componente
- `DOCUMENTACION/05-Historial-Clipboard/plan-actual/*` - Actualizar después de implementar

## Funciones clave a agregar/modificar

### Nuevas constantes
```python
MI_PUERTO_CLIPBOARD = 50509
PUERTO_CLIPBOARD_OTRA = 50509
CLIPBOARD_POLLING_INTERVAL = 500  # ms
```

### Nuevo socket UDP para clipboard
```python
sock_clipboard = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_clipboard.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_clipboard.bind(("0.0.0.0", MI_PUERTO_CLIPBOARD))
```

### Variables globales
```python
clipboard_anterior = ""
clipboard_habilitado = True
```

### Pestaña "Clipboard"
```python
frame_clipboard = ttk.Frame(notebook)
notebook.add(frame_clipboard, text="  Clipboard  ")

caja_clipboard = scrolledtext.ScrolledText(frame_clipboard, wrap=tk.WORD, font=("Consolas", 11))
caja_clipboard.pack(expand=True, fill="both", padx=8, pady=8)
```

### Funciones de lógica
```python
def monitorear_clipboard():
    global clipboard_anterior
    while clipboard_habilitado:
        try:
            contenido_actual = ventana.clipboard_get()
            if contenido_actual and contenido_actual != clipboard_anterior:
                timestamp = datetime.now().strftime("%H:%M:%S")
                agregar_clipboard_historial(timestamp, contenido_actual, "local")
                enviar_clipboard_remoto(timestamp, contenido_actual)
                clipboard_anterior = contenido_actual
        except tk.TclError:
            pass
        time.sleep(CLIPBOARD_POLLING_INTERVAL / 1000)

def escuchar_clipboard():
    while True:
        try:
            datos, _ = sock_clipboard.recvfrom(65535)
        except OSError:
            break
        mensaje = datos.decode("utf-8", errors="replace")
        partes = mensaje.split("|||", 1)
        if len(partes) == 2:
            timestamp, contenido = partes
            ventana.after(0, agregar_clipboard_historial, timestamp, contenido, "remoto")

def enviar_clipboard_remoto(timestamp, contenido):
    if not IP_OTRA_PC:
        return
    mensaje = f"{timestamp}|||{contenido}"
    try:
        sock_clipboard.sendto(mensaje.encode("utf-8"), (IP_OTRA_PC, PUERTO_CLIPBOARD_OTRA))
    except OSError as e:
        print("Error al enviar clipboard:", e)

def agregar_clipboard_historial(timestamp, contenido, origen):
    etiqueta = "[LOCAL]" if origen == "local" else "[REMOTO]"
    linea = f"[{timestamp}] {etiqueta} {contenido}\n"
    caja_clipboard.insert("1.0", linea)
```

### Inicialización de hilos
```python
hilo_clipboard_monitor = threading.Thread(target=monitorear_clipboard, daemon=True)
hilo_clipboard_monitor.start()

hilo_clipboard_escucha = threading.Thread(target=escuchar_clipboard, daemon=True)
hilo_clipboard_escucha.start()
```

### Cierre de sockets
```python
sock_clipboard.close()
```

## Logs relacionados
- Logs/ULTIMO_NUMERO.txt - Para generar el nuevo log
- Logs/NN-HISTORIAL-CLIPBOARD-AAAA-MM-DD_HH-MM-SS.md - Log de cambios
