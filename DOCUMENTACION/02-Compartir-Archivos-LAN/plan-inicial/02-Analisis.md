# Análisis — Compartir archivos LAN

Documentación del componente **Compartir archivos LAN**: transferencia de archivos entre 2 PCs de la misma red local.

## Análisis del dominio
El problema es transferir datos binarios (archivos) entre dos nodos de la misma red local de manera confiable. A diferencia del componente de notas compartidas (que usa UDP para texto corto), los archivos requieren garantía de entrega completa, integridad de datos, y manejo de tamaños variables. El volumen de datos puede ser significativamente mayor, por lo que se necesita un protocolo confiable y mecanismos de progreso.

## Alternativas consideradas

### Modelo de comunicación
| Opción | Descripción | Observación |
|---|---|---|
| Cliente-servidor | Una PC actúa de servidor, la otra de cliente | Asimetría innecesaria para 2 equipos; si el "servidor" se cierra, el otro queda sin conexión |
| **P2P / simétrico (elegido)** | Las dos PCs corren el mismo script; cada una es emisor y receptor a la vez | Sin punto único de falla; el mismo archivo sirve para las dos máquinas; consistente con componente de notas |

### Protocolo de transporte
| Opción | Descripción | Observación |
|---|---|---|
| UDP | Datagramas sin conexión | Sin garantía de entrega; requeriría implementar ACK, retransmisiones, fragmentación — complejo para archivos |
| **TCP (elegido)** | Conexión persistente, con handshake | Garantiza entrega y orden de bytes; ideal para transferencia de archivos; manejo de flujo automático |

### Estrategia de transferencia
| Opción | Descripción | Observación |
|---|---|---|
| HTTP | Usar servidor HTTP simple | Requiere librerías adicionales; overhead de headers HTTP; más complejo |
| FTP | Protocolo FTP | Requiere librerías adicionales; complejidad innecesaria para 2 PCs |
| **TCP directo (elegido)** | Socket TCP crudo con protocolo simple | Solo librería estándar; control total sobre transferencia; más simple de entender y mantener |

### Integración con notas compartidas
| Opción | Descripción | Observación |
|---|---|---|
| Misma ventana, mismo archivo | Agregar funcionalidad de archivos a `notas_compartidas.py` | Mezcla responsabilidades; archivo crece; difícil mantener |
| **Archivo separado, puerto diferente (elegido)** | `archivos_compartidos.py` con puerto TCP 50506 | Separación clara; coexistencia con notas; modularidad; puede ejecutarse en paralelo |

### Interfaz gráfica
| Opción | Descripción | Observación |
|---|---|---|
| Consola/CLI | Transferencia por línea de comandos | Menos amigable; requiere conocimientos técnicos |
| **tkinter (elegido)** | Interfaz gráfica nativa | Consistente con notas compartidas; fácil de usar; solo librería estándar |

## Decisiones clave
1. **Arquitectura simétrica**: un solo archivo (`archivos_compartidos.py`), usado sin cambios de lógica en las dos PCs; solo cambia el valor de `IP_OTRA_PC`.
2. **TCP sobre el puerto 50506**: puerto alto, diferente del 50505 usado por notas compartidas (UDP), para evitar conflictos.
3. **Protocolo simple**: enviar metadatos primero (nombre archivo, tamaño), luego el contenido binario. Esto permite al receptor saber qué esperar y validar integridad.
4. **Chunking**: leer y enviar en bloques (chunks) de tamaño fijo (ej: 4096 bytes) para no cargar archivos grandes en memoria y permitir actualización de progreso.
5. **Barra de progreso**: mostrar porcentaje y bytes transferidos al usuario durante la transferencia.
6. **Carpeta de descargas configurable**: por defecto una carpeta `descargas/` en el mismo directorio del script, pero configurable.
7. **Sobrescritura de archivos**: si ya existe un archivo con el mismo nombre, preguntar al usuario o agregar timestamp (decisión pendiente).
8. **Transferencia uno-a-uno**: una transferencia a la vez; si llega una nueva mientras hay una en curso, rechazar o encolar (decisión pendiente).
