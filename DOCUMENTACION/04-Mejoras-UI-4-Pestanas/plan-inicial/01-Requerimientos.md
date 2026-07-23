# Requerimientos - Mejoras UI 4 Pestañas

## Problema
La interfaz actual de "Compartidor Local" tiene solo 2 pestañas (Texto en vivo y Archivos). El usuario necesita una mejor experiencia para enviar mensajes rápidos entre PCs de su red local, con un flujo más cómodo: enviar, recibir, copiar y limpiar rápidamente.

## Objetivos
- Agregar 2 nuevas pestañas para mejorar la UX: "Enviar y recibir texto" e "Historial"
- Implementar un indicador visual de conexión (círculo/cuadrado verde) en lugar de mensajes de texto en el área de texto en vivo
- Permitir envío rápido de mensajes con input que se limpia automáticamente
- Permitir recepción de mensajes con botón de copiar que limpia el área
- Mantener un historial sincronizado de todos los mensajes enviados/recibidos

## Alcance
- Modificar `notas_compartidas.py` para tener 4 pestañas en lugar de 2
- Agregar nuevo puerto UDP 50508 para mensajes rápidos e historial
- Mantener funcionalidad existente de "Texto en vivo" (UDP 50505) y "Archivos" (TCP 50506)
- No modificar `archivos_compartidos.py`

## Restricciones
- Debe seguir el flujo Documentation-First del proyecto
- Debe mantener compatibilidad con la arquitectura P2P existente
- Debe ser thread-safe (actualizaciones de UI desde hilos de red)
- Debe mantener la estructura de documentación del proyecto
