# Análisis - Mejoras UI 4 Pestañas

## Análisis del dominio
El usuario necesita enviar mensajes rápidos entre PCs de su red local con un flujo simplificado:
- Enviar mensaje → se limpia el input
- Recibir mensaje → aparece en área de recepción
- Copiar mensaje → se copia al clipboard y se limpia el área
- Historial → todos los mensajes quedan registrados

## Alternativas consideradas

### Alternativa 1: Modificar pestaña "Texto en vivo" existente
- **Ventaja:** Menos cambios en la UI
- **Desventaja:** Pierde la funcionalidad de edición en tiempo real que el usuario usa actualmente
- **Decisión:** Rechazada - el usuario quiere mantener "Texto en vivo" como está

### Alternativa 2: Crear pestaña única para envío/recepción/historial
- **Ventaja:** Menos pestañas en total
- **Desventaja:** Mezcla funcionalidades diferentes, puede ser confuso
- **Decisión:** Rechazada - el usuario pidió explícitamente 4 pestañas separadas

### Alternativa 3: Usar el mismo puerto UDP para todo
- **Ventaja:** Menos puertos, configuración más simple
- **Desventaja:** Colisiones entre mensajes de texto en vivo y mensajes rápidos
- **Decisión:** Rechazada - mejor separar por funcionalidad

## Decisión de diseño
Crear 4 pestañas separadas con puertos dedicados:
- **Texto en vivo:** UDP 50505 (existente, sin cambios funcionales)
- **Enviar y recibir texto:** UDP 50508 (nuevo)
- **Archivos:** TCP 50506 (existente, sin cambios)
- **Historial:** UDP 50508 (compartido con "Enviar y recibir texto")

## Protocolo de comunicación
Para "Enviar y recibir texto" e "Historial":
- Formato: `timestamp|||mensaje`
- Delimitador: `|||` (tres barras verticales)
- Encoding: UTF-8
- Transporte: UDP datagramas

## Indicador visual de conexión
- Ubicación: Barra inferior (junto a botones existentes)
- Diseño: Canvas con círculo/cuadrado
- Estados:
  - Verde: `IP_OTRA_PC` configurada y no vacía
  - Gris: `IP_OTRA_PC` vacía
