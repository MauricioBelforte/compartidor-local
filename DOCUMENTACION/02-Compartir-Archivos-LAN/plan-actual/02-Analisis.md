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
| Archivo separado, puerto diferente | `archivos_compartidos.py` con puerto TCP 50506 | Separación clara; coexistencia con notas; modularidad |
| **App unificada con pestañas (elegido)** | `notas_compartidas.py` con ttk.Notebook (Texto en vivo + Archivos) | Mejor UX; un solo proceso; configuración compartida; descubrimiento automático compartido |

### Interfaz gráfica
| Opción | Descripción | Observación |
|---|---|---|
| Consola/CLI | Transferencia por línea de comandos | Menos amigable; requiere conocimientos técnicos |
| **tkinter (elegido)** | Interfaz gráfica nativa | Consistente con notas compartidas; fácil de usar; solo librería estándar |

## Decisiones clave
1. **App unificada con pestañas**: `notas_compartidas.py` con ttk.Notebook integra "Texto en vivo" (UDP 50505) y "Archivos" (TCP 50506) en una sola ventana.
2. **Arquitectura simétrica**: un solo archivo usado sin cambios de lógica en las dos PCs; solo cambia el valor de `IP_OTRA_PC`.
3. **TCP sobre el puerto 50506**: puerto alto, diferente del 50505 usado por notas compartidas (UDP), para evitar conflictos.
4. **Descubrimiento automático de IP**: broadcast UDP en puerto 50507 permite encontrar automáticamente la otra PC en la red.
5. **Configuración persistente**: IP guardada en `config.json` para no tener que reconfigurar cada vez.
6. **Protocolo simple**: enviar metadatos primero (nombre archivo, tamaño), luego el contenido binario. Esto permite al receptor saber qué esperar y validar integridad.
7. **Chunking**: leer y enviar en bloques (chunks) de tamaño fijo (4096 bytes) para no cargar archivos grandes en memoria y permitir actualización de progreso.
8. **Barra de progreso**: mostrar porcentaje y bytes transferidos al usuario durante la transferencia.
9. **Carpeta de descargas configurable**: por defecto `descargas/` en el mismo directorio del script.
10. **Sobrescritura de archivos**: si ya existe un archivo con el mismo nombre, se agrega timestamp automáticamente para evitar pérdida de datos.
11. **Transferencia uno-a-uno**: una transferencia a la vez; si llega una nueva mientras hay una en curso, se rechaza temporalmente.
