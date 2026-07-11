# Log de Cambios — 09-creacion-plan-multi-pc-soporte-2026-07-11_01-41-00

## Fecha
2026-07-11 01:41:00

## Descripción
Creación del plan inicial para el componente "Multi-PC Soporte" que permitirá al sistema funcionar con más de 2 PCs en la red mediante selección manual de destino. Se documentaron 4 alternativas de escalado para futuro.

## Código Original
No existía código previo para este componente.

## Código Nuevo
No se creó código en esta fase. Solo documentación de planificación.

## Cambios en Estructura de Proyecto
- Creada carpeta `DOCUMENTACION/03-Multi-PC-Soporte/plan-inicial/` con 5 archivos:
  - `01-Requerimientos.md`: Definición del problema (limitación a 2 PCs), objetivo (selección manual), alcance, restricciones, requisitos funcionales/no funcionales, casos de uso
  - `02-Analisis.md`: Análisis del dominio, 4 alternativas de escalado consideradas:
    - Opción 1 (ELEGIDA): Selección manual de destino - simple, mantiene arquitectura 1-a-1
    - Opción 2 (Futuro): Broadcast para texto - comunicación de grupo, más complejo
    - Opción 3 (Futuro): Multicast UDP - profesional y eficiente, requiere soporte de router
    - Opción 4 (Futuro): Sistema de salas - máximo flexibilidad, más complejo
  - `03-Diseno.md`: Arquitectura (mantiene 1-a-1), diagrama de flujo de selección, diseño de diálogo de selección, diseño de botón de cambio de destino, modificaciones al código existente, casos borde
  - `04-Codigo.md`: Funciones a modificar (`autodescubrir_continuo`), funciones a agregar (`mostrar_dialogo_seleccion`, `cambiar_destino`), objetos globales a agregar (`btn_cambiar`), modificaciones a interfaz, consideraciones de threading, manejo de errores, testing
  - `05-Checklist.md`: Tareas completadas (documentación) y pendientes (implementación, pruebas)
- Creada carpeta `DOCUMENTACION/03-Multi-PC-Soporte/plan-actual/` con copia de los 5 archivos
- Actualizado `DOCUMENTACION/README.md` agregando componente 03 con estado "En planificación" y actualizando componente 02 a "Implementado"
- Actualizado `Logs/ULTIMO_NUMERO.txt` de "08" a "09"

## Detalles del Diseño

### Solución Elegida: Opción 1 - Selección Manual
- Diálogo de selección condicional: solo aparece cuando hay más de 2 PCs
- Con 1 o 2 PCs, comportamiento idéntico al actual (sin cambios perceptibles)
- Botón "Cambiar destino" para permitir cambio en cualquier momento
- Mantiene arquitectura 1-a-1 (sin comunicación de grupo)
- Compatible con `config.json` existente

### Alternativas Futuras Documentadas
- **Opción 2 (Broadcast):** Para comunicación de grupo real, cada PC recibe texto de todas
- **Opción 3 (Multicast):** Para escalabilidad profesional, tráfico optimizado
- **Opción 4 (Sistema de salas):** Para máxima flexibilidad, múltiples grupos simultáneos

### Ruta de Escalamiento
Cada fase puede implementarse incrementalmente sin descartar la anterior, permitiendo evolución gradual según necesidades.

## Próximos Pasos
- Implementar modificaciones en `autodescubrir_continuo()`
- Implementar diálogo de selección de PC
- Implementar botón de cambio de destino
- Probar en red real con múltiples PCs
- Validar que no haya regresión en caso de 2 PCs
