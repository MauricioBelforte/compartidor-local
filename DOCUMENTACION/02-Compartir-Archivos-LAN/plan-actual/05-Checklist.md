# Checklist — Compartir archivos LAN

Documentación del componente **Compartir archivos LAN**: transferencia de archivos entre 2 PCs de la misma red local.

## Completado
- [x] Definir arquitectura (P2P simétrico vs. cliente-servidor) y elegir P2P
- [x] Elegir protocolo de transporte (TCP vs. UDP) y elegir TCP
- [x] Diseñar protocolo de transferencia (metadatos + contenido en chunks)
- [x] Elegir lenguaje e interfaz (Python + tkinter, consistente con notas compartidas)
- [x] Definir puerto TCP 50506 (diferente de UDP 50505 de notas)
- [x] Diseñar estructura de metadatos (longitud nombre, nombre, tamaño)
- [x] Diseñar flujo de envío (selección, conexión, chunking, progreso)
- [x] Diseñar flujo de recepción (aceptar, metadatos, guardado, progreso)
- [x] Diseñar manejo de threading (hilo servidor, hilos por conexión)
- [x] Diseñar actualización thread-safe de interfaz (ventana.after)
- [x] Diseñar manejo de nombres duplicados (timestamp)
- [x] Diseñar carpeta de descargas configurable
- [x] Documentar el componente (este set de archivos)
- [x] Integrar componente en app unificada con pestañas (ttk.Notebook)
- [x] Implementar descubrimiento automático de IP vía broadcast UDP
- [x] Implementar configuración persistente en config.json
- [x] Implementar interfaz unificada con pestañas "Texto en vivo" y "Archivos"
- [x] Implementar historial de transferencias en interfaz
- [x] Implementar botones de búsqueda automática y configuración manual de IP

## Pendiente
- [x] Implementar módulo de archivos en `notas_compartidas.py` con todas las funciones
- [x] Implementar interfaz gráfica (botón selección, barras de progreso, etiquetas)
- [x] Implementar lógica de envío de metadatos
- [x] Implementar lógica de envío de archivo en chunks
- [x] Implementar lógica de recepción de metadatos
- [x] Implementar lógica de recepción de archivo en chunks
- [x] Implementar actualización de barras de progreso
- [x] Implementar generación de nombres únicos
- [x] Implementar manejo de errores (conexión, I/O, socket)
- [x] Implementar historial simple de archivos transferidos
- [ ] Validar protocolo con prueba en loopback
- [ ] Probar transferencia de archivos de diferentes tipos (texto, imagen, binario)
- [ ] Probar transferencia de archivos de diferentes tamaños (pequeño, mediano)
- [ ] Probar en 2 PCs reales dentro de LAN
- [ ] Confirmar permisos de firewall en Windows/Mac (TCP 50506 y UDP 50507)
- [ ] Implementar cancelación de transferencia en curso
- [ ] Logging más completo (errores, transferencias, estadísticas)
- [ ] Evaluar soporte para múltiples transferencias simultáneas
- [ ] Evaluar compresión de archivos antes de transferencia
- [ ] (Opcional, fuera del alcance actual) Soporte para más de 2 PCs
