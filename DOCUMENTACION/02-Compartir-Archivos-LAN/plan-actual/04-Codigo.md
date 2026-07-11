# Código — Compartir archivos LAN

Documentación del componente **Compartir archivos LAN**: transferencia de archivos entre 2 PCs de la misma red local.

## Archivos involucrados
| Archivo | Rol |
|---|---|
| `notas_compartidas.py` | App unificada con pestañas. Contiene módulo de archivos (TCP 50506), módulo de texto (UDP 50505), y descubrimiento automático (UDP 50507). Se usa sin cambios de lógica en las dos PCs — solo cambia el valor de `IP_OTRA_PC`. |
| `config.json` | Archivo de configuración persistente donde se guarda la IP de la otra PC. |
| `descargas/` | Carpeta donde se guardan los archivos recibidos (se crea automáticamente si no existe). |

## Configuración (constantes)
| Constante | Descripción |
|---|---|
| `CONFIG_FILE` | Nombre del archivo de configuración persistente ("config.json") |
| `DISCOVER_PORT` | Puerto para descubrimiento automático vía broadcast UDP (50507) |
| `MI_PUERTO_TEXTO` | Puerto UDP para texto en vivo (50505) |
| `PUERTO_TEXTO_OTRA` | Puerto UDP de destino para texto (50505) |
| `MI_PUERTO_ARCHIVOS` | Puerto TCP donde esta PC escucha conexiones de archivos (50506) |
| `PUERTO_ARCHIVOS_OTRA` | Puerto TCP de destino para archivos (50506) |
| `IP_OTRA_PC` | IP local de la otra PC — el único valor que difiere entre PC A y PC B |
| `CARPETA_DESCARGAS` | Carpeta donde se guardan los archivos recibidos ("descargas" por defecto) |
| `CHUNK_SIZE` | Tamaño de cada chunk de transferencia (4096 bytes por defecto) |

## Funciones clave
| Función | Qué hace |
|---|---|
| `seleccionar_archivo()` | Abre diálogo de selección de archivo y obtiene ruta del archivo a enviar. |
| `iniciar_envio(ruta_archivo)` | Conecta a la otra PC, envía metadatos y contenido del archivo en chunks. Actualiza barra de progreso. |
| `enviar_metadatos(sock, nombre, tamaño)` | Envía longitud del nombre, nombre y tamaño del archivo por el socket. |
| `enviar_archivo(sock, ruta_archivo, tamaño)` | Lee archivo en chunks y envía cada chunk por el socket. |
| `aceptar_conexiones()` | Loop en hilo daemon que acepta conexiones entrantes y crea hilos para manejarlas. |
| `manejar_cliente(conn, addr)` | Recibe metadatos y archivo de una conexión, lo guarda en carpeta de descargas. Actualiza progreso. |
| `recibir_metadatos(sock)` | Lee longitud del nombre, nombre y tamaño del archivo del socket. |
| `recibir_archivo(sock, ruta_salida, tamaño)` | Recibe chunks del socket y los escribe al archivo. |
| `actualizar_progreso_envio(pct, bytes_actuales, bytes_totales)` | Actualiza barra de progreso de envío desde el hilo principal. |
| `actualizar_progreso_recepcion(pct, bytes_actuales, bytes_totales)` | Actualiza barra de progreso de recepción desde el hilo principal. |
| `generar_nombre_unico(nombre_base, carpeta)` | Genera nombre único agregando timestamp si ya existe archivo con ese nombre. |
| `ejecutar_envio()` | Dispara el envío del archivo seleccionado (wrapper para botón). |
| `mostrar_mensaje(texto)` | Agrega un mensaje al historial de la interfaz. |
| `cargar_config()` | Carga IP de la otra PC desde `config.json` al iniciar. |
| `guardar_config(ip)` | Guarda IP de la otra PC en `config.json`. |
| `obtener_ip_local()` | Obtiene la IP local de esta PC para descubrimiento. |
| `escuchar_discovery()` | Hilo daemon que responde a broadcasts de descubrimiento. |
| `buscar_pc(timeout)` | Envía broadcast y espera respuestas de otras PCs en la red. |
| `autodescubrir_continuo()` | Búsqueda automática de PC al inicio si no hay IP configurada. |
| `buscar_automatico()` | Búsqueda manual de PC vía botón en la interfaz. |
| `pedir_ip()` | Diálogo para ingresar IP manualmente. |

## Objetos globales
- `sock_servidor` — socket TCP servidor, creado una vez al iniciar; escucha en `MI_PUERTO_ARCHIVOS`.
- `sock_discover` — socket UDP para descubrimiento automático, escucha en `DISCOVER_PORT`.
- `ventana` — ventana principal de tkinter con ttk.Notebook.
- `notebook` — widget ttk.Notebook con pestañas "Texto en vivo" y "Archivos".
- `btn_seleccionar` — botón para seleccionar archivo a enviar.
- `btn_enviar` — botón para iniciar el envío del archivo seleccionado.
- `btn_buscar` — botón para buscar PC automáticamente.
- `btn_config` — botón para configurar IP manualmente.
- `lbl_archivo` — etiqueta que muestra el nombre del archivo seleccionado.
- `progreso_envio` — widget `ttk.Progressbar` para mostrar progreso de envío.
- `lbl_progreso_envio` — etiqueta que muestra porcentaje y bytes de envío.
- `progreso_recepcion` — widget `ttk.Progressbar` para mostrar progreso de recepción.
- `lbl_progreso_recepcion` — etiqueta que muestra porcentaje y bytes de recepción.
- `lista_historial` — widget `Listbox` que muestra historial de transferencias.
- `lbl_estado_texto` — etiqueta que muestra estado del módulo de texto.
- `lbl_estado_archivos` — etiqueta que muestra estado del módulo de archivos.
- `lbl_buscar` — etiqueta que muestra estado de búsqueda de PC.
- `hilo_servidor` — hilo daemon que corre `aceptar_conexiones()`.
- `hilo_discover` — hilo daemon que corre `escuchar_discovery()`.
- `enviando` — flag booleano para indicar si hay un envío en curso.
- `recibiendo` — flag booleano para indicar si hay una recepción en curso.

## Estructura de datos

### Metadatos de archivo
```python
# Estructura enviada antes del contenido:
# [4 bytes: longitud nombre (big-endian int)]
# [N bytes: nombre archivo (UTF-8)]
# [8 bytes: tamaño archivo (big-endian long)]
```

## Logs
Inicialmente sin sistema de logging formal. Se usarán `print()` en consola para errores de conexión y mensajes de estado. Agregar logging más completo queda pendiente (ver `05-Checklist.md`).

## Manejo de errores
- Excepciones de conexión (`ConnectionRefusedError`, `TimeoutError`): mostrar mensaje al usuario y cerrar socket.
- Excepciones de I/O de archivo (`FileNotFoundError`, `PermissionError`): mostrar mensaje al usuario.
- Excepciones de socket (`OSError`): cerrar conexión y mostrar mensaje.
- Validación de integridad: verificar que se recibieron exactamente `tamaño_archivo` bytes.

## Consideraciones de threading
- `aceptar_conexiones()` corre en hilo daemon separado.
- Cada `manejar_cliente()` corre en su propio hilo.
- Actualizaciones de UI se agendan con `ventana.after(0, funcion, args)` para thread-safety.
- Flags `enviando` y `recibiendo` protegen contra transferencias simultáneas no deseadas.
