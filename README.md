<!-- filepath: /home/ignacio-quercetti/Escritorio/Tp2 computacion/computacion-2025-backgammon-MQuercetti/README.md -->
# 🎲 Backgammon en Python  

Este proyecto implementa una versión completa del juego **Backgammon** en Python, siguiendo reglas tradicionales. Incluye lógica central separada de la UI, interfaz de línea de comando (CLI), interfaz gráfica con Pygame, y soporte opcional para guardado en Redis. Diseñado con principios SOLID para modularidad y mantenibilidad.  

**Autor**: Ignacio Quercetti  
**Versión**: 1.0.0  
**Fecha**: Octubre 2025  

---

## 📋 Descripción  

Backgammon es un juego de estrategia para dos jugadores. Cada uno tiene 15 fichas que deben moverse por un tablero de 24 puntos, usando dados para determinar movimientos. El objetivo es retirar todas las fichas antes que el rival.  

Este proyecto cumple con:  

- Reglas estándar (movimientos, capturas, reingresos desde barra, bear-off).  
- Separación core/UI.  
- Cobertura de tests >90%.  
- Interfaces CLI y Pygame.  

---

## 📋 Requisitos del Sistema  

- **Python**: 3.8 o superior.  
- **Dependencias**: Ver `requirements.txt` (incluye `pygame` para UI gráfica, `redis` opcional para guardado).  
- **Docker**: Recomendado para despliegue consistente (testing y juego).  
- **Sistema Operativo**: Linux/Mac/Windows (para Pygame, configura display en Linux).  

---

## 🚀 Instalación y Ejecución  

### Opción 1: Instalación Local (sin Docker)  

1. **Clona el repositorio**:  

   ```bash
   git clone <url-del-repo-oficial>
   cd computacion-2025-backgammon-MQuercetti
   ```

2. **Instala las dependencias**:  

   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta la interfaz deseada**:  

   - CLI: `python -m cli`
   - Pygame: `python -m pygame_ui`

### Opción 2: Uso de Docker  

1. **Construye la imagen**:  

   ```bash
   docker build -t backgammon .
   ```

2. **Ejecuta el contenedor**:  

   ```bash
   docker run -it --rm backgammon
   ```

---

## 🧪 Tests  

Para ejecutar los tests:  

```bash
pytest tests/
```

---

## 📂 Estructura del Proyecto  

El proyecto tiene la siguiente estructura:  

computacion-2025-backgammon-MQuercetti/
├── core/              # Lógica central (board.py, player.py, ai.py, etc.)
├── cli/               # Interfaz de línea de comando (cli.py)
├── pygame_ui/         # Interfaz gráfica (main.py, renderizado)
├── assets/            # Imágenes y sonidos para Pygame
├── tests/             # Tests unitarios (test_*.py)
├── [requirements.txt](http://_vscodecontentref_/1)   # Dependencias
├── Dockerfile         # Para Docker
├── [README.md](http://_vscodecontentref_/2)          # Este archivo
├── CHANGELOG.md       # Historial de cambios
├── JUSTIFICACION.md   # Justificación del diseño
└── prompts-*.md       # Prompts usados con IA

---

## 📜 Notas Adicionales  

- Para contribuir, sigue las guías en `CONTRIBUTING.md`.  
- Reporta issues en el repositorio de GitHub.  
- Consulta la documentación en línea para más detalles.  

¡Disfruta del juego! 🎉
