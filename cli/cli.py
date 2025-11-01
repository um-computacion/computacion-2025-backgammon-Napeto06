import random
import sys
import os
from typing import List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.board import Board
from core.player import Player
from core.ai import AIPlayer


def _candidate_from_points(board: Board, player: Player) -> List[int]:
    """Return candidate from_points considering bar priority and ownership."""
    # Bar priority: if player has checkers on bar, must enter from bar
    if len(board.get_bar()[player]) > 0:  # Usa getter
        return [-1] if player.get_color() == "white" else [24]  # Usa getter
    # Otherwise, any point with at least one checker belonging to the player
    points = []
    for i in range(24):
        stack = board.get_point(i)  # Usa getter
        if stack and stack[-1].get_owner() == player:  # Usa getter
            points.append(i)
    return points


def _valid_from_points_for_die(board: Board, player: Player, die: int) -> List[int]:
    """Filter candidate points to those that produce a valid move for this die."""
    return [
        fp
        for fp in _candidate_from_points(board, player)
        if board.is_valid_move(fp, die, player)
    ]


def _input_from_point(
    prompt: str, valid_choices: List[int], player: Player
) -> int | None:
    """Prompt the user to choose a from_point, allowing 'q' to quit or 'pass' to skip.

    Accepts aliases:
      - 'bar' → -1 for white, 24 for black
    Returns None if user chooses to pass.
    """
    while True:
        raw = input(prompt).strip().lower()
        if raw in {"q", "quit", "exit"}:
            raise KeyboardInterrupt
        if raw in {"p", "pass"}:
            return None
        if raw == "bar":
            choice = -1 if player.get_color() == "white" else 24  # Usa getter
        else:
            try:
                choice = int(raw)
            except ValueError:
                print("Invalid input. Enter an integer index, 'bar', or 'pass'.")
                continue
        if choice in valid_choices:
            return choice
        print(f"Invalid point. Valid options: {sorted(valid_choices)} (or 'pass').")


def _play_human_turn(board: Board, player: Player) -> None:
    print(f"\nTurno de {player.get_name()} ({player.get_color()}).")
    dice = board.roll_dice()
    print(f"Dados: {dice}")

    for die in dice:
        valid_froms = [
            fp
            for fp in range(24)
            if board.get_point(fp) and board.get_point(fp)[0].get_owner() == player
        ]
        if len(board.get_bar()[player]) > 0:
            valid_froms = ["bar"]

        if not any(board.is_valid_move(fp, die, player) for fp in valid_froms):
            print(f"- Sin movimientos válidos para dado {die}.")
            continue

        while True:
            try:
                from_point_str = input(
                    f"Elige punto de origen para mover con dado {die} (o 'pass'): "
                )
                if from_point_str.lower() == "pass":
                    break
                
                from_point = (
                    "bar"
                    if from_point_str.lower() == "bar"
                    else int(from_point_str)
                )

                if board.is_valid_move(from_point, die, player):
                    board.move_piece(from_point, die, player)
                    print(f"Movido desde {from_point_str} con {die}.")
                    break
                else:
                    print("Movimiento inválido. Intenta de nuevo.")
            except ValueError:
                print("Entrada inválida. Ingresa un número de punto o 'bar'.")
            except IndexError:
                print("Número de punto fuera de rango.")
    board.display()


def _can_bear_off(board: Board, player: Player, die: int) -> bool:
    """Chequea si el player puede hacer bear-off con el dado."""
    home_points = (
        range(0, 6) if player.get_color() == "white" else range(18, 24)
    )  # Usa getter
    return any(
        len(board.get_point(p)) > 0
        and board.is_valid_move(p, die, player)  # Usa getter
        for p in home_points
    )


def _parse_from_point(choice: str, player: Player) -> int:
    """Parsea la entrada del usuario para from_point."""
    if choice == "bar":
        return -1 if player.get_color() == "white" else 24  # Usa getter
    return int(choice)


def _play_ai_turn(board: Board, player: Player) -> None:
    print(f"\nTurno de {player.get_name()} ({player.get_color()}).")
    dice = board.roll_dice()
    print(f"Dados: {dice}")

    moves = player.choose_moves(board, dice)
    
    if not moves:
        print("La IA no tiene movimientos.")
    else:
        for from_point, to_point in moves:
            try:
                # We need to calculate the die used for the move to call `move_piece`
                if to_point == "off":
                    required_die = (
                        (from_point + 1)
                        if player.get_color() == "white"
                        else (24 - from_point)
                    )
                    die = next(
                        (d for d in dice if d >= required_die), max(dice)
                    )
                elif from_point == "bar":
                    die = (
                        (24 - to_point)
                        if player.get_color() == "white"
                        else (to_point + 1)
                    )
                else:
                    die = abs(to_point - from_point)

                board.move_piece(from_point, die, player)
                from_display = "bar" if from_point == "bar" else from_point
                print(f"IA movió desde {from_display} a {to_point} con dado {die}.")
            except ValueError as e:
                print(f"La IA intentó un movimiento inválido: {e}")
    
    board.display()


def _choose_mode() -> str:
    print("\nBienvenido a Backgammon!")
    print("Selecciona el modo de juego:")
    print("1. Humano vs IA")
    print("2. Humano vs Humano")
    print("3. Salir")
    while True:
        choice = input("Ingresa 1, 2 o 3: ").strip()
        if choice in {"1", "2", "3"}:
            return choice
        print("Opción inválida.")


def main() -> None:
    try:
        choice = _choose_mode()
        if choice == "3":
            print("Saliendo. ¡Hasta luego!")
            return

        if choice == "1":
            name = input("Nombre del jugador humano: ").strip() or "Humano"
            human = Player(name, "white")
            ai_player = AIPlayer("Computer", "black")
            board = Board(human, ai_player)
            print(
                f"Juego iniciado: Humano ({human.get_name()}) vs IA ({ai_player.get_name()})."
            )
            play_game(board, human, ai_player)
        elif choice == "2":
            # Humano vs Humano
            name1 = input("Nombre del Jugador 1 (blanco): ").strip() or "Jugador 1"
            name2 = input("Nombre del Jugador 2 (negro): ").strip() or "Jugador 2"
            p1 = Player(name1, "white")
            p2 = Player(name2, "black")
            board = Board(p1, p2)
            print("Juego iniciado: Humano vs Humano.")
            play_game(board, p1, p2)

        winner = board.get_winner() if board.is_game_over() else None
        if winner:
            print(f"\n¡{winner.get_name()} ({winner.get_color()}) gana!")  # Usa getters
        else:
            print("\nJuego terminado.")
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")


def play_game(board, p1, p2):
    while not board.is_game_over():
        current_player = board.get_current_player()
        print(f"Turno: {current_player.get_name()}")
        board.display()

        if isinstance(current_player, AIPlayer):
            _play_ai_turn(board, current_player)
        else:
            _play_human_turn(board, current_player)

        board.switch_player()

    winner = board.get_winner()
    if winner:
        print(f"¡{winner.get_name()} gana!")  # Usa getter
    else:
        print("Juego terminado.")


if __name__ == "__main__":
    main()
