# Código — Notas compartidas LAN

Documentación del proyecto **Notas compartidas LAN**: comunicación instantánea de texto entre 2 PCs de la misma red local.

## Archivos involucrados
| Archivo | Rol |
|---|---|
| `notas_compartidas.py` | Archivo principal unificado. Contiene 2 pestañas: "Texto en vivo" (UDP) y "Archivos" (TCP). |
| `archivos_compartidos.py` | Standalone del componente de archivos (TCP, mismo código que la pestaña Archivos). |

## Configuración (constantes) — Archivo unificado
| Constante | Descripción |
|---|---|
| `IP_OTRA_PC` | IP local de la otra PC — el único valor que cambia entre PC A y PC B |
| `MI_PUERTO_TEXTO` | Puerto UDP donde esta PC escucha texto (50505) |
| `PUERTO_TEXTO_OTRA` | Puerto UDP de destino para texto en la otra PC (50505) |
| `MI_PUERTO_ARCHIVOS` | Puerto TCP donde esta PC escucha archivos (50506) |
| `PUERTO_ARCHIVOS_OTRA` | Puerto TCP de destino para archivos en la otra PC (50506) |
| `CARPETA_DESCARGAS` | Carpeta donde se guardan archivos recibidos ("descargas") |
| `CHUNK_SIZE` | Tamaño de chunk para transferencia de archivos (4096 bytes) |

## Funciones clave — Pestaña Texto en vivo
| Función | Qué hace |
|---|---|
| `enviar_texto(event=None)` | Lee el contenido de la caja y lo manda por UDP. Atada a `<KeyRelease>`. |
| `escuchar_texto()` | Loop bloqueante en hilo daemon; espera datagramas UDP entrantes. |
| `actualizar_caja(texto)` | Reemplaza el contenido de la caja con texto recibido (thread-safe via `ventana.after`). |

## Funciones clave — Pestaña Archivos
| Función | Qué hace |
|---|---|
| `seleccionar_archivo()` | Abre `filedialog.askopenfilename()` para elegir archivo a enviar. |
| `ejecutar_envio()` | Dispara el envío del archivo seleccionado. |
| `iniciar_envio(ruta)` | Conecta TCP a la otra PC, envía metadatos + contenido en chunks. |
| `enviar_metadatos(sock, nombre, tamaño)` | Envía 4 bytes longitud nombre + nombre UTF-8 + 8 bytes tamaño. |
| `enviar_archivo(sock, ruta, tamaño)` | Lee archivo en chunks de 4096 bytes y envía por socket. |
| `recibir_metadatos(sock)` | Lee 4 bytes longitud + nombre + 8 bytes tamaño del socket. |
| `recibir_archivo(sock, ruta, tamaño)` | Recibe chunks y escribe al archivo hasta completar tamaño. |
| `manejar_cliente(conn, addr)` | Hilo por conexión: recibe metadatos + archivo, guarda en descargas/. |
| `aceptar_conexiones()` | Loop en hilo daemon que acepta conexiones TCP entrantes. |
| `generar_nombre_unico(nombre, carpeta)` | Agrega timestamp si el archivo ya existe. |

## Objetos globales
- `sock_texto` — socket UDP (50505) para texto en vivo.
- `sock_servidor` — socket TCP servidor (50506) para recibir archivos.
- `ventana` — ventana principal de tkinter con `ttk.Notebook`.
- `notebook` — widget de pestañas con 2 tabs.
- `caja` — `ScrolledText` dentro de la pestaña Texto.
- `progreso_envio` / `progreso_recepcion` — `ttk.Progressbar` para archivos.
- `lista_historial` — `Listbox` con historial de transferencias.
- `enviando` / `recibiendo` — flags booleanos para control de concurrencia.

## Logs
Todavía no hay un sistema de logging formal. El único registro actual es un `print()` en consola si falla el envío (dentro de `enviar()`, ante una excepción `OSError`). No se registran los mensajes recibidos ni errores de recepción — si `escuchar()` encuentra un `OSError` (por ejemplo, al cerrarse el socket), el loop simplemente termina sin dejar rastro. Agregar logging más completo queda pendiente (ver `05-Checklist.md`).
