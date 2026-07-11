# Requerimientos — Multi-PC Soporte

Documentación del componente **Multi-PC Soporte**: soporte para más de 2 PCs en la red con selección manual de destino.

## Problema
El sistema actual está diseñado para comunicación 1-a-1 entre 2 PCs. Cuando hay más de 2 PCs en la red:
- El descubrimiento automático encuentra todas las PCs pero solo usa la primera
- No hay forma de seleccionar entre múltiples destinos
- Cada PC solo puede comunicarse con una sola IP configurada
- No hay comunicación de grupo

Esto limita el uso en redes domésticas donde pueden haber 3 o más dispositivos (ej: PC de escritorio, notebook, tablet, etc.).

## Objetivo
Permitir que el sistema funcione con más de 2 PCs en la red, manteniendo la simplicidad de comunicación 1-a-1 pero permitiendo seleccionar dinámicamente el destino cuando hay múltiples opciones disponibles.

## Alcance
- Comunicación sigue siendo 1-a-1 (no comunicación de grupo)
- Cuando el descubrimiento automático encuentra más de 2 IPs, mostrar diálogo de selección
- Permitir cambiar el destino sin reiniciar la aplicación
- Mantener compatibilidad con el caso de 2 PCs (sin cambios en UX cuando solo hay 2)
- Integrado en la app unificada existente (`notas_compartidas.py`)

## Restricciones
- No cambiar la arquitectura base de comunicación 1-a-1
- No implementar comunicación de grupo (broadcast, multicast, salas) en esta fase
- Mantener simplicidad de la interfaz actual
- No requerir cambios en la configuración persistente existente (`config.json`)

## Requisitos Funcionales
- Detectar cuando el descubrimiento automático encuentra más de 2 PCs
- Mostrar diálogo de selección de destino cuando hay múltiples opciones
- Permitir cambiar el destino en cualquier momento (botón adicional)
- Mostrar IP destino actual en la interfaz
- Mantener comunicación 1-a-1 después de seleccionar destino
- Validar que la PC seleccionada esté disponible antes de establecer conexión

## Requisitos No Funcionales
- Simplicidad: UX intuitiva, sin complicar la interfaz actual
- Performance: descubrimiento rápido, sin impacto en transferencias
- Compatibilidad: debe funcionar con el caso de 2 PCs sin cambios perceptibles
- Robustez: manejo de PCs que se desconectan/reconectan

## Casos de Uso
- **Caso 1 (2 PCs)**: Comportamiento idéntico al actual, sin cambios
- **Caso 2 (3+ PCs)**: Al iniciar, si hay múltiples PCs, mostrar diálogo de selección
- **Caso 3 (Cambio de destino)**: Usuario puede cambiar destino en cualquier momento
- **Caso 4 (PC offline)**: Si la PC seleccionada está offline, permitir re-seleccionar otra
