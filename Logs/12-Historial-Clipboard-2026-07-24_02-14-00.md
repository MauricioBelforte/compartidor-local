# Log de Cambios - Historial de Clipboard

**Fecha:** 2026-07-24 02:14:00
**Componente:** 05 - Historial de Clipboard
**Archivo modificado:** notas_compartidas.py

## Resumen
Se implementó el monitoreo automático del clipboard del sistema con una nueva pestaña que muestra el historial de copias sincronizado entre PCs.

## Cambios realizados

### 1. Importación de módulo time
- **Código original:**
```python
import json
import os
import socket
import struct
import threading
import tkinter as tk
```
- **Código nuevo:**
```python
import json
import os
import socket
import struct
import threading
import time
import tkinter as tk
```
- **Descripción:** Se agregó el módulo `time` para implementar el polling del clipboard.

### 2. Configuración de puertos
- **Código original:**
```python
MI_PUERTO_MENSAJES = 50508
PUERTO_MENSAJES_OTRA = 50508
CARPETA_DESCARGAS = "descargas"
CHUNK_SIZE = 4096
```
- **Código nuevo:**
```python
MI_PUERTO_MENSAJES = 50508
PUERTO_MENSAJES_OTRA = 50508
MI_PUERTO_CLIPBOARD = 50509
PUERTO_CLIPBOARD_OTRA = 50509
CARPETA_DESCARGAS = "descargas"
CHUNK_SIZE = 4096
CLIPBOARD_POLLING_INTERVAL = 500
```
- **Descripción:** Se agregaron constantes para el nuevo puerto UDP 50509 y el intervalo de polling (500ms).

### 3. Variables globales
- **Código original:**
```python
IP_OTRA_PC = ""
```
- **Código nuevo:**
```python
IP_OTRA_PC = ""
clipboard_anterior = ""
clipboard_habilitado = True
```
- **Descripción:** Se agregaron variables globales para rastrear el estado del clipboard.

### 4. Socket UDP para clipboard
- **Código nuevo:**
```python
# ============================================================
# MODULO CLIPBOARD
# ============================================================

sock_clipboard = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_clipboard.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_clipboard.bind(("0.0.0.0", MI_PUERTO_CLIPBOARD))
```
- **Descripción:** Se creó un nuevo socket UDP para el módulo de clipboard.

### 5. Funciones de lógica para clipboard
- **Código nuevo:** Se agregaron las siguientes funciones:
  - `monitorear_clipboard()`: Verifica el clipboard cada 500ms y detecta cambios
  - `escuchar_clipboard()`: Escucha mensajes de clipboard remotos en hilo daemon
  - `enviar_clipboard_remoto(timestamp, contenido)`: Envía cambios de clipboard a la otra PC
  - `agregar_clipboard_historial(timestamp, contenido, origen)`: Agrega entrada al historial

### 6. Pestaña "Clipboard"
- **Código nuevo:** Se agregó la pestaña completa con:
  - ScrolledText para mostrar historial de copias
  - Formato: `[HH:MM:SS] [LOCAL/REMOTO] contenido`
  - Más nuevo arriba

### 7. Inicialización de hilos
- **Código nuevo:**
```python
hilo_clipboard_monitor = threading.Thread(target=monitorear_clipboard, daemon=True)
hilo_clipboard_monitor.start()

hilo_clipboard_escucha = threading.Thread(target=escuchar_clipboard, daemon=True)
hilo_clipboard_escucha.start()
```
- **Descripción:** Se iniciaron los hilos de monitoreo y escucha para clipboard.

### 8. Cierre de sockets
- **Código original:**
```python
sock_texto.close()
sock_mensajes.close()
sock_servidor.close()
sock_discover.close()
```
- **Código nuevo:**
```python
sock_texto.close()
sock_mensajes.close()
sock_clipboard.close()
sock_servidor.close()
sock_discover.close()
```
- **Descripción:** Se agregó el cierre del socket de clipboard.

## Documentación actualizada
- DOCUMENTACION/README.md: Se agregó componente 05
- DOCUMENTACION/1-DOCUMENTO-DE-ESPECIFICACIONES-ACTUAL.md: Se actualizaron requisitos funcionales
- DOCUMENTACION/2-DOCUMENTO-DISENO-ACTUAL.md: Se actualizó arquitectura general y diagrama
- DOCUMENTACION/3-DOCUMENTO-TAREAS-ACTUAL.md: Se agregaron tareas completadas del componente 05
- DOCUMENTACION/05-Historial-Clipboard/: Se creó documentación completa del componente

## Verificación
- La aplicación inicia sin errores
- La pestaña "Clipboard" se muestra correctamente
- El monitoreo de clipboard se inicia automáticamente

## Consideraciones de privacidad
- El clipboard puede contener información sensible (contraseñas, datos personales)
- El historial de clipboard se sincroniza automáticamente con la otra PC
- El usuario debe ser consciente de esta sincronización
