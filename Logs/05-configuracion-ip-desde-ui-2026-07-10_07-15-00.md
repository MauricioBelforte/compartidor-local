# Log de Cambios — 05-configuracion-ip-desde-ui-2026-07-10_07-15-00

## Fecha
2026-07-10 07:15:00

## Descripción
Se eliminó la dependencia de editar el código para configurar la IP. Ahora la IP de la otra PC se configura desde la interfaz gráfica.

## Cambios
- Se agregó sistema de config.json: la IP se guarda/lee de un archivo JSON junto al ejecutable
- En el primer inicio, si no hay config.json, se muestra un diálogo pidiendo la IP
- Botón "Configurar IP" en ambas apps para cambiar la IP en cualquier momento
- `notas_compartidas.py`: botón en barra inferior, IP se aplica a ambas pestañas
- `archivos_compartidos.py`: mismo sistema, mismo botón
- Las etiquetas de estado se actualizan dinámicamente al cambiar la IP

## Archivos modificados
- `notas_compartidas.py`: reescrita sección de configuración, agregadas funciones cargar/guardar/pedir IP, botón config
- `archivos_compartidos.py`: mismo sistema de config.json, botón configurar IP

## Verificación
- App unificada se abre y pide IP si no hay config.json
- Botón "Configurar IP" funciona correctamente
- Etiquetas de estado reflejan la IP configurada
- Exe recompilado y subido al release v1.0.0
