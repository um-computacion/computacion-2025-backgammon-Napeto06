# Changelog del Proyecto Backgammon

## Versión 2.0 (Octubre 2025) - Refactorización y Estabilización

Esta versión representa una reconstrucción fundamental del juego para solucionar errores sistémicos, mejorar la estabilidad y añadir funcionalidades clave que estaban pendientes.

### ✨ Mejoras y Nuevas Funcionalidades

- **Refactorización Integral del Core:** Se reescribió por completo la lógica del juego (`core/`) para seguir principios de diseño de software modernos, separando responsabilidades en clases claras y cohesivas (`Game`, `Board`, `Player`, `AIPlayer`, `Dice`).
- **Interfaz de Usuario Reconstruida:** Se reescribió `pygame_ui/main.py` desde cero para integrarse con el nuevo `core`, adoptando una máquina de estados robusta para gestionar el flujo del juego (menú, partida, turno de la IA, fin de juego).
- **IA Completamente Funcional:** La inteligencia artificial ahora juega de forma autónoma y correcta. Su turno es automático, mostrando los dados antes de mover para una mejor experiencia de usuario.
- **Pantalla de Fin de Juego:** Se ha añadido una pantalla de "Game Over" que anuncia al ganador y ofrece opciones para "Jugar de Nuevo" o "Volver al Menú Principal".
- **Lógica de "Bear-Off" Corregida:** Se ha implementado la regla de que solo se pueden retirar fichas con un tiro de dado exacto, eliminando el comportamiento de "overshoot".
- **Mensajes en Pantalla:** El juego ahora muestra un mensaje claro cuando un jugador no tiene movimientos posibles.
- **Mejoras Visuales:**
  - Los dados dobles ahora se muestran en una cuadrícula de 2x2.
  - Las pilas de más de 5 fichas en un punto ahora muestran un contador numérico para mayor claridad.

### 🐛 Corrección de Errores

- **Solucionado el Crash de Arranque (Importación Circular):** Se ha resuelto el `ImportError` crítico causado por dependencias circulares entre los módulos del `core`.
- **Solucionados los Botones No Funcionales:** Se ha corregido el bucle de eventos de Pygame que impedía que los botones del menú principal y otras pantallas respondieran, haciendo el juego completamente navegable.
- **Solucionados Múltiples Crashes en Tiempo de Ejecución:** La nueva arquitectura elimina `TypeError` y `NameError` que ocurrían esporádicamente.
- **Corregida la Lógica de Movimiento:** Las fichas ahora se mueven en la dirección correcta según las reglas del Backgammon, y el consumo de dados es el adecuado.
- **Estabilidad General:** El juego ya no se bloquea y ofrece una experiencia de principio a fin sin interrupciones.

## Versión 2.1 (Noviembre 2025) — Docker, build y arreglos rápidos

Pequeña actualización para preparar el proyecto para trabajar con contenedores Docker y facilitar su ejecución en distintos entornos.

### 🔧 Cambios relevantes

- Se añadió un `Dockerfile` y los pasos necesarios para construir una imagen que incluya las dependencias del proyecto.
- El `Dockerfile` instala dependencias de sistema necesarias para compilar e instalar `pygame` (SDL2, freetype, pkg-config, compilador, etc.) y luego instala las dependencias Python desde `requirements.txt`.
- Se añadió `gunicorn` a `requirements.txt` para disponer del ejecutable en la imagen (si se desea ejecutar la aplicación como servicio WSGI).
- Se corrigió un import en `pygame_ui/main.py` (ahora `import pygame`) que provocaba un AttributeError al iniciar la UI dentro del contenedor.

### 🚀 Cómo usar Docker (resumen rápido)

- Construir la imagen (desde la raíz del repo):

    ```bash
    docker build -t computacion2025backgammonnapeto061:latest .
    ```

- Ejecutar la versión de consola (CLI):

    ```bash
    docker run --rm -it --name backgammon_cli computacion2025backgammonnapeto061:latest python -m cli.cli
    ```

- Ejecutar la UI con X11 (en un entorno Linux con X11):

    ```bash
    xhost +local:docker
    docker run --rm -it \
        --env DISPLAY=$DISPLAY \
        --volume /tmp/.X11-unix:/tmp/.X11-unix \
        --device /dev/dri \
        --name backgammon_ui \
        computacion2025backgammonnapeto061:latest \
        python -m pygame_ui.main
    ```

### 📝 Notas y recomendaciones

- Si obtienes "permission denied" al conectar con el socket de Docker, añade tu usuario al grupo `docker`:

    ```bash
    sudo usermod -aG docker $USER
    # cerrar sesión e iniciar de nuevo o ejecutar `newgrp docker` en la terminal
    ```

- Construir la imagen podrá tardar varios minutos (compila pygame y otras ruedas nativas).
- Si quieres que la imagen arranque automáticamente la CLI o la UI, puedo ajustar el `CMD` en el `Dockerfile`.
