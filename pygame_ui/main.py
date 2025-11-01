import pygame 
import sys
import math
import os

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.game import Game
from core.player import Player
from core.ai import AIPlayer
from core.checkers import Checkers

# --- Constants ---
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 680
BACKGROUND_COLOR = (0, 40, 0) # Dark Green
BOARD_COLOR = (139, 69, 19)   # Saddle Brown
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
POINT_COLOR_1 = (205, 133, 63) # Peru
POINT_COLOR_2 = (160, 82, 45)   # Sienna
HUD_COLOR = (20, 20, 20)
FONT_COLOR = (230, 230, 230)

# Board layout
BEAR_OFF_WIDTH = 80
BOARD_LEFT = BEAR_OFF_WIDTH + 20
BOARD_TOP = 70
BOARD_WIDTH = 700
BOARD_HEIGHT = 540
POINT_WIDTH = BOARD_WIDTH / 13
POINT_HEIGHT = BOARD_HEIGHT / 2.5
CHECKER_RADIUS = int(POINT_WIDTH / 2.2)

class BackgammonUI:
    def __init__(self, screen):
        self.screen = screen
        self.game = None
        self.font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 36)
        self.game_state = "menu"
        self.player_names = ["Player 1", "AI Player"]
        self.active_input = None
        self.game_mode = None
        self.selected_checker_point = None
        self.possible_moves = []
        self.menu_buttons = {
            "h_vs_h": pygame.Rect(SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2 - 100, 300, 80),
            "h_vs_ai": pygame.Rect(SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2, 300, 80),
            "exit": pygame.Rect(SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2 + 100, 300, 80)
        }
        self.ingame_buttons = {
            "roll_dice": pygame.Rect(BOARD_LEFT + BOARD_WIDTH + 20, SCREEN_HEIGHT - 240, 200, 50),
            "exit": pygame.Rect(BOARD_LEFT + BOARD_WIDTH + 20, SCREEN_HEIGHT - 170, 200, 50)
        }
        self.game_over_buttons = {
            "play_again": pygame.Rect(SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2, 300, 80),
            "main_menu": pygame.Rect(SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2 + 100, 300, 80)
        }
        self.initial_roll_button = pygame.Rect(SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT - 120, 300, 60)
        self.dice_rolled = False
        self.message = None
        self.message_timer = 0
        self.ai_turn_timer = None

    def draw_board(self):
        pygame.draw.rect(self.screen, BOARD_COLOR, (BOARD_LEFT, BOARD_TOP, BOARD_WIDTH, BOARD_HEIGHT))
        bar_x = BOARD_LEFT + 6 * POINT_WIDTH
        pygame.draw.rect(self.screen, (200, 0, 0), (bar_x, BOARD_TOP, POINT_WIDTH, BOARD_HEIGHT))
        for i in range(24):
            color = POINT_COLOR_1 if (i % 2) != 0 else POINT_COLOR_2
            if 0 <= i <= 5: col = 12 - i
            elif 6 <= i <= 11: col = 11 - i
            elif 12 <= i <= 17: col = i - 12
            else: col = i - 11
            x_base = BOARD_LEFT + (col + 0.5) * POINT_WIDTH
            if i >= 12:
                p1, p2, p3 = (x_base - POINT_WIDTH / 2, BOARD_TOP), (x_base + POINT_WIDTH / 2, BOARD_TOP), (x_base, BOARD_TOP + POINT_HEIGHT)
            else:
                p1, p2, p3 = (x_base - POINT_WIDTH / 2, BOARD_TOP + BOARD_HEIGHT), (x_base + POINT_WIDTH / 2, BOARD_TOP + BOARD_HEIGHT), (x_base, BOARD_TOP + BOARD_HEIGHT - POINT_HEIGHT)
            pygame.draw.polygon(self.screen, color, [p1, p2, p3])

    def draw_checkers(self):
        if not self.game: return
        points = self.game.board.get_points()
        for i, point in enumerate(points):
            num_checkers = len(point)
            for j, checker in enumerate(point[:5]): # Limit drawing to 5 checkers
                player = checker.get_owner()
                color = WHITE if player.get_color() == 'white' else BLACK
                x, y = self.get_checker_position(i, j)
                pygame.draw.circle(self.screen, color, (int(x), int(y)), CHECKER_RADIUS)
            
            if num_checkers > 5:
                # Position counter on the 5th checker
                x, y = self.get_checker_position(i, 4) 
                count_font = pygame.font.Font(None, 24)
                count_text = count_font.render(str(num_checkers), True, (255, 200, 0))
                self.screen.blit(count_text, (x - count_text.get_width()/2, y - count_text.get_height()/2))
            
            bar = self.game.board.get_bar()
            bar_x = BOARD_LEFT + 6.5 * POINT_WIDTH
            for player, checkers in bar.items():
                for k, checker in enumerate(checkers):
                    color = WHITE if player.get_color() == 'white' else BLACK
                    y_pos = (BOARD_TOP + BOARD_HEIGHT / 4) + (k * CHECKER_RADIUS * 2) if player.get_color() == 'white' else \
                            (BOARD_TOP + 3 * BOARD_HEIGHT / 4) - (k * CHECKER_RADIUS * 2)
                    pygame.draw.circle(self.screen, color, (int(bar_x), int(y_pos)), CHECKER_RADIUS)

    def get_checker_position(self, point_index, stack_index):
        is_top = point_index >= 12
        
        if 0 <= point_index <= 5: col = 12 - point_index
        elif 6 <= point_index <= 11: col = 11 - point_index
        elif 12 <= point_index <= 17: col = point_index - 12
        else: col = point_index - 11
            
        x = BOARD_LEFT + (col + 0.5) * POINT_WIDTH

        y_offset = CHECKER_RADIUS + (stack_index * (CHECKER_RADIUS * 2))
        if stack_index >= 5: # Ensure checkers don't go off board
             y_offset = CHECKER_RADIUS + (4 * (CHECKER_RADIUS * 2))

        if is_top:
            y = BOARD_TOP + y_offset
        else:
            y = BOARD_TOP + BOARD_HEIGHT - y_offset
            
        return x, y

    def draw_hud(self):
        hud_x = BOARD_LEFT + BOARD_WIDTH + 10
        hud_width = SCREEN_WIDTH - hud_x - 10
        pygame.draw.rect(self.screen, HUD_COLOR, (hud_x, 0, hud_width, SCREEN_HEIGHT))

        if not self.game: return

        title_font = pygame.font.Font(None, 40)
        title_text = title_font.render("Backgammon", True, FONT_COLOR)
        self.screen.blit(title_text, (hud_x + hud_width/2 - title_text.get_width()/2, 20))

        player = self.game.get_current_player()
        turn_font = pygame.font.Font(None, 38)
        turn_text = turn_font.render(f"Turn:", True, (200, 200, 200))
        player_text = turn_font.render(player.get_name(), True, FONT_COLOR)
        self.screen.blit(turn_text, (hud_x + hud_width/2 - turn_text.get_width()/2, 130))
        self.screen.blit(player_text, (hud_x + hud_width/2 - player_text.get_width()/2, 170))
        
        self.draw_message() # Draw any active message
        
        dice = self.game.dice.get_values()
        dice_y = 240
        dice_info_font = pygame.font.Font(None, 34)
        if not self.dice_rolled:
            dice_text_str = "Roll the dice!"
            dice_text = dice_info_font.render(dice_text_str, True, FONT_COLOR)
            self.screen.blit(dice_text, (hud_x + hud_width/2 - dice_text.get_width()/2, dice_y))
        else:
            self.draw_dice(dice, hud_x + hud_width/2, dice_y + 40)

        for key, rect in self.ingame_buttons.items():
            pygame.draw.rect(self.screen, POINT_COLOR_1, rect, border_radius=8)
            text_str = key.replace("_", " ").title()
            text = self.small_font.render(text_str, True, FONT_COLOR)
            self.screen.blit(text, (rect.centerx - text.get_width()/2, rect.centery - text.get_height()/2))

    def draw_dice(self, dice, center_x, center_y):
        die_size = 50
        pip_radius = 5
        die_padding = 15

        pip_positions = {
            1: [(0.5, 0.5)],
            2: [(0.25, 0.25), (0.75, 0.75)],
            3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
            4: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)],
            5: [(0.25, 0.25), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.75, 0.75)],
            6: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.5), (0.75, 0.5), (0.25, 0.75), (0.75, 0.75)]
        }

        if len(dice) == 4:
            x1 = center_x - die_size - die_padding / 2
            x2 = center_x + die_padding / 2
            y1 = center_y - die_size - die_padding / 2
            y2 = center_y + die_padding / 2
            positions = [ (x1, y1), (x2, y1), (x1, y2), (x2, y2) ]
            
            for i, die_value in enumerate(dice):
                die_x, die_y = positions[i]
                die_rect = pygame.Rect(die_x, die_y, die_size, die_size)
                pygame.draw.rect(self.screen, WHITE, die_rect, border_radius=5)

                for pos in pip_positions[die_value]:
                    pip_x = die_x + pos[0] * die_size
                    pip_y = die_y + pos[1] * die_size
                    pygame.draw.circle(self.screen, BLACK, (int(pip_x), int(pip_y)), pip_radius)
        else:
            total_width = len(dice) * die_size + (len(dice) - 1) * die_padding
            start_x = center_x - total_width / 2
            for i, die_value in enumerate(dice):
                die_x = start_x + i * (die_size + die_padding)
                die_rect = pygame.Rect(die_x, center_y, die_size, die_size)
                pygame.draw.rect(self.screen, WHITE, die_rect, border_radius=5)

                for pos in pip_positions[die_value]:
                    pip_x = die_x + pos[0] * die_size
                    pip_y = center_y + pos[1] * die_size
                    pygame.draw.circle(self.screen, BLACK, (int(pip_x), int(pip_y)), pip_radius)
    
    def handle_menu_click(self, pos):
        if self.menu_buttons["h_vs_h"].collidepoint(pos):
            self.game_mode = "h_vs_h"
            self.game_state = "enter_names"
            self.player_names = ["Player 1", "Player 2"]
        elif self.menu_buttons["h_vs_ai"].collidepoint(pos):
            self.game_mode = "h_vs_ai"
            self.game_state = "enter_names"
            self.player_names = ["Player 1", "AI Player"]
        elif self.menu_buttons["exit"].collidepoint(pos):
            pygame.quit()
            sys.exit()

    def handle_click(self, pos):
        if self.game_state == "game_over":
            if self.game_over_buttons["play_again"].collidepoint(pos):
                if self.game_mode == "h_vs_h":
                    p1 = Player(self.game.players[0].get_name(), "white")
                    p2 = Player(self.game.players[1].get_name(), "black")
                else:
                    p1 = Player(self.game.players[0].get_name(), "white")
                    p2 = AIPlayer(self.game.players[1].get_name(), "black")
                self.game = Game([p1, p2])
                self.game_state = "initial_roll"
            elif self.game_over_buttons["main_menu"].collidepoint(pos):
                self.__init__(self.screen)
            return

        if self.ingame_buttons["exit"].collidepoint(pos):
            self.game_state = "menu"
            self.game = None
            return
        
        if self.ingame_buttons["roll_dice"].collidepoint(pos) and not self.dice_rolled:
            # Button is now only for human players
            if isinstance(self.game.get_current_player(), AIPlayer):
                return

            self.game.roll_dice()
            self.dice_rolled = True
            current_player = self.game.get_current_player()
            if not self.game.has_possible_moves(current_player):
                self.message = "No Tienes Movimientos Posibles"
                self.message_timer = pygame.time.get_ticks()
            return

        if not self.dice_rolled:
            return

        clicked_point = self.get_point_from_pos(pos)
        
        player = self.game.get_current_player()
        
        if self.game.board.get_bar().get(player):
            if self.selected_checker_point == 'bar':
                self.handle_move('bar', clicked_point)
            elif clicked_point == 'bar':
                self.handle_selection('bar')
            return

        if self.selected_checker_point is not None:
            self.handle_move(self.selected_checker_point, clicked_point)
        elif isinstance(clicked_point, int):
            self.handle_selection(clicked_point)

    def handle_selection(self, point_index):
        player = self.game.get_current_player()
        dice = self.game.dice.get_values()
        
        if point_index == 'bar':
            if self.game.board.get_bar().get(player):
                self.selected_checker_point = 'bar'
                self.possible_moves = self.game.board.get_possible_moves_for_checker('bar', player, dice)
        else:
            point_content = self.game.board.get_point(point_index)
            if point_content and point_content[0].get_owner() == player:
                self.selected_checker_point = point_index
                self.possible_moves = self.game.board.get_possible_moves_for_checker(point_index, player, dice)
            else:
                self.selected_checker_point = None
                self.possible_moves = []

    def handle_move(self, from_point, to_point):
        if to_point in self.possible_moves:
            try:
                # The core game logic now handles move validation and execution
                self.game.move(from_point, to_point)
            except (ValueError, IndexError) as e:
                print(f"Move Error: {e}")

            # After a successful move, check the game state
            current_player = self.game.get_current_player()
            
            # If there are no dice left, the turn is over.
            if not self.game.dice.get_values():
                self.game.switch_player()
                self.dice_rolled = False
            # If there ARE dice left, but no possible moves, show the message.
            # The main loop will handle the turn switch after the message timer.
            elif not self.game.has_possible_moves(current_player):
                self.message = "No Tienes Movimientos Posibles"
                self.message_timer = pygame.time.get_ticks()
        
        # Reset selection regardless of whether the move was successful or not
        self.selected_checker_point = None
        self.possible_moves = []


    def get_point_from_pos(self, pos):
        x, y = pos

        if 10 <= x < 10 + BEAR_OFF_WIDTH:
            player = self.game.get_current_player()
            p1_rect = pygame.Rect(10, BOARD_TOP, BEAR_OFF_WIDTH, BOARD_HEIGHT / 2 - 10)
            p2_rect = pygame.Rect(10, BOARD_TOP + BOARD_HEIGHT / 2 + 10, BEAR_OFF_WIDTH, BOARD_HEIGHT / 2 - 10)
            
            if (player.get_color() == 'white' and p1_rect.collidepoint(pos)) or \
               (player.get_color() == 'black' and p2_rect.collidepoint(pos)):
                return "off"

        if not (BOARD_LEFT <= x <= BOARD_LEFT + BOARD_WIDTH and BOARD_TOP <= y <= BOARD_TOP + BOARD_HEIGHT):
            return None
        
        bar_x_start = BOARD_LEFT + 6 * POINT_WIDTH
        bar_x_end = bar_x_start + POINT_WIDTH
        
        if bar_x_start <= x <= bar_x_end:
            return 'bar'

        if x < bar_x_start:
            col = int((x - BOARD_LEFT) / POINT_WIDTH)
            point = 12 + col if y < BOARD_TOP + BOARD_HEIGHT / 2 else 11 - col
        else:
            col = int((x - bar_x_end) / POINT_WIDTH)
            point = 18 + col if y < BOARD_TOP + BOARD_HEIGHT / 2 else 5 - col
            
        return point

    def draw_possible_moves(self):
        if self.selected_checker_point is not None and isinstance(self.selected_checker_point, int):
            num_checkers = len(self.game.board.get_point(self.selected_checker_point))
            if num_checkers > 0:
                x, y = self.get_checker_position(self.selected_checker_point, num_checkers - 1)
                pygame.draw.circle(self.screen, (0, 255, 0), (int(x), int(y)), CHECKER_RADIUS + 3, 3)

        for move in self.possible_moves:
            if move == 'off':
                player = self.game.get_current_player()
                rect = pygame.Rect(10, BOARD_TOP, BEAR_OFF_WIDTH, BOARD_HEIGHT / 2 - 10) if player.get_color() == 'white' else \
                       pygame.Rect(10, BOARD_TOP + BOARD_HEIGHT / 2 + 10, BEAR_OFF_WIDTH, BOARD_HEIGHT / 2 - 10)
                
                highlight_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
                highlight_surf.fill((0, 255, 0, 100))
                self.screen.blit(highlight_surf, rect.topleft)
            elif isinstance(move, int):
                num_checkers_dest = len(self.game.board.get_point(move))
                x, y = self.get_checker_position(move, num_checkers_dest)
                
                highlight_surf = pygame.Surface((CHECKER_RADIUS * 2, CHECKER_RADIUS * 2), pygame.SRCALPHA)
                pygame.draw.circle(highlight_surf, (0, 255, 0, 120), (CHECKER_RADIUS, CHECKER_RADIUS), CHECKER_RADIUS)
                self.screen.blit(highlight_surf, (int(x - CHECKER_RADIUS), int(y - CHECKER_RADIUS)))
                
    def draw_main_menu(self):
        self.screen.fill(HUD_COLOR)
        title_text = self.font.render("Backgammon", True, FONT_COLOR)
        self.screen.blit(title_text, (SCREEN_WIDTH/2 - title_text.get_width()/2, SCREEN_HEIGHT/4))

        for key, rect in self.menu_buttons.items():
            pygame.draw.rect(self.screen, POINT_COLOR_1, rect, border_radius=8)
            text_str = key.replace("_", " ").title()
            text = self.small_font.render(text_str, True, FONT_COLOR)
            self.screen.blit(text, (rect.centerx - text.get_width()/2, rect.centery - text.get_height()/2))

    def draw_enter_names_screen(self):
        self.screen.fill(HUD_COLOR)
        title_text = self.font.render("Enter Player Names", True, FONT_COLOR)
        self.screen.blit(title_text, (SCREEN_WIDTH/2 - title_text.get_width()/2, 100))

        self.input_rects = []
        num_players = 1 if self.game_mode == "h_vs_ai" else 2
        for i in range(num_players):
            rect = pygame.Rect(SCREEN_WIDTH/2 - 150, 200 + i * 100, 300, 50)
            self.input_rects.append(rect)
            pygame.draw.rect(self.screen, WHITE, rect, 2)
            name_text = self.small_font.render(self.player_names[i], True, FONT_COLOR)
            self.screen.blit(name_text, (rect.x + 10, rect.y + 10))

        self.start_game_rect = pygame.Rect(SCREEN_WIDTH/2 - 100, 400, 200, 50)
        pygame.draw.rect(self.screen, POINT_COLOR_1, self.start_game_rect)
        start_text = self.small_font.render("Start Game", True, FONT_COLOR)
        self.screen.blit(start_text, (self.start_game_rect.centerx - start_text.get_width()/2, self.start_game_rect.centery - start_text.get_height()/2))
        
        self.exit_names_rect = pygame.Rect(SCREEN_WIDTH/2 - 100, 470, 200, 50)
        pygame.draw.rect(self.screen, POINT_COLOR_2, self.exit_names_rect)
        exit_text = self.small_font.render("Exit", True, FONT_COLOR)
        self.screen.blit(exit_text, (self.exit_names_rect.centerx - exit_text.get_width()/2, self.exit_names_rect.centery - exit_text.get_height()/2))

    def handle_names_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.input_rects):
                if rect.collidepoint(event.pos):
                    self.active_input = i
                    return
            self.active_input = None

            if self.start_game_rect.collidepoint(event.pos):
                if self.game_mode == "h_vs_h":
                    p1 = Player(self.player_names[0], "white")
                    p2 = Player(self.player_names[1], "black")
                else:
                    p1 = Player(self.player_names[0], "white")
                    p2 = AIPlayer(self.player_names[1], "black")
                self.game = Game([p1, p2])
                self.game_state = "initial_roll"
            elif self.exit_names_rect.collidepoint(event.pos):
                self.game_state = "menu"

        if event.type == pygame.KEYDOWN and self.active_input is not None:
            current_name = self.player_names[self.active_input]
            if event.key == pygame.K_BACKSPACE:
                self.player_names[self.active_input] = current_name[:-1]
            else:
                self.player_names[self.active_input] += event.unicode
    
    def draw_bear_off_area(self):
        label_font = pygame.font.Font(None, 24)
        
        p1_rect = pygame.Rect(10, BOARD_TOP, BEAR_OFF_WIDTH, BOARD_HEIGHT / 2 - 10)
        pygame.draw.rect(self.screen, (40, 40, 40), p1_rect)
        if self.game:
            p1_off = self.game.board.get_off_board_count(self.game.players[0])
            p1_text = self.font.render(str(p1_off), True, WHITE)
            self.screen.blit(p1_text, (p1_rect.centerx - p1_text.get_width()/2, p1_rect.centery - p1_text.get_height()/2))
        p1_label = label_font.render("White Off", True, FONT_COLOR)
        self.screen.blit(p1_label, (p1_rect.centerx - p1_label.get_width()/2, p1_rect.bottom - 20))

        p2_rect = pygame.Rect(10, BOARD_TOP + BOARD_HEIGHT / 2 + 10, BEAR_OFF_WIDTH, BOARD_HEIGHT / 2 - 10)
        pygame.draw.rect(self.screen, (40, 40, 40), p2_rect)
        if self.game:
            p2_off = self.game.board.get_off_board_count(self.game.players[1])
            p2_text = self.font.render(str(p2_off), True, WHITE)
            self.screen.blit(p2_text, (p2_rect.centerx - p2_text.get_width()/2, p2_rect.centery - p2_text.get_height()/2))
        p2_label = label_font.render("Black Off", True, FONT_COLOR)
        self.screen.blit(p2_label, (p2_rect.centerx - p2_label.get_width()/2, p2_rect.bottom - 20))

    def draw_initial_roll_screen(self):
        self.screen.fill(HUD_COLOR)
        title_text = self.font.render("Initial Roll", True, FONT_COLOR)
        self.screen.blit(title_text, (SCREEN_WIDTH/2 - title_text.get_width()/2, 100))

        if self.game.initial_roll_winner:
            winner_name = self.game.initial_roll_winner.get_name()
            msg = f"{winner_name} wins the roll and goes first!"
            p1_roll = self.game.initial_rolls[0]
            p2_roll = self.game.initial_rolls[1]
            roll_text = self.small_font.render(f"{self.game.players[0].get_name()}: {p1_roll}, {self.game.players[1].get_name()}: {p2_roll}", True, FONT_COLOR)
            start_text_str = "Start Game"
        elif self.game.initial_rolls != [0, 0]:
            msg = "It's a tie! Roll again."
            roll_text = self.small_font.render(f"Both players rolled a {self.game.initial_rolls[0]}", True, FONT_COLOR)
            start_text_str = "Roll Again"
        else:
            msg = "Click the button to roll for the first turn."
            roll_text = self.small_font.render("", True, FONT_COLOR)
            start_text_str = "Roll for First Turn"

        msg_text = self.small_font.render(msg, True, FONT_COLOR)
        self.screen.blit(msg_text, (SCREEN_WIDTH/2 - msg_text.get_width()/2, 250))
        self.screen.blit(roll_text, (SCREEN_WIDTH/2 - roll_text.get_width()/2, 300))

        pygame.draw.rect(self.screen, POINT_COLOR_1, self.initial_roll_button, border_radius=8)
        start_text = self.small_font.render(start_text_str, True, FONT_COLOR)
        self.screen.blit(start_text, (self.initial_roll_button.centerx - start_text.get_width()/2, self.initial_roll_button.centery - start_text.get_height()/2))
    
    def draw_game_over_screen(self):
        self.screen.fill(HUD_COLOR)
        winner = self.game.get_winner()
        if winner:
            win_text = self.font.render(f"{winner.get_name()} wins!", True, FONT_COLOR)
            self.screen.blit(win_text, (SCREEN_WIDTH/2 - win_text.get_width()/2, SCREEN_HEIGHT/4))
        
        for key, rect in self.game_over_buttons.items():
            pygame.draw.rect(self.screen, POINT_COLOR_1, rect, border_radius=8)
            text_str = key.replace("_", " ").title()
            text = self.small_font.render(text_str, True, FONT_COLOR)
            self.screen.blit(text, (rect.centerx - text.get_width()/2, rect.centery - text.get_height()/2))

    def draw_message(self):
        if self.message:
            # Create a semi-transparent surface for the background
            overlay = pygame.Surface((500, 100), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) # Black with alpha transparency

            # Render the text
            msg_font = pygame.font.Font(None, 42)
            msg_text = msg_font.render(self.message, True, (255, 255, 150)) # Light Yellow
            text_rect = msg_text.get_rect(center=(250, 50))

            # Blit the text onto the overlay
            overlay.blit(msg_text, text_rect)

            # Blit the overlay onto the center of the game board
            board_center_x = BOARD_LEFT + BOARD_WIDTH / 2
            board_center_y = BOARD_TOP + BOARD_HEIGHT / 2
            self.screen.blit(overlay, (board_center_x - 250, board_center_y - 50))
            
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # --- Event Handling based on Game State ---
                if self.game_state == "enter_names":
                    self.handle_names_input(event)  # Handles both clicks and key presses
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if self.game_state == "menu":
                        self.handle_menu_click(pos)
                    elif self.game_state == "initial_roll":
                        if self.initial_roll_button.collidepoint(pos):
                            if self.game.initial_roll_winner:
                                self.game_state = "playing"
                                self.dice_rolled = True  # The initial roll counts as the first turn's dice
                            else:
                                self.game.determine_first_player()
                    elif self.game_state == "playing":
                        self.handle_click(pos)
                    elif self.game_state == "game_over":
                        self.handle_click(pos)  # Reuses the main click handler
            
            if self.game and self.game.is_game_over():
                self.game_state = "game_over"

            if self.message and pygame.time.get_ticks() - self.message_timer > 2000:
                self.message = None
                self.game.switch_player()
                self.dice_rolled = False
                
            current_player = self.game.get_current_player() if self.game else None
            
            # --- Automatic AI Turn Management ---
            is_ai_turn = isinstance(current_player, AIPlayer) and self.game_state == "playing"

            # --- Automatic AI Turn Management ---
            # This logic block handles the entire AI turn sequence, including the special first turn.
            if is_ai_turn:
                if not self.dice_rolled:
                    # Normal turn start: Roll dice and set timer
                    self.game.roll_dice()
                    self.dice_rolled = True
                    self.ai_turn_timer = pygame.time.get_ticks()
                    if not self.game.has_possible_moves(current_player):
                        self.message = "No Tienes Movimientos Posibles"
                        self.message_timer = pygame.time.get_ticks()
                    else:
                        self.game_state = "ai_moving"
                elif self.dice_rolled and self.game_state != "ai_moving":
                    # Special case: First turn where dice are already rolled.
                    # Start the timer and switch to moving state.
                    self.ai_turn_timer = pygame.time.get_ticks()
                    self.game_state = "ai_moving"

            if self.game_state == "ai_moving":
                if self.ai_turn_timer is not None and pygame.time.get_ticks() - self.ai_turn_timer > 1000:
                    self.game.play_ai_turn()
                    self.game.switch_player()
                    self.dice_rolled = False
                    self.game_state = "playing"
                    self.ai_turn_timer = None

            self.screen.fill(BACKGROUND_COLOR)
            if self.game_state in ["playing", "ai_rolling", "ai_moving"]:
                self.draw_board()
                self.draw_checkers()
                self.draw_possible_moves()
                self.draw_hud()
                self.draw_bear_off_area()
            elif self.game_state == "menu":
                self.draw_main_menu()
            elif self.game_state == "enter_names":
                self.draw_enter_names_screen()
            elif self.game_state == "initial_roll":
                self.draw_initial_roll_screen()
            elif self.game_state == "game_over":
                self.draw_game_over_screen()
            
            pygame.display.flip()

        pygame.quit()

def main():
    os.environ['SDL_AUDIODRIVER'] = 'dsp'
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Backgammon")
    
    ui = BackgammonUI(screen)
    ui.run()

if __name__ == "__main__":
    main()