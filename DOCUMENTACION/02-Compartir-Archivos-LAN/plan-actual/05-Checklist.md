# Checklist — Compartir archivos LAN

Documentación del componente **Compartir archivos LAN**: transferencia de archivos entre 2 PCs de la misma red local.

## Completado
- [ ] Definir arquitectura (P2P simétrico vs. cliente-servidor) y elegir P2P
- [ ] Elegir protocolo de transporte (TCP vs. UDP) y elegir TCP
- [ ] Diseñar protocolo de transferencia (metadatos + contenido en chunks)
- [ ] Elegir lenguaje e interfaz (Python + tkinter, consistente con notas compartidas)
- [ ] Definir puerto TCP 50506 (diferente de UDP 50505 de notas)
- [ ] Diseñar estructura de metadatos (longitud nombre, nombre, tamaño)
- [ ] Diseñar flujo de envío (selección, conexión, chunking, progreso)
- [ ] Diseñar flujo de recepción (aceptar, metadatos, guardado, progreso)
- [ ] Diseñar manejo de threading (hilo servidor, hilos por conexión)
- [ ] Diseñar actualización thread-safe de interfaz (ventana.after)
- [ ] Diseñar manejo de nombres duplicados (timestamp)
- [ ] Diseñar carpeta de descargas configurable
- [ ] Documentar el componente (este set de archivos)

## Pendiente
- [x] Implementar `archivos_compartidos.py` con todas las funciones
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
- [ ] Confirmar permisos de firewall en Windows/Mac
- [ ] Implementar cancelación de transferencia en curso
- [ ] Logging más completo (errores, transferencias, estadísticas)
- [ ] Evaluar soporte para múltiples transferencias simultáneas
- [ ] Evaluar compresión de archivos antes de transferencia
- [ ] (Opcional, fuera del alcance actual) Soporte para más de 2 PCs
