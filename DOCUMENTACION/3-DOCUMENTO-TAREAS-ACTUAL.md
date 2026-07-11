# Documento de Tareas — Actual

## Tareas Completadas
### App Unificada (notas_compartidas.py con pestañas)
- [x] Unificar texto en vivo + archivos en un solo script con ttk.Notebook
- [x] Pestaña "Texto en vivo" con ScrolledText y sincronización UDP
- [x] Pestaña "Archivos" con selección de archivo, barras de progreso, historial
- [x] Ambos módulos de red arrancan al inicio (UDP + TCP simultáneos)
- [x] Sin conflictos entre puertos (50505 UDP texto, 50506 TCP archivos)
- [x] Layout Tkinter: barra inferior permanece visible al achicar la ventana (grid)
- [x] Release v1.0.0 publicado con binario adjunto en GitHub

### Componente 01 — Notas Compartidas
- [x] Definir arquitectura (P2P simétrico vs. cliente-servidor)
- [x] Elegir protocolo de transporte (UDP vs. TCP)
- [x] Elegir lenguaje e interfaz (Python + tkinter)
- [x] Escribir lógica de red (`enviar`, `escuchar`, manejo de hilo)
- [x] Validar lógica de sockets UDP con prueba en loopback
- [x] Armar interfaz gráfica (ventana, caja de texto, etiqueta de estado)
- [x] Resolver actualización segura de interfaz desde hilo receptor
- [x] Documentar proyecto
- [x] Implementar código completo en `notas_compartidas.py`
- [x] Verificar ejecución de aplicación

### Componente 02 — Compartir Archivos LAN
- [x] Definir arquitectura (P2P simétrico vs. cliente-servidor)
- [x] Elegir protocolo de transporte (TCP vs. UDP)
- [x] Diseñar protocolo de transferencia (metadatos + contenido en chunks)
- [x] Elegir lenguaje e interfaz (Python + tkinter, consistente con notas)
- [x] Definir puerto TCP 50506 (diferente de UDP 50505 de notas)
- [x] Implementar `archivos_compartidos.py` (envío, recepción, progreso, historial)
- [x] Implementar interfaz gráfica (selección archivo, barras progreso, historial)
- [x] Implementar lógica de envío/recepción con metadatos y chunks
- [x] Implementar actualización de barras de progreso (thread-safe)
- [x] Implementar generación de nombres únicos (timestamp)
- [x] Implementar manejo de errores (conexión, I/O, socket)
- [x] Verificar ejecución de aplicación

## Tareas Pendientes
### Componente 01 — Notas Compartidas
- [ ] Probar en 2 PCs reales dentro de LAN
- [ ] Confirmar permisos de firewall en Windows/Mac
- [ ] Descubrimiento automático de IP (broadcast)
- [ ] Manejo de textos muy largos (límite UDP)
- [ ] Logging más completo (errores de recepción, mensajes)
- [ ] Evaluar historial de mensajes vs sobrescribir
- [ ] Evaluar autenticación/cifrado para redes menos confiables
- [ ] (Opcional) Soporte para más de 2 PCs

### Componente 02 — Compartir Archivos LAN
- [ ] Validar protocolo con prueba en loopback
- [ ] Probar transferencia de archivos de diferentes tipos y tamaños
- [ ] Probar en 2 PCs reales dentro de LAN
- [ ] Confirmar permisos de firewall en Windows/Mac (TCP 50506)
- [ ] Implementar cancelación de transferencia en curso
- [ ] Logging más completo (errores, transferencias, estadísticas)
- [ ] Evaluar múltiples transferencias simultáneas
- [ ] (Opcional) Soporte para más de 2 PCs
