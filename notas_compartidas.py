"""
NOTAS COMPARTIDAS - Texto en vivo + Archivos LAN.
Un solo script. Dos modos. Misma red local.
Detecta automaticamente la otra PC en la red.
"""

import json
import os
import socket
import struct
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, simpledialog, ttk
from datetime import datetime

# ---------- CONFIGURACION ----------
CONFIG_FILE = "config.json"
DISCOVER_PORT = 50507
MI_PUERTO_TEXTO = 50505
PUERTO_TEXTO_OTRA = 50505
MI_PUERTO_ARCHIVOS = 50506
PUERTO_ARCHIVOS_OTRA = 50506
CARPETA_DESCARGAS = "descargas"
CHUNK_SIZE = 4096
# -----------------------------------

IP_OTRA_PC = ""


def ruta_config():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), CONFIG_FILE)


def cargar_config():
    global IP_OTRA_PC
    ruta = ruta_config()
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        IP_OTRA_PC = cfg.get("ip_otra_pc", "")
    return IP_OTRA_PC


def guardar_config(ip):
    with open(ruta_config(), "w", encoding="utf-8") as f:
        json.dump({"ip_otra_pc": ip}, f, indent=2)


def obtener_ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


# ============================================================
# MODULO DESCUBRIMIENTO AUTOMATICO
# ============================================================

sock_discover = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_discover.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_discover.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock_discover.bind(("0.0.0.0", DISCOVER_PORT))
sock_discover.settimeout(0.5)

DISCOVER_MSG = b"COMPARTIDOR_DISCOVER"
RESPONSE_PREFIX = b"COMPARTIDOR_RESPONSE:"


def escuchar_discovery():
    mi_ip = obtener_ip_local()
    while True:
        try:
            data, addr = sock_discover.recvfrom(1024)
            if data == DISCOVER_MSG and addr[0] != mi_ip:
                sock_discover.sendto(
                    RESPONSE_PREFIX + mi_ip.encode(), addr
                )
        except socket.timeout:
            continue
        except OSError:
            break


def buscar_pc(timeout=2):
    encontradas = []
    mi_ip = obtener_ip_local()
    sock_discover.sendto(DISCOVER_MSG, ("255.255.255.255", DISCOVER_PORT))
    inicio = datetime.now()
    while (datetime.now() - inicio).total_seconds() < timeout:
        try:
            data, addr = sock_discover.recvfrom(1024)
            if data.startswith(RESPONSE_PREFIX) and addr[0] != mi_ip:
                ip = data[len(RESPONSE_PREFIX):].decode()
                if ip not in encontradas:
                    encontradas.append(ip)
        except socket.timeout:
            continue
        except OSError:
            break
    return encontradas


# ============================================================
# MODULO TEXTO EN VIVO
# ============================================================

sock_texto = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_texto.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_texto.bind(("0.0.0.0", MI_PUERTO_TEXTO))


# ============================================================
# MODULO ARCHIVOS
# ============================================================

sock_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_servidor.bind(("0.0.0.0", MI_PUERTO_ARCHIVOS))
sock_servidor.listen(5)

enviando = False
recibiendo = False


def generar_nombre_unico(nombre_base, carpeta):
    nombre, ext = os.path.splitext(nombre_base)
    ruta = os.path.join(carpeta, nombre_base)
    if not os.path.exists(ruta):
        return ruta
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(carpeta, f"{nombre}_{timestamp}{ext}")


def enviar_metadatos(sock, nombre, tamaño):
    nombre_bytes = nombre.encode("utf-8")
    sock.sendall(struct.pack("!I", len(nombre_bytes)))
    sock.sendall(nombre_bytes)
    sock.sendall(struct.pack("!Q", tamaño))


def enviar_archivo(sock, ruta_archivo, tamaño):
    enviados = 0
    with open(ruta_archivo, "rb") as f:
        while enviados < tamaño:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            sock.sendall(chunk)
            enviados += len(chunk)
            pct = int(enviados / tamaño * 100) if tamaño > 0 else 100
            ventana.after(0, actualizar_progreso_envio, pct, enviados, tamaño)


def iniciar_envio(ruta_archivo):
    global enviando
    if not IP_OTRA_PC:
        ventana.after(0, mostrar_mensaje, "No se encontro ninguna PC en la red.")
        return
    if enviando:
        ventana.after(0, mostrar_mensaje, "Ya hay un envio en curso.")
        return
    if not os.path.isfile(ruta_archivo):
        ventana.after(0, mostrar_mensaje, "El archivo no existe.")
        return

    nombre = os.path.basename(ruta_archivo)
    tamaño = os.path.getsize(ruta_archivo)

    def _envio():
        global enviando
        enviando = True
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((IP_OTRA_PC, PUERTO_ARCHIVOS_OTRA))
            enviar_metadatos(sock, nombre, tamaño)
            enviar_archivo(sock, ruta_archivo, tamaño)
            sock.close()
            ventana.after(0, mostrar_mensaje, f"Envio completado: {nombre}")
        except Exception as e:
            ventana.after(0, mostrar_mensaje, f"Error al enviar: {e}")
        finally:
            enviando = False

    threading.Thread(target=_envio, daemon=True).start()


def recibir_metadatos(sock):
    raw_len = sock.recv(4)
    if not raw_len or len(raw_len) < 4:
        raise ConnectionError("Conexion cerrada al recibir metadatos")
    len_nombre = struct.unpack("!I", raw_len)[0]
    nombre_bytes = b""
    while len(nombre_bytes) < len_nombre:
        chunk = sock.recv(len_nombre - len(nombre_bytes))
        if not chunk:
            raise ConnectionError("Conexion cerrada al recibir nombre")
        nombre_bytes += chunk
    nombre = nombre_bytes.decode("utf-8")
    raw_size = sock.recv(8)
    if not raw_size or len(raw_size) < 8:
        raise ConnectionError("Conexion cerrada al recibir tamaño")
    tamaño = struct.unpack("!Q", raw_size)[0]
    return nombre, tamaño


def recibir_archivo(sock, ruta_salida, tamaño):
    recibidos = 0
    with open(ruta_salida, "wb") as f:
        while recibidos < tamaño:
            resto = tamaño - recibidos
            chunk_size = min(CHUNK_SIZE, resto)
            chunk = sock.recv(chunk_size)
            if not chunk:
                break
            f.write(chunk)
            recibidos += len(chunk)
            pct = int(recibidos / tamaño * 100) if tamaño > 0 else 100
            ventana.after(0, actualizar_progreso_recepcion, pct, recibidos, tamaño)


def manejar_cliente(conn, addr):
    global recibiendo
    if recibiendo:
        conn.close()
        return
    recibiendo = True
    try:
        nombre, tamaño = recibir_metadatos(conn)
        os.makedirs(CARPETA_DESCARGAS, exist_ok=True)
        ruta_salida = generar_nombre_unico(nombre, CARPETA_DESCARGAS)
        ventana.after(0, mostrar_mensaje, f"Recibiendo: {nombre} ({tamaño} bytes)")
        recibir_archivo(conn, ruta_salida, tamaño)
        ventana.after(0, mostrar_mensaje, f"Archivo guardado: {os.path.basename(ruta_salida)}")
    except Exception as e:
        ventana.after(0, mostrar_mensaje, f"Error al recibir: {e}")
    finally:
        recibiendo = False
        conn.close()


def aceptar_conexiones():
    while True:
        try:
            conn, addr = sock_servidor.accept()
            hilo = threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True)
            hilo.start()
        except OSError:
            break


def seleccionar_archivo():
    ruta = filedialog.askopenfilename(title="Seleccionar archivo para enviar")
    if ruta:
        lbl_archivo.config(text=os.path.basename(ruta))
        btn_enviar.config(state=tk.NORMAL)
        ventana._ruta_envio = ruta


def ejecutar_envio():
    ruta = getattr(ventana, "_ruta_envio", None)
    if ruta:
        iniciar_envio(ruta)


def actualizar_etiquetas_estado():
    ip_mostrar = IP_OTRA_PC if IP_OTRA_PC else "SIN CONFIGURAR"
    lbl_estado_texto.config(
        text=f"UDP :{MI_PUERTO_TEXTO}  ->  {ip_mostrar}:{PUERTO_TEXTO_OTRA}"
    )
    lbl_estado_archivos.config(
        text=f"TCP :{MI_PUERTO_ARCHIVOS}  ->  {ip_mostrar}:{PUERTO_ARCHIVOS_OTRA}  |  Descargas: {CARPETA_DESCARGAS}/"
    )


def aplicar_ip(ip):
    global IP_OTRA_PC
    if ip and ip != IP_OTRA_PC:
        IP_OTRA_PC = ip
        guardar_config(ip)
        actualizar_etiquetas_estado()


def autodescubrir():
    encontradas = buscar_pc()
    if encontradas:
        aplicar_ip(encontradas[0])
        ventana.after(0, lambda: caja.insert(
            tk.END, f"\n[PC encontrada: {encontradas[0]}]\n"
        ))


def pedir_ip():
    ip = simpledialog.askstring(
        "Configurar IP",
        "IP local de la OTRA PC (ej: 192.168.1.50):",
        parent=ventana,
        initialvalue=IP_OTRA_PC,
    )
    if ip and ip.strip():
        aplicar_ip(ip.strip())
        return IP_OTRA_PC
    return IP_OTRA_PC


def buscar_automatico():
    lbl_buscar.config(text="Buscando...")
    btn_buscar.config(state=tk.DISABLED)

    def _buscar():
        encontradas = buscar_pc(timeout=3)
        if encontradas:
            ventana.after(0, lambda: aplicar_ip(encontradas[0]))
            ventana.after(0, lambda: mostrar_mensaje(
                f"PC encontrada: {encontradas[0]}"
            ))
            ventana.after(0, lambda: lbl_buscar.config(text="Buscar PC"))
        else:
            ventana.after(0, lambda: lbl_buscar.config(
                text="No se encontro ninguna PC (reintenta)"
            ))
        ventana.after(0, lambda: btn_buscar.config(state=tk.NORMAL))

    threading.Thread(target=_buscar, daemon=True).start()


def abrir_config():
    pedir_ip()


# ============================================================
# INTERFAZ GRAFICA
# ============================================================

ventana = tk.Tk()
ventana.title("Compartidor Local")
ventana.geometry("540x520")
ventana.minsize(480, 400)

# --- Cargar config guardada ---
IP_OTRA_PC = cargar_config()

notebook = ttk.Notebook(ventana)

# ---------- PESTAÑA 1: TEXTO EN VIVO ----------

frame_texto = ttk.Frame(notebook)
notebook.add(frame_texto, text="  Texto en vivo  ")

caja = scrolledtext.ScrolledText(frame_texto, wrap=tk.WORD, font=("Consolas", 12))
caja.pack(expand=True, fill="both", padx=8, pady=8)

lbl_estado_texto = tk.Label(frame_texto, fg="gray")
lbl_estado_texto.pack(pady=(0, 6))


def actualizar_caja(texto):
    caja.delete("1.0", tk.END)
    caja.insert(tk.END, texto)


def escuchar_texto():
    while True:
        try:
            datos, _ = sock_texto.recvfrom(65535)
        except OSError:
            break
        texto = datos.decode("utf-8", errors="replace")
        ventana.after(0, actualizar_caja, texto)


def enviar_texto(event=None):
    if not IP_OTRA_PC:
        return
    contenido = caja.get("1.0", "end-1c")
    try:
        sock_texto.sendto(contenido.encode("utf-8"), (IP_OTRA_PC, PUERTO_TEXTO_OTRA))
    except OSError as e:
        print("No se pudo enviar:", e)


caja.bind("<KeyRelease>", enviar_texto)

hilo_texto = threading.Thread(target=escuchar_texto, daemon=True)
hilo_texto.start()

# ---------- PESTAÑA 2: ARCHIVOS ----------

frame_archivos = ttk.Frame(notebook)
notebook.add(frame_archivos, text="  Archivos  ")

frame_seleccion = tk.Frame(frame_archivos)
frame_seleccion.pack(fill="x", padx=8, pady=(8, 4))

btn_seleccionar = tk.Button(
    frame_seleccion, text="Seleccionar archivo", command=seleccionar_archivo
)
btn_seleccionar.pack(side=tk.LEFT, padx=(0, 8))

lbl_archivo = tk.Label(frame_seleccion, text="Ningun archivo seleccionado", fg="gray")
lbl_archivo.pack(side=tk.LEFT, fill="x", expand=True)

btn_enviar = tk.Button(
    frame_seleccion, text="Enviar", command=ejecutar_envio, state=tk.DISABLED
)
btn_enviar.pack(side=tk.RIGHT)

frame_envio = tk.LabelFrame(frame_archivos, text="Envio", padx=6, pady=6)
frame_envio.pack(fill="x", padx=8, pady=4)

progreso_envio = ttk.Progressbar(frame_envio, length=400, mode="determinate")
progreso_envio.pack(fill="x")

lbl_progreso_envio = tk.Label(frame_envio, text="En espera...", anchor="w")
lbl_progreso_envio.pack(fill="x")

frame_recepcion = tk.LabelFrame(frame_archivos, text="Recepcion", padx=6, pady=6)
frame_recepcion.pack(fill="x", padx=8, pady=4)

progreso_recepcion = ttk.Progressbar(frame_recepcion, length=400, mode="determinate")
progreso_recepcion.pack(fill="x")

lbl_progreso_recepcion = tk.Label(frame_recepcion, text="En espera...", anchor="w")
lbl_progreso_recepcion.pack(fill="x")

frame_historial = tk.LabelFrame(frame_archivos, text="Historial", padx=6, pady=6)
frame_historial.pack(fill="both", expand=True, padx=8, pady=4)

lista_historial = tk.Listbox(frame_historial, height=6, font=("Consolas", 10))
lista_historial.pack(fill="both", expand=True)

lbl_estado_archivos = tk.Label(frame_archivos, fg="gray")
lbl_estado_archivos.pack(pady=(0, 6))


def actualizar_progreso_envio(pct, bytes_actuales, bytes_totales):
    progreso_envio["value"] = pct
    lbl_progreso_envio.config(
        text=f"Enviando: {pct}% ({bytes_actuales}/{bytes_totales} bytes)"
    )


def actualizar_progreso_recepcion(pct, bytes_actuales, bytes_totales):
    progreso_recepcion["value"] = pct
    lbl_progreso_recepcion.config(
        text=f"Recibiendo: {pct}% ({bytes_actuales}/{bytes_totales} bytes)"
    )


def mostrar_mensaje(texto):
    lista_historial.insert(tk.END, texto)
    lista_historial.see(tk.END)


notebook.pack(expand=True, fill="both")

# ---- Barra inferior ----
frame_barra = tk.Frame(ventana)
frame_barra.pack(fill="x", padx=8, pady=(0, 6))

btn_buscar = tk.Button(frame_barra, text="Buscar PC", command=buscar_automatico)
btn_buscar.pack(side=tk.LEFT, padx=(0, 4))

btn_config = tk.Button(frame_barra, text="IP manual", command=abrir_config)
btn_config.pack(side=tk.LEFT)

lbl_buscar = tk.Label(frame_barra, text="", fg="gray")
lbl_buscar.pack(side=tk.LEFT, padx=(8, 0))

actualizar_etiquetas_estado()

# ---- Arrancar hilos ----
hilo_servidor = threading.Thread(target=aceptar_conexiones, daemon=True)
hilo_servidor.start()

hilo_discover = threading.Thread(target=escuchar_discovery, daemon=True)
hilo_discover.start()

# ---- Autodescubrimiento al inicio ----
ventana.after(500, autodescubrir)

ventana.mainloop()

sock_texto.close()
sock_servidor.close()
sock_discover.close()
