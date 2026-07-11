# Checklist — Multi-PC Soporte

Documentación del componente **Multi-PC Soporte**: soporte para más de 2 PCs en la red con selección manual de destino.

## Completado
- [x] Definir problema y objetivo del componente
- [x] Analizar alternativas de escalado (selección manual, broadcast, multicast, sistema de salas)
- [x] Elegir solución: Selección manual de destino (Opción 1)
- [x] Documentar alternativas futuras para escalado
- [x] Diseñar flujo de selección condicional
- [x] Diseñar diálogo de selección de PC
- [x] Diseñar botón de cambio de destino
- [x] Diseñar modificaciones a `autodescubrir_continuo()`
- [x] Diseñar función `mostrar_dialogo_seleccion()`
- [x] Diseñar función `cambiar_destino()`
- [x] Diseñar modificaciones a interfaz (barra inferior)
- [x] Documentar casos borde (PC offline, nueva PC, etc.)
- [x] Documentar el componente (este set de archivos)

## Pendiente
- [ ] Modificar `autodescubrir_continuo()` para verificar cantidad de PCs
- [ ] Implementar `mostrar_dialogo_seleccion(ips)` con lista de IPs y nombres
- [ ] Implementar `cambiar_destino()` con timeout de 4s
- [ ] Agregar botón `btn_cambiar` en barra inferior
- [ ] Probar caso 1 PC (autodescubrimiento sin diálogo)
- [ ] Probar caso 2 PCs (autodescubrimiento sin diálogo)
- [ ] Probar caso 3+ PCs (autodescubrimiento con diálogo)
- [ ] Probar botón "Cambiar destino" en cualquier momento
- [ ] Probar caso sin PCs (mensaje informativo)
- [ ] Probar caso gethostbyaddr falla (fallback a IP)
- [ ] Probar en red real con múltiples PCs
- [ ] Validar que no haya regresión en caso de 2 PCs
- [ ] (Opcional futuro) Implementar Opción 2: Broadcast para texto
- [ ] (Opcional futuro) Implementar Opción 3: Multicast UDP
- [ ] (Opcional futuro) Implementar Opción 4: Sistema de salas
