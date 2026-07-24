# Requerimientos - Historial de Clipboard

## Problema
El usuario necesita un historial de todo lo que copia al clipboard (con Ctrl+C o copiar con el mouse) para poder recuperar copias anteriores. Actualmente el clipboard solo guarda el último elemento copiado.

## Objetivos
- Agregar una nueva pestaña "Clipboard" que muestre un historial de copias
- Monitorear el clipboard del sistema automáticamente
- Guardar timestamp de cada copia
- Permitir sincronización del historial entre PCs
- Mantener compatibilidad con las 4 pestañas existentes

## Alcance
- Modificar `notas_compartidas.py` para agregar la pestaña "Clipboard"
- Implementar polling del clipboard del sistema (verificación periódica)
- Usar puerto UDP nuevo o existente para sincronización
- No modificar funcionalidad existente

## Restricciones
- Debe seguir el flujo Documentation-First del proyecto
- Debe mantener compatibilidad con la arquitectura P2P existente
- Debe ser thread-safe (actualizaciones de UI desde hilos de monitoreo)
- Debe mantener la estructura de documentación del proyecto
