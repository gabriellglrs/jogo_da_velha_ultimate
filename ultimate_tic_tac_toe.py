import pygame
import sys
import math
import json
import random
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Tuple, List
import os


# --- Enums e Classes de Dados ---
class Player(Enum):
    X = 'X'
    O = 'O'
    EMPTY = ' '
    TIE = '-'


class GameState(Enum):
    PLAYING = "playing"
    X_WINS = "x_wins"
    O_WINS = "o_wins"
    TIE = "tie"


class GameMode(Enum):
    HUMAN_VS_HUMAN = "human_vs_human"
    HUMAN_VS_CPU = "human_vs_cpu"


@dataclass
class GameStats:
    x_wins: int = 0
    o_wins: int = 0
    ties: int = 0
    total_games: int = 0


# --- Constantes Melhoradas ---
# Cores com paleta moderna
class Colors:
    WHITE = (255, 255, 255)
    BLACK = (30, 30, 30)
    GRAY = (150, 150, 150)
    LIGHT_GRAY = (240, 240, 240)
    DARK_GRAY = (100, 100, 100)
    RED = (220, 20, 60)  # Vermelho para X
    BLUE = (30, 144, 255)  # Azul para O (humano)
    GREEN = (92, 219, 149)
    YELLOW = (255, 215, 0)
    PURPLE = (147, 112, 219)
    BACKGROUND = (248, 249, 250)
    HOVER = (200, 200, 200, 100)
    CPU_COLOR = (255, 140, 0)  # Laranja para CPU fácil/médio
    HARD_CPU_COLOR = (255, 69, 0)  # Vermelho-laranja para CPU difícil


# Configurações de tela ajustadas para layout mais largo
SCREEN_WIDTH = 1200  # Muito mais largo
SCREEN_HEIGHT = 700  # Altura reduzida
BOARD_SIZE = 600  # Tabuleiro quadrado 600x600
CELL_SIZE = BOARD_SIZE // 3  # 200 pixels cada célula principal
SUB_CELL_SIZE = CELL_SIZE // 3  # ~66.67 pixels cada subcélula

# Configurações visuais
LINE_WIDTH = 6
SUB_LINE_WIDTH = 2
SYMBOL_SIZE = int(SUB_CELL_SIZE * 0.35)
LARGE_SYMBOL_SIZE = int(CELL_SIZE * 0.3)

# Posicionamento da UI - laterais
SIDEBAR_WIDTH = 250
LEFT_SIDEBAR_X = 50
RIGHT_SIDEBAR_X = SCREEN_WIDTH - SIDEBAR_WIDTH - 10  # Adicionado 20px de espaçamento
BOARD_X = (SCREEN_WIDTH - BOARD_SIZE) // 2  # Centralizado
BOARD_Y = 50  # Margem superior

# Configurações dos botões
BUTTON_HEIGHT = 40
BUTTON_WIDTH = 200
BUTTON_MARGIN = 10

# Arquivo para salvar estatísticas
STATS_FILE = "ultimate_tictactoe_stats.json"


class CPUPlayer:
    """Classe para lógica da CPU com diferentes níveis de dificuldade."""

    def __init__(self, difficulty="medium"):
        self.difficulty = difficulty
        self.player = Player.O  # CPU sempre joga como O
        self.max_depth = 2 if difficulty == "hard" else 2

    def get_best_move(self, game):
        """Retorna a melhor jogada para a CPU."""
        if self.difficulty == "easy":
            return self._get_random_move(game)
        elif self.difficulty == "medium":
            return self._get_strategic_move(game)
        else:  # hard
            return self._get_minimax_move(game)

    def _get_random_move(self, game):
        """Jogada aleatória (fácil)."""
        valid_moves = self._get_valid_moves(game)
        if valid_moves:
            return random.choice(valid_moves)
        return None

    def _get_strategic_move(self, game):
        """Jogada estratégica (médio) - prioriza vitórias e bloqueios."""
        valid_moves = self._get_valid_moves(game)
        if not valid_moves:
            return None

        # 1. Tenta vencer o jogo principal
        for move in valid_moves:
            main_row, main_col, row, col = move
            if self._can_win_main_board(game, main_row, main_col, row, col):
                return move

        # 2. Bloqueia vitória do oponente no jogo principal
        for move in valid_moves:
            main_row, main_col, row, col = move
            if self._can_block_main_board(game, main_row, main_col, row, col):
                return move

        # 3. Tenta vencer um tabuleiro pequeno
        for move in valid_moves:
            main_row, main_col, row, col = move
            if self._can_win_small_board(game, main_row, main_col, row, col):
                return move

        # 4. Bloqueia vitória do oponente em tabuleiro pequeno
        for move in valid_moves:
            main_row, main_col, row, col = move
            if self._can_block_small_board(game, main_row, main_col, row, col):
                return move

        # 5. Joga no centro se disponível
        center_moves = [move for move in valid_moves
                        if move[2] == 1 and move[3] == 1]  # Centro da subcélula
        if center_moves:
            return random.choice(center_moves)

        # 6. Jogada aleatória
        return random.choice(valid_moves)

    def _get_minimax_move(self, game):
        """Jogada usando minimax (difícil) - implementação completa."""
        valid_moves = self._get_valid_moves(game)
        if not valid_moves:
            return None

        best_move = None
        best_score = float("-inf")

        # Cria uma cópia do estado do jogo para o minimax
        initial_game_state_copy = self._copy_game_state(game)

        for move in valid_moves:
            # Simula a jogada na cópia
            game_copy_for_move = self._copy_game_state_from_dict(initial_game_state_copy)
            main_row, main_col, row, col = move
            self._make_move_on_copy(game_copy_for_move, main_row, main_col, row, col, self.player)

            # Avalia usando minimax
            score = self._minimax(game_copy_for_move, self.max_depth - 1, False, float("-inf"), float("inf"))

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _minimax(self, game_state_dict, depth, is_maximizing, alpha, beta):
        """Algoritmo minimax com poda alfa-beta."""
        # Verifica condições de parada
        winner = self._check_game_winner(game_state_dict)
        if winner == self.player:
            return 100 + depth  # Prefere vitórias mais rápidas
        elif winner == (Player.X if self.player == Player.O else Player.O):
            return -100 - depth  # Evita derrotas mais rápidas
        elif winner == Player.TIE or depth == 0:
            return self._evaluate_position(game_state_dict)

        valid_moves = self._get_valid_moves_from_state(game_state_dict)
        if not valid_moves:
            return self._evaluate_position(game_state_dict)

        if is_maximizing:
            max_eval = float("-inf")
            for move in valid_moves:
                game_copy = self._copy_game_state_from_dict(game_state_dict)
                main_row, main_col, row, col = move
                self._make_move_on_copy(game_copy, main_row, main_col, row, col, self.player)

                eval_score = self._minimax(game_copy, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)

                if beta <= alpha:
                    break  # Poda alfa-beta
            return max_eval
        else:
            min_eval = float("inf")
            opponent = Player.X if self.player == Player.O else Player.O
            for move in valid_moves:
                game_copy = self._copy_game_state_from_dict(game_state_dict)
                main_row, main_col, row, col = move
                self._make_move_on_copy(game_copy, main_row, main_col, row, col, opponent)

                eval_score = self._minimax(game_copy, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)

                if beta <= alpha:
                    break  # Poda alfa-beta
            return min_eval

    def _evaluate_position(self, game_state_dict):
        """Avalia a posição atual do jogo."""
        score = 0

        # Avalia tabuleiro principal
        score += self._evaluate_board(game_state_dict["main_board"]) * 10

        # Avalia tabuleiros pequenos
        for i, board in enumerate(game_state_dict["boards"]):
            board_score = self._evaluate_board(board)
            score += board_score

            # Bônus por controlar tabuleiros centrais e cantos
            main_row, main_col = i // 3, i % 3
            if main_row == 1 and main_col == 1:  # Centro
                score += board_score * 0.5
            elif (main_row, main_col) in [(0, 0), (0, 2), (2, 0), (2, 2)]:  # Cantos
                score += board_score * 0.3

        return score

    def _evaluate_board(self, board):
        """Avalia um tabuleiro 3x3."""
        score = 0

        # Verifica linhas, colunas e diagonais
        lines = []
        # Linhas
        for row in board:
            lines.append(row)
        # Colunas
        for col in range(3):
            lines.append([board[row][col] for row in range(3)])
        # Diagonais
        lines.append([board[i][i] for i in range(3)])
        lines.append([board[i][2 - i] for i in range(3)])

        for line in lines:
            score += self._evaluate_line(line)

        return score

    def _evaluate_line(self, line):
        """Avalia uma linha de 3 células."""
        my_count = line.count(self.player)
        opp_count = line.count(Player.X if self.player == Player.O else Player.O)
        empty_count = line.count(Player.EMPTY)

        if my_count == 3:
            return 50
        elif my_count == 2 and empty_count == 1:
            return 10
        elif my_count == 1 and empty_count == 2:
            return 1
        elif opp_count == 3:
            return -50
        elif opp_count == 2 and empty_count == 1:
            return -10
        elif opp_count == 1 and empty_count == 2:
            return -1

        return 0

    def _copy_game_state(self, game):
        """Cria uma cópia do estado do jogo a partir do objeto UltimateTicTacToe."""
        return {
            'boards': [[[cell for cell in row] for row in board] for board in game.boards],
            'main_board': [[cell for cell in row] for row in game.main_board],
            'current_player': game.current_player,
            'game_state': game.game_state
        }

    def _copy_game_state_from_dict(self, game_state_dict):
        """Cria uma cópia do estado do jogo a partir de um dicionário de estado."""
        return {
            'boards': [[[cell for cell in row] for row in board] for board in game_state_dict['boards']],
            'main_board': [[cell for cell in row] for row in game_state_dict['main_board']],
            'current_player': game_state_dict['current_player'],
            'game_state': game_state_dict['game_state']
        }

    def _make_move_on_copy(self, game_state_dict, main_row, main_col, row, col, player):
        """Faz uma jogada na cópia do estado do jogo."""
        board_index = main_row * 3 + main_col
        game_state_dict['boards'][board_index][row][col] = player

        # Verifica vitória no tabuleiro pequeno
        winner = self._check_winner_board(game_state_dict['boards'][board_index])
        if winner:
            game_state_dict['main_board'][main_row][main_col] = winner
        elif self._is_board_full_state(game_state_dict['boards'][board_index]):
            game_state_dict['main_board'][main_row][main_col] = Player.TIE

        # Atualiza jogador atual
        game_state_dict['current_player'] = Player.O if player == Player.X else Player.X

    def _check_winner_board(self, board):
        """Verifica vencedor em um tabuleiro."""
        # Linhas
        for row in board:
            if row[0] == row[1] == row[2] and row[0] != Player.EMPTY:
                return row[0]
        # Colunas
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] and board[0][col] != Player.EMPTY:
                return board[0][col]
        # Diagonais
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != Player.EMPTY:
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != Player.EMPTY:
            return board[0][2]
        return None

    def _check_game_winner(self, game_state_dict):
        """Verifica vencedor do jogo principal."""
        return self._check_winner_board(game_state_dict['main_board'])

    def _is_board_full_state(self, board):
        """Verifica se um tabuleiro está cheio."""
        return all(cell != Player.EMPTY for row in board for cell in row)

    def _get_valid_moves_from_state(self, game_state_dict):
        """Retorna jogadas válidas de um estado do jogo."""
        valid_moves = []
        for main_row in range(3):
            for main_col in range(3):
                if game_state_dict['main_board'][main_row][main_col] == Player.EMPTY:
                    board_index = main_row * 3 + main_col
                    for row in range(3):
                        for col in range(3):
                            if game_state_dict['boards'][board_index][row][col] == Player.EMPTY:
                                valid_moves.append((main_row, main_col, row, col))
        return valid_moves

    def _get_valid_moves(self, game):
        """Retorna todas as jogadas válidas."""
        valid_moves = []
        for main_row in range(3):
            for main_col in range(3):
                if game.main_board[main_row][main_col] == Player.EMPTY:
                    board_index = game.get_board_index(main_row, main_col)
                    for row in range(3):
                        for col in range(3):
                            if game.boards[board_index][row][col] == Player.EMPTY:
                                valid_moves.append((main_row, main_col, row, col))
        return valid_moves

    def _can_win_small_board(self, game, main_row, main_col, row, col):
        """Verifica se a jogada pode vencer um tabuleiro pequeno."""
        board_index = game.get_board_index(main_row, main_col)
        board_copy = [row[:] for row in game.boards[board_index]]
        board_copy[row][col] = self.player
        return game.check_winner(board_copy) == self.player

    def _can_block_small_board(self, game, main_row, main_col, row, col):
        """Verifica se a jogada pode bloquear vitória do oponente em tabuleiro pequeno."""
        board_index = game.get_board_index(main_row, main_col)
        board_copy = [row[:] for row in game.boards[board_index]]
        opponent = Player.X if self.player == Player.O else Player.O
        board_copy[row][col] = opponent
        return game.check_winner(board_copy) == opponent

    def _can_win_main_board(self, game, main_row, main_col, row, col):
        """Verifica se a jogada pode vencer o jogo principal."""
        # Simula a jogada
        board_index = game.get_board_index(main_row, main_col)
        board_copy = [row[:] for row in game.boards[board_index]]
        board_copy[row][col] = self.player

        # Verifica se vence o tabuleiro pequeno
        if game.check_winner(board_copy) == self.player:
            # Simula vitória no tabuleiro principal
            main_board_copy = [row[:] for row in game.main_board]
            main_board_copy[main_row][main_col] = self.player
            return game.check_winner(main_board_copy) == self.player

        return False

    def _can_block_main_board(self, game, main_row, main_col, row, col):
        """Verifica se a jogada pode bloquear vitória do oponente no jogo principal."""
        board_index = game.get_board_index(main_row, main_col)
        board_copy = [row[:] for row in game.boards[board_index]]
        opponent = Player.X if self.player == Player.O else Player.O
        board_copy[row][col] = opponent

        # Verifica se oponente venceria o tabuleiro pequeno
        if game.check_winner(board_copy) == opponent:
            # Simula vitória do oponente no tabuleiro principal
            main_board_copy = [row[:] for row in game.main_board]
            main_board_copy[main_row][main_col] = opponent
            return game.check_winner(main_board_copy) == opponent

        return False


class UltimateTicTacToe:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Ultimate Tic-Tac-Toe - Layout Largo')

        # Estado do jogo
        self.boards = self.create_boards()
        self.main_board = [[Player.EMPTY for _ in range(3)] for _ in range(3)]
        self.current_player = Player.X
        self.game_state = GameState.PLAYING
        self.last_move = None
        self.hover_cell = None

        # Modo de jogo e CPU
        self.game_mode = GameMode.HUMAN_VS_HUMAN
        self.cpu_player = CPUPlayer("medium")
        self.cpu_thinking = False
        self.cpu_think_timer = 0
        self.cpu_move_delay = 1000

        # UI
        self.font_large = pygame.font.Font(None, 42)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 20)
        self.clock = pygame.time.Clock()

        # Estatísticas
        self.stats = self.load_stats()

        # Botões nas laterais
        self.buttons = self.create_buttons()

    def create_boards(self):
        """Cria a estrutura de dados para os 9 tabuleiros."""
        return [[[Player.EMPTY for _ in range(3)] for _ in range(3)] for _ in range(9)]

    def create_buttons(self):
        """Cria os botões da interface nas laterais."""
        buttons = {}

        # Botões da lateral esquerda - Controles do jogo
        left_buttons = ['restart', 'new_game', 'clear_stats']
        for i, name in enumerate(left_buttons):
            y = 100 + i * (BUTTON_HEIGHT + BUTTON_MARGIN)
            buttons[name] = pygame.Rect(LEFT_SIDEBAR_X, y, BUTTON_WIDTH, BUTTON_HEIGHT)

        # Botões da lateral direita - Modos de jogo
        right_buttons = ['vs_human', 'vs_cpu_easy', 'vs_cpu_medium', 'vs_cpu_hard']
        for i, name in enumerate(right_buttons):
            y = 100 + i * (BUTTON_HEIGHT + BUTTON_MARGIN)
            buttons[name] = pygame.Rect(RIGHT_SIDEBAR_X, y, BUTTON_WIDTH, BUTTON_HEIGHT)

        return buttons

    def load_stats(self):
        """Carrega estatísticas do arquivo."""
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, 'r') as f:
                    data = json.load(f)
                    return GameStats(**data)
            except:
                pass
        return GameStats()

    def save_stats(self):
        """Salva estatísticas no arquivo."""
        with open(STATS_FILE, 'w') as f:
            json.dump(self.stats.__dict__, f)

    def get_board_index(self, main_row: int, main_col: int) -> int:
        """Converte coordenadas para índice do tabuleiro."""
        return main_row * 3 + main_col

    def check_winner(self, board: List[List[Player]]) -> Optional[Player]:
        """Verifica vencedor em um tabuleiro 3x3."""
        # Linhas
        for row in board:
            if row[0] == row[1] == row[2] and row[0] != Player.EMPTY:
                return row[0]

        # Colunas
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] and board[0][col] != Player.EMPTY:
                return board[0][col]

        # Diagonais
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != Player.EMPTY:
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != Player.EMPTY:
            return board[0][2]

        return None

    def is_board_full(self, board: List[List[Player]]) -> bool:
        """Verifica se um tabuleiro está cheio."""
        return all(cell != Player.EMPTY for row in board for cell in row)

    def make_move(self, main_row: int, main_col: int, row: int, col: int) -> bool:
        """Executa uma jogada se for válida."""
        board_index = self.get_board_index(main_row, main_col)

        # Validações básicas
        if self.game_state != GameState.PLAYING:
            return False

        if self.main_board[main_row][main_col] != Player.EMPTY:
            return False

        if self.boards[board_index][row][col] != Player.EMPTY:
            return False

        # Executa a jogada
        self.boards[board_index][row][col] = self.current_player
        self.last_move = (main_row, main_col, row, col)

        # Verifica vitória no tabuleiro menor
        winner = self.check_winner(self.boards[board_index])
        if winner:
            self.main_board[main_row][main_col] = winner
        elif self.is_board_full(self.boards[board_index]):
            self.main_board[main_row][main_col] = Player.TIE

        # Verifica vitória geral
        game_winner = self.check_winner(self.main_board)
        if game_winner:
            if game_winner == Player.X:
                self.game_state = GameState.X_WINS
                self.stats.x_wins += 1
            else:
                self.game_state = GameState.O_WINS
                self.stats.o_wins += 1
            self.stats.total_games += 1
            self.save_stats()
        elif self.is_board_full(self.main_board):
            self.game_state = GameState.TIE
            self.stats.ties += 1
            self.stats.total_games += 1
            self.save_stats()

        # Troca jogador
        if self.game_state == GameState.PLAYING:
            self.current_player = Player.O if self.current_player == Player.X else Player.X

            # Se for modo CPU e agora é a vez da CPU
            if (self.game_mode == GameMode.HUMAN_VS_CPU and
                    self.current_player == Player.O and
                    self.game_state == GameState.PLAYING):
                self.cpu_thinking = True
                self.cpu_think_timer = pygame.time.get_ticks()

        return True

    def process_cpu_move(self):
        """Processa jogada da CPU."""
        if (self.cpu_thinking and
                pygame.time.get_ticks() - self.cpu_think_timer > self.cpu_move_delay):

            move = self.cpu_player.get_best_move(self)
            if move:
                main_row, main_col, row, col = move
                self.make_move(main_row, main_col, row, col)

            self.cpu_thinking = False

    def restart_game(self):
        """Reinicia o jogo atual."""
        self.boards = self.create_boards()
        self.main_board = [[Player.EMPTY for _ in range(3)] for _ in range(3)]
        self.current_player = Player.X
        self.game_state = GameState.PLAYING
        self.last_move = None
        self.hover_cell = None
        self.cpu_thinking = False

    def set_game_mode(self, mode: GameMode, difficulty: str = "medium"):
        """Define o modo de jogo."""
        self.game_mode = mode
        if mode == GameMode.HUMAN_VS_CPU:
            self.cpu_player = CPUPlayer(difficulty)
        self.restart_game()

    def clear_stats(self):
        """Limpa as estatísticas."""
        self.stats = GameStats()
        self.save_stats()

    def get_mouse_position(self, pos: Tuple[int, int]) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Converte posição do mouse em coordenadas do jogo."""
        x, y = pos

        # Ajusta para o offset do tabuleiro
        x -= BOARD_X
        y -= BOARD_Y

        if x < 0 or x >= BOARD_SIZE or y < 0 or y >= BOARD_SIZE:
            return None

        main_col = min(2, int(x // CELL_SIZE))
        main_row = min(2, int(y // CELL_SIZE))

        sub_col = min(2, int((x % CELL_SIZE) // SUB_CELL_SIZE))
        sub_row = min(2, int((y % CELL_SIZE) // SUB_CELL_SIZE))

        return (main_row, main_col), (sub_row, sub_col)

    def draw_background(self):
        """Desenha o fundo."""
        self.screen.fill(Colors.BACKGROUND)

    def draw_grid(self):
        """Desenha as grades com dimensões corretas."""
        # Grade principal (mais espessa)
        for i in range(1, 3):
            # Linhas verticais
            x = BOARD_X + i * CELL_SIZE
            pygame.draw.line(self.screen, Colors.BLACK,
                             (x, BOARD_Y), (x, BOARD_Y + BOARD_SIZE), LINE_WIDTH)
            # Linhas horizontais
            y = BOARD_Y + i * CELL_SIZE
            pygame.draw.line(self.screen, Colors.BLACK,
                             (BOARD_X, y), (BOARD_X + BOARD_SIZE, y), LINE_WIDTH)

        # Sub-grades
        for main_row in range(3):
            for main_col in range(3):
                for i in range(1, 3):
                    # Linhas verticais das subcélulas
                    start_x = BOARD_X + main_col * CELL_SIZE + i * SUB_CELL_SIZE
                    start_y = BOARD_Y + main_row * CELL_SIZE
                    end_y = BOARD_Y + (main_row + 1) * CELL_SIZE
                    pygame.draw.line(self.screen, Colors.GRAY,
                                     (start_x, start_y), (start_x, end_y), SUB_LINE_WIDTH)

                    # Linhas horizontais das subcélulas
                    start_x = BOARD_X + main_col * CELL_SIZE
                    end_x = BOARD_X + (main_col + 1) * CELL_SIZE
                    start_y = BOARD_Y + main_row * CELL_SIZE + i * SUB_CELL_SIZE
                    pygame.draw.line(self.screen, Colors.GRAY,
                                     (start_x, start_y), (end_x, start_y), SUB_LINE_WIDTH)

    def draw_hover_effect(self):
        """Desenha efeito hover na célula sob o mouse."""
        if (self.hover_cell and self.game_state == GameState.PLAYING and
                not self.cpu_thinking and
                (self.game_mode == GameMode.HUMAN_VS_HUMAN or self.current_player == Player.X)):

            (main_row, main_col), (sub_row, sub_col) = self.hover_cell

            # Verifica se a célula está disponível
            board_index = self.get_board_index(main_row, main_col)
            if (self.main_board[main_row][main_col] == Player.EMPTY and
                    self.boards[board_index][sub_row][sub_col] == Player.EMPTY):
                x = BOARD_X + main_col * CELL_SIZE + sub_col * SUB_CELL_SIZE
                y = BOARD_Y + main_row * CELL_SIZE + sub_row * SUB_CELL_SIZE

                hover_surface = pygame.Surface((SUB_CELL_SIZE, SUB_CELL_SIZE), pygame.SRCALPHA)
                hover_surface.fill(Colors.HOVER)
                self.screen.blit(hover_surface, (x, y))

    def draw_moves(self):
        """Desenha X e O com cores diferentes."""
        for main_row in range(3):
            for main_col in range(3):
                board_index = self.get_board_index(main_row, main_col)

                for row in range(3):
                    for col in range(3):
                        player = self.boards[board_index][row][col]
                        if player != Player.EMPTY:
                            x_center = (BOARD_X + main_col * CELL_SIZE +
                                        col * SUB_CELL_SIZE + SUB_CELL_SIZE // 2)
                            y_center = (BOARD_Y + main_row * CELL_SIZE + row * SUB_CELL_SIZE +
                                        SUB_CELL_SIZE // 2)

                            if player == Player.X:
                                self.draw_x(x_center, y_center, SYMBOL_SIZE, Colors.RED)
                            else:
                                # O sempre azul, independente do modo
                                self.draw_o(x_center, y_center, SYMBOL_SIZE, Colors.BLUE)

    def draw_x(self, x: float, y: float, size: float, color: tuple):
        """Desenha um X estilizado."""
        thickness = 4
        pygame.draw.line(self.screen, color,
                         (x - size, y - size), (x + size, y + size), thickness)
        pygame.draw.line(self.screen, color,
                         (x - size, y + size), (x + size, y - size), thickness)

    def draw_o(self, x: float, y: float, size: float, color: tuple):
        """Desenha um O estilizado."""
        thickness = 4
        pygame.draw.circle(self.screen, color, (int(x), int(y)), int(size), thickness)

    def draw_main_winners(self):
        """Desenha vencedores dos tabuleiros principais."""
        for main_row in range(3):
            for main_col in range(3):
                winner = self.main_board[main_row][main_col]
                if winner in [Player.X, Player.O]:
                    x_center = BOARD_X + main_col * CELL_SIZE + CELL_SIZE // 2
                    y_center = BOARD_Y + main_row * CELL_SIZE + CELL_SIZE // 2

                    # Fundo semi-transparente
                    overlay = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                    overlay.fill((255, 255, 255, 180))
                    self.screen.blit(overlay, (BOARD_X + main_col * CELL_SIZE,
                                               BOARD_Y + main_row * CELL_SIZE))

                    if winner == Player.X:
                        self.draw_x(x_center, y_center, LARGE_SYMBOL_SIZE, Colors.RED)
                    else:
                        # O sempre azul, independente do modo
                        self.draw_o(x_center, y_center, LARGE_SYMBOL_SIZE, Colors.BLUE)
                elif winner == Player.TIE:
                    # Desenha indicador de empate
                    x = BOARD_X + main_col * CELL_SIZE + 10
                    y = BOARD_Y + main_row * CELL_SIZE + 10
                    w = CELL_SIZE - 20
                    h = CELL_SIZE - 20
                    pygame.draw.rect(self.screen, Colors.GRAY, (x, y, w, h), 4)

                    # Texto "EMPATE"
                    text = self.font_small.render("EMPATE", True, Colors.GRAY)
                    text_rect = text.get_rect(center=(x + w // 2, y + h // 2))
                    self.screen.blit(text, text_rect)

    def draw_status(self):
        """Desenha informações de status no centro superior."""
        y_pos = 10

        # Status do jogo
        if self.game_state == GameState.PLAYING:
            if self.cpu_thinking:
                if self.cpu_player.difficulty == "hard":
                    text = "🧠 CPU está pensando profundamente..."
                else:
                    text = "🤖 CPU está pensando..."
                color = Colors.HARD_CPU_COLOR if self.cpu_player.difficulty == "hard" else Colors.CPU_COLOR
            elif self.game_mode == GameMode.HUMAN_VS_CPU:
                if self.current_player == Player.X:
                    text = "Sua vez! Escolha uma célula livre"
                    color = Colors.RED
                else:
                    text = f"Vez da CPU ({self.cpu_player.difficulty.title()})"
                    color = Colors.HARD_CPU_COLOR if self.cpu_player.difficulty == "hard" else Colors.CPU_COLOR
            else:
                text = f"Jogador {self.current_player.value}: Escolha qualquer célula livre"
                color = Colors.RED if self.current_player == Player.X else Colors.BLUE
        elif self.game_state == GameState.X_WINS:
            if self.game_mode == GameMode.HUMAN_VS_CPU:
                text = "🎉 Você VENCEU! 🎉"
            else:
                text = "🎉 Jogador X VENCEU! 🎉"
            color = Colors.RED
        elif self.game_state == GameState.O_WINS:
            if self.game_mode == GameMode.HUMAN_VS_CPU:
                text = f"🤖 CPU VENCEU! 🤖"
            else:
                text = "🎉 Jogador O VENCEU! 🎉"
            color = Colors.BLUE  # O sempre azul
        else:
            text = "⚖️ EMPATE! ⚖️"
            color = Colors.DARK_GRAY

        rendered_text = self.font_medium.render(text, True, color)
        text_rect = rendered_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos + 15))
        self.screen.blit(rendered_text, text_rect)

    def draw_buttons(self):
        """Desenha botões da interface nas laterais."""
        button_texts = {
            'restart': 'Reiniciar',
            'new_game': 'Novo Jogo',
            'clear_stats': 'Limpar Stats',
            'vs_human': 'vs Humano',
            'vs_cpu_easy': 'CPU Fácil',
            'vs_cpu_medium': 'CPU Médio',
            'vs_cpu_hard': 'CPU Difícil'
        }

        for name, rect in self.buttons.items():
            # Efeito hover nos botões
            mouse_pos = pygame.mouse.get_pos()
            is_hovered = rect.collidepoint(mouse_pos)

            # Destaca botão do modo atual
            is_current_mode = False
            if name == 'vs_human' and self.game_mode == GameMode.HUMAN_VS_HUMAN:
                is_current_mode = True
            elif name == 'vs_cpu_easy' and self.game_mode == GameMode.HUMAN_VS_CPU and self.cpu_player.difficulty == "easy":
                is_current_mode = True
            elif name == 'vs_cpu_medium' and self.game_mode == GameMode.HUMAN_VS_CPU and self.cpu_player.difficulty == "medium":
                is_current_mode = True
            elif name == 'vs_cpu_hard' and self.game_mode == GameMode.HUMAN_VS_CPU and self.cpu_player.difficulty == "hard":
                is_current_mode = True

            if is_current_mode:
                color = Colors.GREEN
            elif is_hovered:
                color = Colors.GRAY
            else:
                color = Colors.LIGHT_GRAY

            # Fundo do botão
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
            pygame.draw.rect(self.screen, Colors.DARK_GRAY, rect, 2, border_radius=5)

            # Texto do botão
            text_color = Colors.WHITE if is_current_mode else Colors.BLACK
            text = self.font_small.render(button_texts[name], True, text_color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def draw_sidebar_info(self):
        """Desenha informações nas laterais."""
        # Lateral esquerda - Título dos controles
        title_left = self.font_medium.render("CONTROLES", True, Colors.BLACK)
        self.screen.blit(title_left, (LEFT_SIDEBAR_X, 60))

        # Lateral direita - Título dos modos
        title_right = self.font_medium.render("MODOS DE JOGO", True, Colors.BLACK)
        self.screen.blit(title_right, (RIGHT_SIDEBAR_X, 60))

        # Estatísticas na lateral esquerda (abaixo dos botões)
        stats_y = 300
        stats_title = self.font_medium.render("ESTATÍSTICAS", True, Colors.BLACK)
        self.screen.blit(stats_title, (LEFT_SIDEBAR_X, stats_y))

        stats_text = [
            f"Vitórias X: {self.stats.x_wins}",
            f"Vitórias O: {self.stats.o_wins}",
            f"Empates: {self.stats.ties}",
            f"Total: {self.stats.total_games}"
        ]

        for i, text in enumerate(stats_text):
            rendered = self.font_small.render(text, True, Colors.BLACK)
            self.screen.blit(rendered, (LEFT_SIDEBAR_X, stats_y + 40 + i * 25))

        # Modo atual na lateral direita (abaixo dos botões)
        mode_y = 300
        mode_title = self.font_medium.render("MODO ATUAL", True, Colors.BLACK)
        self.screen.blit(mode_title, (RIGHT_SIDEBAR_X, mode_y))

        if self.game_mode == GameMode.HUMAN_VS_HUMAN:
            mode_text = "Humano vs Humano"
        else:
            mode_text = f"Humano vs CPU ({self.cpu_player.difficulty.title()})"

        mode_rendered = self.font_small.render(mode_text, True, Colors.BLACK)
        self.screen.blit(mode_rendered, (RIGHT_SIDEBAR_X, mode_y + 40))

        # Legenda de cores
        legend_y = mode_y + 80
        legend_title = self.font_medium.render("LEGENDA", True, Colors.BLACK)
        self.screen.blit(legend_title, (RIGHT_SIDEBAR_X, legend_y))

        # X vermelho
        pygame.draw.line(self.screen, Colors.RED,
                         (RIGHT_SIDEBAR_X, legend_y + 40),
                         (RIGHT_SIDEBAR_X + 20, legend_y + 60), 4)
        pygame.draw.line(self.screen, Colors.RED,
                         (RIGHT_SIDEBAR_X, legend_y + 60),
                         (RIGHT_SIDEBAR_X + 20, legend_y + 40), 4)
        x_text = self.font_small.render("X - Vermelho", True, Colors.BLACK)
        self.screen.blit(x_text, (RIGHT_SIDEBAR_X + 30, legend_y + 45))

        # O azul
        o_color = Colors.BLUE  # O sempre azul
        if self.game_mode == GameMode.HUMAN_VS_CPU:
            o_label = "O - CPU (Azul)"
        else:
            o_label = "O - Azul"

        pygame.draw.circle(self.screen, o_color,
                           (RIGHT_SIDEBAR_X + 10, legend_y + 85), 10, 4)
        o_text = self.font_small.render(o_label, True, Colors.BLACK)
        self.screen.blit(o_text, (RIGHT_SIDEBAR_X + 30, legend_y + 80))

    def handle_click(self, pos: Tuple[int, int]):
        """Processa cliques do mouse."""
        # Verifica cliques nos botões
        for name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if name == 'restart' or name == 'new_game':
                    self.restart_game()
                elif name == 'clear_stats':
                    self.clear_stats()
                elif name == 'vs_human':
                    self.set_game_mode(GameMode.HUMAN_VS_HUMAN)
                elif name == 'vs_cpu_easy':
                    self.set_game_mode(GameMode.HUMAN_VS_CPU, "easy")
                elif name == 'vs_cpu_medium':
                    self.set_game_mode(GameMode.HUMAN_VS_CPU, "medium")
                elif name == 'vs_cpu_hard':
                    self.set_game_mode(GameMode.HUMAN_VS_CPU, "hard")
                return

        # Verifica cliques no tabuleiro (apenas se for jogador humano)
        if (self.game_state == GameState.PLAYING and not self.cpu_thinking and
                (self.game_mode == GameMode.HUMAN_VS_HUMAN or self.current_player == Player.X)):
            coords = self.get_mouse_position(pos)
            if coords:
                (main_row, main_col), (sub_row, sub_col) = coords
                self.make_move(main_row, main_col, sub_row, sub_col)

    def handle_mouse_motion(self, pos: Tuple[int, int]):
        """Processa movimento do mouse para efeito hover."""
        coords = self.get_mouse_position(pos)
        self.hover_cell = coords

    def run(self):
        """Loop principal do jogo."""
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event.pos)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_n:
                        self.restart_game()
                    elif event.key == pygame.K_1:
                        self.set_game_mode(GameMode.HUMAN_VS_HUMAN)
                    elif event.key == pygame.K_2:
                        self.set_game_mode(GameMode.HUMAN_VS_CPU, "easy")
                    elif event.key == pygame.K_3:
                        self.set_game_mode(GameMode.HUMAN_VS_CPU, "medium")
                    elif event.key == pygame.K_4:
                        self.set_game_mode(GameMode.HUMAN_VS_CPU, "hard")

            # Processa jogada da CPU se necessário
            self.process_cpu_move()

            # Desenho
            self.draw_background()
            self.draw_hover_effect()
            self.draw_grid()
            self.draw_moves()
            self.draw_main_winners()
            self.draw_status()
            self.draw_buttons()
            self.draw_sidebar_info()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


# --- Execução ---
if __name__ == "__main__":
    game = UltimateTicTacToe()
    game.run()

