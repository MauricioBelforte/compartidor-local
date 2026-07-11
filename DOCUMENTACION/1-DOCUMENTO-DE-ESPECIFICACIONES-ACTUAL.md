# Documento de Especificaciones — Actual

## Propósito del Proyecto
Comunicación instantánea entre 2 PCs de la misma red local (LAN) sin depender de servicios externos: texto en vivo + transferencia de archivos.

## Requisitos Funcionales
- Sincronización de texto en tiempo casi real entre 2 PCs
- Transferencia de archivos de cualquier tipo vía TCP
- App unificada con 2 pestañas (texto en vivo + archivos)
- Comunicación exclusivamente dentro de la red local (LAN)
- Interfaz de escritorio nativa (ventana propia)
- Un solo archivo ejecutable en ambas PCs (solo cambia IP de destino)

## Requisitos No Funcionales
- Python 3 con tkinter en ambas máquinas
- Puerto UDP 50505 (configurable)
- Firewall debe permitir la aplicación en el puerto elegido
- Sin autenticación ni cifrado (red de confianza)

## Stack Tecnológico
- **Lenguaje:** Python 3
- **Interfaz:** tkinter + ttk
- **Comunicación:** Socket UDP (texto) + TCP (archivos)
- **Arquitectura:** P2P simétrico

## Restricciones
- Las dos PCs deben estar en la misma red local
- Pensado para uso personal en red de confianza
- No apto para redes públicas o compartidas con desconocidos
- Texto en vivo: UDP puerto 50505, sin ACK
- Archivos: TCP puerto 50506, una transferencia a la vez por dirección
- Pensado para 2 PCs (escalar a más equipos fuera de alcance actual)
