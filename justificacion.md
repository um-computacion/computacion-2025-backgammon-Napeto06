# 🎲 Justificación del Diseño - Backgammon en Python  

Este documento justifica las decisiones de diseño del proyecto **Backgammon**, siguiendo principios SOLID y OOP. Se actualiza a lo largo del desarrollo para reflejar evolución.  

**Autor**: Ignacio Quercetti  
**Versión**: 1.0.0  
**Fecha**: Octubre 2025  

---

## 📋 Resumen del Diseño General  

El proyecto implementa Backgammon con **encapsulación estricta**, modularidad y extensibilidad. Separa lógica core de UI, usa TDD para tests, y soporta CLI y Pygame. Prioriza mantenibilidad y cumplimiento de reglas tradicionales.  

---

## 🏗️ Justificación de las Clases Elegidas  

### Clases Principales y Responsabilidades  

- **Player** 🎯: Gestiona identidad (nombre, color). Elegida para separar jugador de tablero.  
- **Checkers** ⚫: Representa fichas individuales. Elegida para rastrear propiedad y movimientos.  
- **Board** 📋: Controla estado del tablero. Elegida como núcleo central para reglas.  
- **AIPlayer** 🤖: Maneja IA. Elegida para encapsular decisiones, extensible a algoritmos avanzados.  
- **Game** (opcional) 🎮: Coordina flujo. Elegida para separar lógica de juego de estado.  

Cumple **SRP** (responsabilidad única) para claridad.  

---

## 🔧 Justificación de Atributos  

### Atributos Elegidos y Razones  

- **Player**: `__name__` (str), `__color__` (str). Identifican jugador; `__color__` define reglas. Encapsulados para integridad.  
- **Checkers**: `__owner__` (Player). Rastrea propiedad; esencial para validaciones.  
- **Board**: `__points__` (list), `__bar__` (dict), etc. Representan estado completo. Encapsulados para prevenir errores.  
- **AIPlayer**: `__board__`, `__player__`. Acceden a estado; encapsulados para aislamiento.  

Usa prefijo `__` para **ocultamiento de información**.  

---

## 🎯 Decisiones de Diseño Relevantes  

- **Encapsulación Estricta** 🔒: Getters/setters para acceso controlado.  
- **TYPE_CHECKING** 📦: Evita dependencias circulares.  
- **Separación de Concerns** 🧩: Core, tests, UI separados.  
- **IA Simple** 🤖: Evalúa por fichas en home; extensible.  
- **Random Positions** 🎲: Simula variabilidad.  
- **CLI y GUI** 🖥️: CLI para testing, Pygame para visual.  

---

## ⚠️ Excepciones y Manejo de Errores  

### Excepciones Definidas  

- **ValueError**: Para movimientos inválidos (e.g., bloqueado). Indica errores lógicos.  
- **AttributeError**: Evitado con getters.  
- **KeyboardInterrupt**: Para salir en CLI.  

### Manejo  

- Validaciones previenen errores.  
- Try-except en UI para entradas inválidas.  
- Excepciones custom opcionales (e.g., `InvalidMoveError`).  

---

## 🧪 Estrategias de Testing y Cobertura  

### Qué se Probó y Por Qué  

- **Unitarios**: Cubren clases (`Player`, `Board`, etc.). Verifican inicialización, movimientos, edge cases.  
- **Mocks**: Aislan pruebas (e.g., en `test_ai.py`).  
- **Cobertura**: >90%, con TDD.  

Razones: Garantiza robustez, facilita cambios, detecta regresiones. Ejecuta con `pytest`.  

---

## 📚 Referencias a Requisitos SOLID  

- **S (Única)**: Cada clase una tarea.  
- **O (Abierto/Cerrado)**: Extensible sin modificar.  
- **L (Liskov)**: Subclases respetan contratos.  
- **I (Interfaces)**: Getters mínimos.  
- **D (Dependencias)**: Inyección (e.g., Board recibe Players).  

---

## 📊 Anexos: Diagramas UML  

### Diagrama de Clases (Texto)
+----------------+     +-----------------+
|     Player     |     |    Checkers     |
+----------------+     +-----------------+
| - __name__: str|     | - __owner__: Player |
| - __color__: str|     +-----------------+
+----------------+     | + get_owner()   |
| + get_name()   |     +-----------------+
| + get_color()  |
| + __eq__()     |
| + __hash__()   |
+----------------+

+----------------+     +-----------------+
|     Board      |     |    AIPlayer     |
+----------------+     +-----------------+
| - __points__: list|  | - __board__: Board |
| - __bar__: dict |  | - __player__: Player|
| - __current_player__| +-----------------+
| ...             |  | + play_turn()    |
+----------------+  | + _evaluate_board()|
| + move_piece()  |  +-----------------+
| + is_valid_move()|
| + get_point()   |
+----------------+

Relaciones:
- Board contiene list[Checkers] en __points__
- Checkers tiene 1 Player como __owner__
- AIPlayer usa Board y Player

---

## 📜 Notas Adicionales  

- Evolución versionada en Git.  
- Consulta código para detalles.  

¡Diseño sólido! 🎉
