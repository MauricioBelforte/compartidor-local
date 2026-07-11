# Documento de Ejecución — Actual

## Archivos del Proyecto
| Archivo | Descripción |
|---------|-------------|
| `notas_compartidas.py` | App unificada con 2 pestañas: Texto en vivo (UDP 50505) + Archivos (TCP 50506) |
| `archivos_compartidos.py` | Componente 02 standalone — Transferencia de archivos vía TCP (puerto 50506) |
| `AGENTS.md` | Reglas globales para la IA |
| `DOCUMENTACION/` | Sistema de documentación |

---

## App Unificada: `notas_compartidas.py` (recomendada)

Un solo script con 2 pestañas (ttk.Notebook). Ambos módulos de red arrancan al inicio.

### Configuración
```python
IP_OTRA_PC = "192.168.1.50"       # Unica IP para ambos modos

# Texto en vivo (UDP)
MI_PUERTO_TEXTO = 50505
PUERTO_TEXTO_OTRA = 50505

# Archivos (TCP)
MI_PUERTO_ARCHIVOS = 50506
PUERTO_ARCHIVOS_OTRA = 50506
CARPETA_DESCARGAS = "descargas"
CHUNK_SIZE = 4096
```

### Ejecución
```bash
python notas_compartidas.py
```

### Funciones Clave — Pestaña "Texto en vivo"
- `enviar_texto(event=None)`: Envía contenido de la caja por UDP en cada tecla
- `escuchar_texto()`: Hilo daemon que recibe datagramas UDP
- `actualizar_caja(texto)`: Reemplaza contenido con texto recibido

### Funciones Clave — Pestaña "Archivos"
- `seleccionar_archivo()`: Abre diálogo para elegir archivo a enviar
- `ejecutar_envio()`: Dispara el envío del archivo seleccionado
- `iniciar_envio(ruta)`: Envía archivo en chunks TCP con barra de progreso
- `enviar_metadatos()` / `enviar_archivo()`: Envío de metadatos + contenido
- `recibir_metadatos()` / `recibir_archivo()`: Recepción de metadatos + contenido
- `aceptar_conexiones()`: Hilo servidor TCP que acepta conexiones entrantes
- `manejar_cliente()`: Recibe archivo y lo guarda en `descargas/`
- `generar_nombre_unico()`: Agrega timestamp si el archivo ya existe

---

## Componente 02 Standalone: `archivos_compartidos.py`

### Configuración
```python
MI_PUERTO = 50506              # Puerto donde esta PC escucha
IP_OTRA_PC = "192.168.1.50"    # IP local de la otra PC (único valor que cambia)
PUERTO_OTRA_PC = 50506
CARPETA_DESCARGAS = "descargas"
CHUNK_SIZE = 4096
```

### Ejecución
```bash
python archivos_compartidos.py
```

---

## Requisitos Previos (ambos componentes)
- Python 3 instalado
- tkinter (viene por defecto en Windows/Mac; en Linux: `sudo apt install python3-tk`)
- Firewall permitiendo puertos 50505 (UDP) y 50506 (TCP)

## Logs
Actualmente `print()` en consola para errores. Sistema de logging formal pendiente.
