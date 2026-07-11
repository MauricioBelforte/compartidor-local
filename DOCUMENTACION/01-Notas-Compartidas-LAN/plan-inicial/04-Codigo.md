# Código — Notas compartidas LAN

Documentación del proyecto **Notas compartidas LAN**: comunicación instantánea de texto entre 2 PCs de la misma red local.

## Archivos involucrados
| Archivo | Rol |
|---|---|
| `notas_compartidas.py` | Único archivo del proyecto. Contiene configuración, lógica de red e interfaz gráfica. Se usa sin cambios de lógica en las dos PCs — solo cambia el valor de `IP_OTRA_PC`. |

## Configuración (constantes)
| Constante | Descripción |
|---|---|
| `MI_PUERTO` | Puerto donde esta PC escucha (50505 por defecto, igual en ambas PCs) |
| `IP_OTRA_PC` | IP local de la otra PC — el único valor que difiere entre PC A y PC B |
| `PUERTO_OTRA_PC` | Puerto de destino en la otra PC (50505 por defecto) |

## Funciones clave
| Función | Qué hace |
|---|---|
| `enviar(event=None)` | Lee el contenido de la caja de texto y lo manda por UDP a la otra PC. Atada al evento `<KeyRelease>`. |
| `escuchar()` | Loop bloqueante en un hilo aparte; espera datagramas entrantes y agenda la actualización de la interfaz. |
| `actualizar_caja(texto)` | Reemplaza el contenido de la caja de texto con el texto recibido. Solo se llama desde el hilo principal (vía `ventana.after`). |

## Objetos globales
- `sock` — socket UDP, creado una vez al iniciar; se cierra al cerrar la ventana.
- `ventana` — ventana principal de tkinter.
- `caja` — widget `ScrolledText` donde se escribe/lee el texto compartido.
- `estado` — etiqueta que muestra puerto propio e IP/puerto de destino, útil para verificar la configuración a simple vista.
- `hilo` — hilo daemon que corre `escuchar()`.

## Logs
Todavía no hay un sistema de logging formal. El único registro actual es un `print()` en consola si falla el envío (dentro de `enviar()`, ante una excepción `OSError`). No se registran los mensajes recibidos ni errores de recepción — si `escuchar()` encuentra un `OSError` (por ejemplo, al cerrarse el socket), el loop simplemente termina sin dejar rastro. Agregar logging más completo queda pendiente (ver `05-Checklist.md`).
