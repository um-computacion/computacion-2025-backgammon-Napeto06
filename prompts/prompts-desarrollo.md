# Prompt

¿Podrías ayudarme a realizar este código? Con las pautas que te di (SOLID y TDD).

## Respuesta

Se propuso una implementación de la clase Board para el juego de Backgammon, siguiendo los principios SOLID y el método TDD. La clase Board gestiona el estado del tablero, inicializa los puntos según la disposición estándar de Backgammon y permite mover fichas entre puntos. La implementación está preparada para ser testeada y extendida.

## Prompt

El tema es que se tiene que mover acorde a los dados porque depende de qué número toque en el tablero y si está ocupado no puede estar en ese lugar y que si el dado tiene ambos números iguales se duplican ambos dados.

## Respuesta

La lógica de movimiento en Backgammon depende del resultado de los dados y del estado de los puntos en el tablero. El jugador puede mover una ficha tantos puntos como indique cada dado, pero solo si el destino no está ocupado por más de una ficha del oponente. Si ambos dados muestran el mismo número (dobles), el jugador tiene cuatro movimientos en vez de dos.

Para cumplir con SOLID, la lógica de movimiento debe estar en el tablero, no en la ficha. La ficha solo conoce a su dueño. El tablero verifica si el movimiento es válido y ejecuta el movimiento.

A continuación se muestra una propuesta para la clase `Checkers` y la lógica de movimiento en el tablero:

## Prompt

¿Qué te parece el código de ai.py?

## Respuesta

El código de `ai.py` implementa una IA básica para Backgammon que sigue buenas prácticas de diseño y es fácil de extender.  

- Utiliza una clase `AIPlayer` con métodos bien definidos para jugar un turno, generar secuencias de movimientos y elegir la mejor opción.
- El método `play_turn` lanza los dados, genera todas las combinaciones posibles de movimientos y ejecuta la mejor secuencia encontrada.
- La función `_get_possible_sequences` prueba ambos órdenes de los dados y simula movimientos en un tablero temporal, lo que permite evaluar diferentes opciones.
- La selección de la secuencia se realiza de forma aleatoria, pero el diseño permite agregar fácilmente una función de evaluación más avanzada.

El código está alineado con los principios SOLID (especialmente responsabilidad única y fácil extensión) y es apto para aplicar TDD.  
Para mejorar, podrías implementar el método `_copy_board` y agregar una función de evaluación para que la IA tome decisiones más inteligentes.

## Prompt

¿Podés hacer el código de AI.py?

## Respuesta

Se implementó la clase AIPlayer para Backgammon siguiendo SOLID y TDD. La IA lanza los dados, genera movimientos válidos y ejecuta el mejor movimiento disponible. El diseño permite extender la lógica de decisión y facilita la integración con el tablero y los jugadores.

## Prompt

El código está alineado con los principios SOLID (especialmente responsabilidad única y fácil extensión) y es apto para aplicar TDD.  
Para mejorar, podrías implementar el método _copy_board y agregar una función de evaluación para que la IA tome decisiones más inteligentes.
¿Podrías hacer eso?

## Respuesta

Se implementó el método _copy_board usando copy.deepcopy para simular movimientos sin afectar el tablero real. Además, se agregó la función _evaluate_sequence, que asigna un puntaje simple a cada secuencia de movimientos, permitiendo que la IA elija la opción más ventajosa según el avance de sus fichas. Esto mejora la toma de decisiones y mantiene el diseño alineado con SOLID y TDD.

## Prompt

podrías agregar los tests de game?

## Respuesta

Se agregaron tests unitarios para la clase Game. Los tests verifican la inicialización, el flujo de turnos para humano e IA, y el comportamiento cuando el juego termina, utilizando mocks para simular entradas y métodos. Esto asegura que la lógica principal del juego funcione correctamente y facilita el mantenimiento del proyecto.

# Guía de Desarrollo del Proyecto Backgammon

Este documento proporciona una guía técnica para desarrolladores que trabajen en este proyecto. Seguir estas directrices es crucial para mantener la calidad y estabilidad del código.

## 1. Arquitectura del Proyecto

El proyecto está dividido en dos componentes principales:

- **`core/` (Backend - Lógica del Juego):**
  - Contiene toda la lógica pura del Backgammon, sin ninguna dependencia de la interfaz de usuario.
  - **`Game`:** Es el orquestador principal. Gestiona los turnos, los dados y el estado general de la partida.
  - **`Board`:** Representa el tablero. Gestiona la posición de las fichas y valida la legalidad de los movimientos según las reglas.
  - **`Player` / `AIPlayer`:** Representan a los participantes. `AIPlayer` hereda de `Player` y contiene la lógica para la toma de decisiones autónoma.
  - **`Dice`:** Gestiona el estado y las tiradas de los dados.

- **`pygame_ui/` (Frontend - Interfaz Gráfica):**
  - Es responsable de toda la representación visual y la interacción con el usuario.
  - Utiliza `pygame` para renderizar el tablero, las fichas y los menús.
  - **`BackgammonUI`:** Es la clase principal que gestiona la máquina de estados de la UI (menú, partida, fin de juego) y el bucle de eventos.
  - **No debe contener lógica de reglas de juego.** Toda la validación de movimientos se delega al `core`. La UI solo pregunta al `core` si un movimiento es válido (`game.has_possible_moves`, `game.move`, etc.).

## 2. Flujo de Trabajo y Principios de Diseño

- **Separación de Responsabilidades:** Mantener siempre la lógica del juego (`core`) desacoplada de la interfaz (`pygame_ui`). La UI no debe saber *por qué* un movimiento es ilegal, solo que *lo es*.
- **Estado Inmutable (en la medida de lo posible):** La lógica de la IA (`choose_moves`) debe operar sobre una **copia** del tablero (`copy.deepcopy(board)`) para evitar modificar el estado real del juego durante su deliberación.
- **Máquina de Estados en la UI:** La interfaz se gestiona con una máquina de estados (`self.game_state`). Cualquier cambio en el flujo del juego (como pasar del menú a la partida) debe ser un cambio de estado explícito.

## 3. Cómo Ejecutar el Juego

Para iniciar la interfaz gráfica de Pygame, ejecuta el siguiente comando desde la raíz del repositorio:

```bash
python3 pygame_ui/main.py
```

## 4. Dependencias

El proyecto requiere `pygame`. Asegúrate de tenerlo instalado:

```bash
pip install pygame
```

## 5. Importaciones Circulares

El `core` tiene dependencias complejas. Para evitar `ImportError` por importaciones circulares, se utilizan dos técnicas estándar de Python:

- `from __future__ import annotations` en la primera línea del archivo.
- Escribir las anotaciones de tipo como cadenas de texto (ej. `player: 'Player'`) para posponer su evaluación.

# Archivo de Prompts para Desarrollo

Este archivo documenta los prompts utilizados para generar o refactorizar código de la aplicación.

---

## Prompt 1: Refactorizar `core/game.py` para cumplir convenciones

- **Modelo / Herramienta usada**: Jules (Agente de Software Autónomo)
- **Instrucciones del sistema**: "Eres Jules, un ingeniero de software..." (Instrucciones estándar del sistema)
- **Texto exacto del prompt**: "El archivo `core/game.py` tiene un problema importante con las convenciones de nombrado: los atributos no siguen la regla `__atributo__`. Además, los docstrings, aunque presentes, podrían ser más explícitos sobre lo que hace cada función. Voy a corregir ambos problemas: 1. Renombraré todos los atributos para que sigan la convención `__atributo__`. 2. Mejoraré los docstrings de los métodos públicos."
- **Respuesta/resultado completo devuelto por la IA**: 
  ```python
  # (Se incluye aquí el bloque de código completo generado por la IA,
  # que corresponde a la refactorización de la clase Game con los
  # nuevos nombres de atributos y docstrings mejorados)
  class Game:
      def __init__(self, players: list['Player'], random_positions=False):
          """
          Initializes the Game object.
          ...
          """
          self.__players__ = players
          self.__board__ = Board(players[0], players[1], random_positions=random_positions)
          # ... resto de los atributos y métodos ...
  ```
- **Uso de la salida**: Usada con modificaciones. Después de aplicar el cambio, los tests fallaron debido al cambio de nombres de atributos, lo que requirió correcciones adicionales en los archivos de test.
- **Referencia a los archivos finales**: `core/game.py`, `tests/test_game_logic.py`, `tests/test_player.py`.

---
