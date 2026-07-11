# Log de Cambios — 06-autodescubrimiento-ip-broadcast-2026-07-10_08-00-00

## Fecha
2026-07-10 08:00:00

## Descripción
Se agrego autodescubrimiento de IP por broadcast UDP. Ya no es necesario configurar la IP manualmente.

## Cambios
- Nuevo modulo de descubrimiento en UDP puerto 50507
- `escuchar_discovery()`: hilo daemon que responde a broadcasts con la IP local
- `buscar_pc(timeout)`: envia broadcast, recolecta respuestas de otras PCs
- `autodescubrir()`: se ejecuta 500ms despues de abrir la app
- Boton "Buscar PC" para buscar en cualquier momento
- Boton "IP manual" como fallback si no funciona el autodescubrimiento
- La IP descubierta se guarda automaticamente en config.json

## Archivos modificados
- `notas_compartidas.py`: agregado modulo discovery, botones Buscar/IP manual
- `archivos_compartidos.py`: mismo sistema de discovery

## Verificacion
- App se abre correctamente
- Hilo de discovery arranca sin errores
- Exe recompilado y subido al release
