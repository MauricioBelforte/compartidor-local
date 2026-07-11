# Checklist — Notas compartidas LAN

Documentación del proyecto **Notas compartidas LAN**: comunicación instantánea de texto entre 2 PCs de la misma red local.

## Completado
- [x] Definir arquitectura (P2P simétrico vs. cliente-servidor) y elegir P2P
- [x] Elegir protocolo de transporte (UDP vs. TCP) y elegir UDP
- [x] Elegir lenguaje e interfaz (Python + tkinter vs. alternativas basadas en navegador)
- [x] Escribir la lógica de red (`enviar`, `escuchar`, manejo de hilo)
- [x] Validar la lógica de sockets UDP con una prueba en loopback (incluyendo tildes/ñ) — OK
- [x] Armar la interfaz gráfica (ventana, caja de texto, etiqueta de estado)
- [x] Resolver la actualización segura de la interfaz desde el hilo receptor (`ventana.after`)
- [x] Documentar el proyecto (este set de archivos)
- [x] Implementar código completo en `notas_compartidas.py`
- [x] Verificar ejecución de la aplicación

## Pendiente
- [ ] Probar en las 2 PCs reales dentro de la LAN (solo se validó la lógica de red en un entorno aislado, no en la red real)
- [ ] Confirmar permisos de firewall en Windows/Mac en el primer uso
- [ ] Descubrimiento automático de IP (broadcast), para no tener que configurar `IP_OTRA_PC` a mano
- [ ] Manejo de textos muy largos (por encima del límite práctico de un datagrama UDP)
- [ ] Logging más completo (errores de recepción, mensajes intercambiados)
- [ ] Decidir si vale la pena un historial de mensajes en vez de sobrescribir el texto anterior
- [ ] Evaluar si hace falta algún tipo de autenticación/cifrado si se llegara a usar en una red menos confiable
- [ ] (Opcional, fuera del alcance actual) Soporte para más de 2 PCs
