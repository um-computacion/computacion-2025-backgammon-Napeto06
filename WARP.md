# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

Project overview
- Simplified Backgammon game implemented in Python for two players, with a minimal CLI and basic AI.
- Python 3.10 is used in CI; use the same locally for consistency.

Environment setup
- Create and activate a virtual environment, then install dependencies.

```bash path=null start=null
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
# Optional (to reproduce CI lint step locally):
pip install pylint
```

Common commands
- Test discovery uses the builtin unittest runner. Coverage is collected with coverage.py.

Run all tests
```bash path=null start=null
python -m unittest discover -s tests -p "test*.py"
```

Run all tests with coverage and generate reports
```bash path=null start=null
coverage run -m unittest discover -s tests -p "test*.py"
coverage report -m
coverage xml -o cobertura.xml
```

Run a single test file
```bash path=null start=null
python -m unittest tests/test_board.py
```

Run a single test case or method
```bash path=null start=null
# Module path syntax
python -m unittest tests.test_board.TestBoard
python -m unittest tests.test_board.TestBoard.test_init
```

Lint (optional; mirrors CI behavior)
- CI runs pylint over all Python files (using a .pylintrc if present). Locally, either mirror CI’s find/xargs call or lint packages directly.
```bash path=null start=null
# Mirror CI (will ignore missing .pylintrc gracefully):
find . -name "*.py" -not -path "./.venv/*" -not -path "./venv/*" | xargs pylint --rcfile=.pylintrc || true
# Or lint packages explicitly:
pylint core cli tests || true
```

Run the CLI (interactive)
- The CLI is a simple prompt loop.
```bash path=null start=null
python -m cli.cli
# or
python cli/cli.py
```

Continuous Integration (reference)
- CI workflow at .github/workflows/ci.yml performs:
  - Python 3.10 setup
  - pip install -r requirements.txt
  - coverage run -m unittest discover -s tests -p "test*.py"
  - coverage xml -o cobertura.xml and coverage report -m > coverage_report.txt
  - pylint report generation (optional; .pylintrc if present)
  - REPORTS.md is generated aggregating coverage and pylint outputs

High-level architecture
- Packages
  - core/
    - player.py: Player entity with name and color; equality/hash by identity attributes.
    - checkers.py: Checker piece tied to a Player.
    - dice.py: roll_dice() returns [d1, d2] or [d, d, d, d] on doubles.
    - board.py: Central game state and rules.
      - Maintains points (24), bar per player, off_board counts, current player, winner.
      - Validates moves (direction by color, bar priority, blocking rules, hits, bear-off).
      - Applies moves, handling hits to bar and bearing off; detects game end.
      - Integrates a basic AIPlayer instance (self.ai) tied to the board and second player.
      - Provides helper methods: get_point, roll_dice, switch_player, is_game_over, get_winner, display.
    - ai.py: AIPlayer with a very simple move heuristic.
      - Iterates candidate moves; uses board.is_valid_move and board.move_piece to play a turn.
      - Includes simple sequence scoring helpers (not fully integrated yet).
    - game.py: Game orchestration loop (human vs AI) using Board; prints state each turn.
      - Note: If invoking directly, ensure AI import path resolves to core.ai.AIPlayer.
  - cli/
    - cli.py: Minimal interactive menu loop for starting a game (demonstrative; not wired to core.Game’s loop).
- Tests (unittest)
  - tests/ test*.py modules cover dice, checkers, player, AI behaviors, and board rules/integration.
  - Discovery pattern is test*.py; files not matching this (e.g., a misspelled name) will be skipped by default.

Notable integration points
- Board owns and configures an AIPlayer instance (board.ai) tied to the board and to player2 by default.
- Game orchestrates play on a Board, alternating human and AI turns; CLI is a separate, simplified entry point.
- CI targets unittest + coverage; pylint reporting is best-effort and does not fail the build.
