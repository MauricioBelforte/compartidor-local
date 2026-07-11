# Análisis — Multi-PC Soporte

Documentación del componente **Multi-PC Soporte**: soporte para más de 2 PCs en la red con selección manual de destino.

## Análisis del dominio
El problema es escalar el sistema de comunicación 1-a-1 para funcionar en redes con más de 2 dispositivos. El sistema actual tiene una arquitectura punto a punto simple: cada PC tiene una sola IP destino configurada. Para soportar múltiples PCs, necesitamos permitir selección dinámica de destino sin cambiar la arquitectura base de comunicación.

## Alternativas de Escalado Consideradas

### Opción 1: Selección Manual (ELEGIDA)
**Descripción:** Cuando el descubrimiento automático encuentra múltiples IPs, mostrar un diálogo de selección para que el usuario elija a cuál PC conectarse. Permitir cambiar el destino en cualquier momento mediante un botón adicional.

**Ventajas:**
- Simple de implementar
- Poco cambio en arquitectura existente
- Mantiene comunicación 1-a-1 (sin complejidad de grupo)
- UX intuitiva para el usuario

**Desventajas:**
- No hay comunicación de grupo real
- Cada PC solo se comunica con una a la vez
- Requiere interacción del usuario para cambiar destino

**Decisión:** Elegida para esta fase por simplicidad y alineación con caso de uso actual.

---

### Opción 2: Broadcast para Texto (Comunicación de Grupo)
**Descripción:** Cambiar el módulo de texto en vivo para usar broadcast UDP (`255.255.255.255`) en lugar de unicast. Todas las PCs en la red recibirían el texto de todas las demás.

**Ventajas:**
- Comunicación de grupo real sin servidor
- Todas las PCs ven el texto de todas
- Escalable a N PCs automáticamente

**Desventajas:**
- Cada PC vería su propio texto reflejado (necesita filtrado por IP)
- Tráfico de red mayor (cada mensaje enviado a todos)
- No funciona para archivos (TCP no soporta broadcast)
- Más complejo de implementar

**Estado:** Documentado para futuro si se requiere comunicación de grupo real.

---

### Opción 3: Multicast UDP
**Descripción:** Usar multicast UDP (ej: dirección `239.255.255.250`) en lugar de unicast o broadcast. Las PCs se unen a un grupo multicast y reciben mensajes dirigidos a ese grupo.

**Ventajas:**
- Comunicación de grupo eficiente
- Tráfico de red optimizado (solo routers que tienen miembros del grupo reciben)
- Escalable a grandes redes
- Profesional y robusto

**Desventajas:**
- Requiere cambios significativos en arquitectura
- Routers deben soportar multicast (algunos routers domésticos no)
- Más complejo de configurar y depurar
- No funciona para archivos (TCP no soporta multicast)

**Estado:** Documentado para futuro si se requiere escalabilidad profesional.

---

### Opción 4: Sistema de Salas
**Descripción:** Implementar un sistema de "salas" donde las PCs pueden crear o unirse a salas con nombres. El descubrimiento automático encontraría salas disponibles en la red. La comunicación ocurre dentro de cada sala.

**Ventajas:**
- Flexible: múltiples grupos simultáneos
- Cada PC puede participar en múltiples salas
- Escalable a N PCs y N grupos
- UX rica para gestión de grupos

**Desventajas:**
- Más complejo de implementar
- Requiere UI adicional para gestión de salas
- Mayor superficie de código a mantener
- Sobrecarga para caso simple de 2 PCs

**Estado:** Documentado para futuro si se requiere flexibilidad de grupos.

---

## Decisiones Clave (Opción 1 Elegida)

1. **Mantener arquitectura 1-a-1:** No cambiar la base de comunicación punto a punto. Solo agregar capa de selección de destino.

2. **Diálogo de selección condicional:** Solo mostrar diálogo cuando hay más de 2 PCs. Con 2 PCs, comportamiento idéntico al actual.

3. **Botón de cambio de destino:** Agregar botón en la interfaz para permitir cambiar destino en cualquier momento sin reiniciar.

4. **Validación de disponibilidad:** Antes de establecer conexión, verificar que la PC seleccionada esté respondiendo al descubrimiento.

5. **Mantener config.json:** No cambiar el formato de configuración existente. La IP seleccionada se guarda igual que antes.

6. **UX simple:** El diálogo debe ser simple (lista de IPs con nombres si es posible). No complicar la interfaz actual.

7. **Compatibilidad hacia atrás:** Debe funcionar exactamente igual con 2 PCs sin cambios perceptibles para el usuario.

## Limitaciones de la Solución Elegida

- **Sin comunicación de grupo:** Si 3 PCs (A, B, C) están en la red:
  - A conectada a B → A↔B comunican
  - B conectada a A → A↔B comunican
  - C conectada a A → A↔C comunican
  - B y C no se comunican entre sí directamente

- **Una conexión a la vez:** Cada PC solo puede tener un destino activo. Para hablar con otra PC, debe cambiar destino manualmente.

- **No persistencia de múltiples destinos:** No hay historial de PCs usadas. Cada vez que se cambia, se sobrescribe la configuración.

## Ruta de Escalamiento Futura

Si en el futuro se requiere comunicación de grupo real, se puede evolucionar de esta manera:

1. **Fase actual (Opción 1):** Selección manual de destino, comunicación 1-a-1
2. **Fase siguiente (Opción 2):** Broadcast para texto, filtrado de IP propia
3. **Fase avanzada (Opción 3):** Multicast UDP para eficiencia
4. **Fase completa (Opción 4):** Sistema de salas para máxima flexibilidad

Cada fase puede implementarse incrementalmente sin descartar la anterior.
