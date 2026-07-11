"""
ARCHIVOS COMPARTIDOS - Transferencia de archivos entre 2 PCs en LAN.
Version standalone. La IP de la otra PC se configura desde la interfaz.
"""

import json
import os
import socket
import struct
import threading
import tkinter as tk
from tkinter import filedialog, simpledialog, ttk
from datetime import datetime

CONFIG_FILE = "config.json"
MI_PUERTO = 50506
PUERTO_OTRA_PC = 50506
CARPETA_DESCARGAS = "descargas"
CHUNK_SIZE = 4096

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


sock_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_servidor.bind(("0.0.0.0", MI_PUERTO))
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
        ventana.after(0, mostrar_mensaje, "Configura la IP de la otra PC primero.")
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
            sock.connect((IP_OTRA_PC, PUERTO_OTRA_PC))
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


def abrir_config():
    global IP_OTRA_PC
    ip = simpledialog.askstring(
        "Configurar IP",
        "IP local de la OTRA PC (ej: 192.168.1.50):",
        parent=ventana,
        initialvalue=IP_OTRA_PC,
    )
    if ip and ip.strip():
        ip = ip.strip()
        guardar_config(ip)
        IP_OTRA_PC = ip
        lbl_estado.config(
            text=f"TCP :{MI_PUERTO}  ->  {IP_OTRA_PC}:{PUERTO_OTRA_PC}  |  Descargas: {CARPETA_DESCARGAS}/"
        )


ventana = tk.Tk()
ventana.title("Archivos compartidos")
ventana.geometry("520x480")

IP_OTRA_PC = cargar_config()
if not IP_OTRA_PC:
    ip = simpledialog.askstring(
        "Configurar IP",
        "IP local de la OTRA PC (ej: 192.168.1.50):",
        parent=ventana,
    )
    if ip and ip.strip():
        IP_OTRA_PC = ip.strip()
        guardar_config(IP_OTRA_PC)

frame_seleccion = tk.Frame(ventana)
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

frame_envio = tk.LabelFrame(ventana, text="Envio", padx=6, pady=6)
frame_envio.pack(fill="x", padx=8, pady=4)

progreso_envio = ttk.Progressbar(frame_envio, length=400, mode="determinate")
progreso_envio.pack(fill="x")

lbl_progreso_envio = tk.Label(frame_envio, text="En espera...", anchor="w")
lbl_progreso_envio.pack(fill="x")

frame_recepcion = tk.LabelFrame(ventana, text="Recepcion", padx=6, pady=6)
frame_recepcion.pack(fill="x", padx=8, pady=4)

progreso_recepcion = ttk.Progressbar(frame_recepcion, length=400, mode="determinate")
progreso_recepcion.pack(fill="x")

lbl_progreso_recepcion = tk.Label(frame_recepcion, text="En espera...", anchor="w")
lbl_progreso_recepcion.pack(fill="x")

frame_historial = tk.LabelFrame(ventana, text="Historial", padx=6, pady=6)
frame_historial.pack(fill="both", expand=True, padx=8, pady=4)

lista_historial = tk.Listbox(frame_historial, height=6, font=("Consolas", 10))
lista_historial.pack(fill="both", expand=True)

frame_barra = tk.Frame(ventana)
frame_barra.pack(fill="x", padx=8, pady=(0, 2))

btn_config = tk.Button(frame_barra, text="Configurar IP", command=abrir_config)
btn_config.pack(side=tk.RIGHT)

ip_mostrar = IP_OTRA_PC if IP_OTRA_PC else "SIN CONFIGURAR"
lbl_estado = tk.Label(
    ventana,
    text=f"TCP :{MI_PUERTO}  ->  {ip_mostrar}:{PUERTO_OTRA_PC}  |  Descargas: {CARPETA_DESCARGAS}/",
    fg="gray",
)
lbl_estado.pack(pady=(0, 6))

hilo_servidor = threading.Thread(target=aceptar_conexiones, daemon=True)
hilo_servidor.start()

ventana.mainloop()
sock_servidor.close()
