# compartidor-local

Compartí texto en vivo y archivos entre 2 PCs en la misma red local, sin internet.

## Cómo usar
1. Configurá `IP_OTRA_PC` en `notas_compartidas.py` con la IP local de la otra PC
2. Ejecutá en ambas: `python notas_compartidas.py`
3. Pestaña **Texto en vivo**: escribí y se ve al instante en la otra PC
4. Pestaña **Archivos**: seleccioná un archivo y click "Enviar"

## Ejecutable (sin Python)
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --name CompartidorLocal notas_compartidas.py
```
El `.exe` se genera en `dist/CompartidorLocal.exe` (~11 MB). Copialo a la otra PC y ejecutalo.
