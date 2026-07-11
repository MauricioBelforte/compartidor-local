# Requerimientos — Notas compartidas LAN

Documentación del proyecto **Notas compartidas LAN**: comunicación instantánea de texto entre 2 PCs de la misma red local.

## Problema
Dos PCs en la misma red doméstica necesitan un modo rápido de pasarse texto (contraseñas temporales, comandos, links, fragmentos de código, etc.) sin depender de servicios externos — WhatsApp Web, email, USB, servicios en la nube — que agregan pasos innecesarios para algo que está a un salto de red de distancia.

## Objetivo
Crear una aplicación tipo "bloc de notas" que, corriendo en las dos PCs a la vez, sincronice el mismo texto entre ambas casi al instante: lo que se escribe o pega en una aparece automáticamente en la otra.

## Alcance
- Comunicación exclusivamente dentro de la red local (LAN). No usa internet ni servidores externos.
- Sincroniza texto plano, no archivos.
- Pensado para 2 PCs (escalar a más equipos queda fuera del alcance actual — ver `05-Checklist.md`).
- Interfaz de escritorio nativa (ventana propia), no basada en navegador.
- Uso personal en una red de confianza, no en redes públicas o compartidas con desconocidos.

## Restricciones
- Las dos PCs deben estar en la misma red local y poder verse por IP (mismo Wi-Fi/switch, sin aislamiento de clientes activado).
- Requiere Python 3 en ambas máquinas, con `tkinter` (viene por defecto en Windows/Mac; en Linux puede requerir instalar `python3-tk` aparte).
- El firewall de cada PC debe permitir la aplicación en el puerto elegido (UDP 50505).
- Sin autenticación ni cifrado: cualquier dispositivo de la misma red que conozca el puerto podría, en teoría, enviar datos a la ventana. Aceptable para el caso de uso previsto (red doméstica de confianza), pero no apto para redes no confiables.
