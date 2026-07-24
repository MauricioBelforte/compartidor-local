# Análisis - Historial de Clipboard

## Análisis del dominio
El clipboard del sistema es un recurso compartido que guarda el último elemento copiado. Para crear un historial, necesitamos:
1. Monitorear periódicamente el clipboard para detectar cambios
2. Guardar cada nuevo contenido con timestamp
3. Mostrar el historial en una pestaña dedicada
4. Sincronizar el historial con la otra PC

## Alternativas consideradas

### Alternativa 1: Usar eventos del sistema para detectar cambios de clipboard
- **Ventaja:** Más eficiente, solo reacciona cuando hay cambios
- **Desventaja:** Requiere librerías externas (pywin32 en Windows), más complejo
- **Decisión:** Rechazada - prefiero mantener el proyecto simple sin dependencias externas

### Alternativa 2: Polling periódico del clipboard
- **Ventaja:** Simple, sin dependencias externas, funciona en todas las plataformas
- **Desventaja:** Menos eficiente, verifica periódicamente aunque no haya cambios
- **Decisión:** Aceptada - polling cada 500ms es suficiente y no afecta performance

### Alternativa 3: Usar el mismo puerto UDP 50508 para clipboard
- **Ventaja:** Menos puertos, configuración más simple
- **Desventaja:** Mezcla protocolos diferentes (mensajes manuales vs clipboard automático)
- **Decisión:** Rechazada - mejor usar puerto UDP 50509 para clipboard

## Decisión de diseño
- Polling periódico del clipboard (cada 500ms)
- Nuevo puerto UDP 50509 para sincronización de clipboard
- Pestaña "Clipboard" con historial de copias
- Formato: `[HH:MM:SS] contenido_copiado`
- Más nuevo arriba

## Protocolo de comunicación
Para sincronización de clipboard:
- Formato: `timestamp|||contenido`
- Delimitador: `|||` (tres barras verticales)
- Encoding: UTF-8
- Transporte: UDP datagramas
- Puerto: 50509

## Consideraciones de privacidad
- El clipboard puede contener información sensible (contraseñas, datos personales)
- El usuario debe ser consciente de que el historial se sincroniza con la otra PC
- Considerar agregar opción para deshabilitar sincronización de clipboard
