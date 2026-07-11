# Código — Compartir archivos LAN

Documentación del componente **Compartir archivos LAN**: transferencia de archivos entre 2 PCs de la misma red local.

## Archivos involucrados
| Archivo | Rol |
|---|---|
| `archivos_compartidos.py` | Único archivo del componente. Contiene configuración, lógica de red e interfaz gráfica. Se usa sin cambios de lógica en las dos PCs — solo cambia el valor de `IP_OTRA_PC`. |
| `descargas/` | Carpeta donde se guardan los archivos recibidos (se crea automáticamente si no existe). |

## Configuración (constantes)
| Constante | Descripción |
|---|---|
| `MI_PUERTO` | Puerto donde esta PC escucha conexiones TCP (50506 por defecto, diferenciado del 50505 de notas compartidas) |
| `IP_OTRA_PC` | IP local de la otra PC — el único valor que difiere entre PC A y PC B |
| `PUERTO_OTRA_PC` | Puerto de destino en la otra PC (50506 por defecto) |
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
| `actualizar_progreso_envio(porcentaje, bytes)` | Actualiza barra de progreso de envío desde el hilo principal. |
| `actualizar_progreso_recepcion(porcentaje, bytes)` | Actualiza barra de progreso de recepción desde el hilo principal. |
| `generar_nombre_unico(nombre_base, carpeta)` | Genera nombre único agregando timestamp si ya existe archivo con ese nombre. |

## Objetos globales
- `sock_servidor` — socket TCP servidor, creado una vez al iniciar; escucha en `MI_PUERTO`.
- `ventana` — ventana principal de tkinter.
- `btn_seleccionar` — botón para seleccionar archivo a enviar.
- `lbl_archivo` — etiqueta que muestra el nombre del archivo seleccionado.
- `progreso_envio` — widget `ttk.Progressbar` para mostrar progreso de envío.
- `progreso_recepcion` — widget `ttk.Progressbar` para mostrar progreso de recepción.
- `estado` — etiqueta que muestra puerto propio, IP/puerto de destino y carpeta de descargas.
- `hilo_servidor` — hilo daemon que corre `aceptar_conexiones()`.
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
