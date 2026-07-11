# Requerimientos — Compartir archivos LAN

Documentación del componente **Compartir archivos LAN**: transferencia de archivos entre 2 PCs de la misma red local.

## Problema
Dos PCs en la misma red doméstica necesitan un modo rápido de compartir archivos (documentos, imágenes, código, etc.) sin depender de servicios externos — email, WhatsApp Web, USB, servicios en la nube — que agregan pasos innecesarios para algo que está a un salto de red de distancia. Aunque ya existe el componente de notas compartidas para texto, este no maneja archivos binarios.

## Objetivo
Crear una aplicación que permita transferir archivos entre dos PCs de la misma red local de forma directa y rápida, con una interfaz simple que integre o complemente la funcionalidad de notas compartidas existente.

## Alcance
- Comunicación exclusivamente dentro de la red local (LAN). No usa internet ni servidores externos.
- Transferencia de archivos de cualquier tipo (texto, imágenes, binarios, etc.).
- Pensado para 2 PCs (escalar a más equipos queda fuera del alcance actual — ver `05-Checklist.md`).
- Interfaz de escritorio nativa (ventana propia), consistente con el componente de notas compartidas.
- Uso personal en una red de confianza, no en redes públicas o compartidas con desconocidos.
- Tamaño de archivos: inicialmente enfocado en archivos pequeños/medianos (hasta unos 100 MB). Archivos muy grandes pueden requerir optimizaciones adicionales.

## Restricciones
- Las dos PCs deben estar en la misma red local y poder verse por IP (mismo Wi-Fi/switch, sin aislamiento de clientes activado).
- Requiere Python 3 en ambas máquinas, con `tkinter` (viene por defecto en Windows/Mac; en Linux puede requerir instalar `python3-tk` aparte).
- El firewall de cada PC debe permitir la aplicación en el puerto elegido (TCP 50506 para diferenciar del componente de notas que usa UDP 50505).
- Sin autenticación ni cifrado: cualquier dispositivo de la misma red que conozca el puerto podría, en teoría, enviar/recibir archivos. Aceptable para el caso de uso previsto (red doméstica de confianza), pero no apto para redes no confiables.
- Debe coexistir con el componente de notas compartidas (puertos diferentes para evitar conflictos).

## Requisitos Funcionales
- Selección de archivo para enviar desde el sistema de archivos local
- Visualización de progreso de transferencia (porcentaje, bytes transferidos)
- Recepción automática de archivos con guardado en carpeta configurable
- Indicador de estado (conectado/desconectado, transferencia en curso)
- Historial simple de archivos transferidos (opcional pero deseable)
- Cancelación de transferencia en curso (opcional pero deseable)

## Requisitos No Funcionales
- Fiabilidad: uso de TCP para garantizar entrega completa de archivos
- Performance: transferencia eficiente sin saturar la red
- Simplicidad: interfaz intuitiva similar a notas compartidas
- Robustez: manejo de errores de conexión, archivos corruptos, etc.
