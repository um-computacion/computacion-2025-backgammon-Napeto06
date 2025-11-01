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
