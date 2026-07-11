# Análisis — Notas compartidas LAN

Documentación del proyecto **Notas compartidas LAN**: comunicación instantánea de texto entre 2 PCs de la misma red local.

## Análisis del dominio
El problema es, en esencia, sincronizar un valor compartido (el texto) entre dos nodos de la misma red local, en tiempo casi real. No hace falta persistencia, no hace falta más de un "documento" a la vez, y el volumen de datos es bajo (texto corto, no archivos binarios). Eso simplifica bastante las alternativas frente a un problema de sincronización general.

## Alternativas consideradas

### Modelo de comunicación
| Opción | Descripción | Observación |
|---|---|---|
| Cliente-servidor | Una PC actúa de servidor, la otra de cliente | Asimetría innecesaria para 2 equipos; si el "servidor" se cierra, el otro queda sin conexión |
| **P2P / simétrico (elegido)** | Las dos PCs corren el mismo script; cada una es emisor y receptor a la vez | Sin punto único de falla; el mismo archivo sirve para las dos máquinas |

### Protocolo de transporte
| Opción | Descripción | Observación |
|---|---|---|
| TCP | Conexión persistente, con handshake | Cada PC debería aceptar conexiones entrantes *y* mantener una saliente — más manejo de hilos y de reconexión |
| **UDP (elegido)** | Datagramas sin conexión | Sin garantía de entrega, pero irrelevante acá: cada mensaje manda el texto completo, así que un paquete perdido lo reemplaza el siguiente cambio |

### Lenguaje e interfaz
| Opción | Descripción | Observación |
|---|---|---|
| Node.js + Socket.io | Reconexión automática, pensado para tiempo real | Requiere instalar Node y dependencias; más natural si fuera basado en navegador |
| Python + Flask + WebSockets | Accesible desde el navegador en cada PC | Hay que levantar un servidor web e instalar Flask/Flask-SocketIO; no da la sensación de ventana tipo bloc de notas |
| **Python + tkinter + socket (elegido)** | Ventana nativa, solo librería estándar | `socket` y `tkinter` ya vienen incluidos; código corto, fácil de seguir y modificar |

## Decisiones clave
1. **Arquitectura simétrica**: un solo archivo (`notas_compartidas.py`), usado sin cambios de lógica en las dos PCs; solo cambia la IP de destino configurada en cada una.
2. **UDP sobre el puerto 50505**: puerto alto, fuera del rango típico de servicios conocidos (se evitó el 5000, usado por AirPlay Receiver en macOS).
3. **Envío en cada `KeyRelease`**: cubre tanto tipear como pegar (Ctrl+V), sin necesidad de un botón "Enviar" explícito — alineado con el objetivo de "pegar y ver al instante".
4. **Última escritura gana**: no se implementó resolución de conflictos. Si las dos personas escriben literalmente al mismo tiempo, el último mensaje enviado sobrescribe al anterior. Se aceptó como límite razonable dado el uso previsto (pegar información puntual, no edición colaborativa simultánea).
