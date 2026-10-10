"""Tic-Tac-Toe game engine: board state, moves, win/draw detection."""

PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '

WIN_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
)


class TicTacToe:
    """3x3 Tic-Tac-Toe with legal moves, undo, and terminal checks."""

    def __init__(self, board=None, current_player=PLAYER_X):
        if board is None:
            self.board = [EMPTY] * 9
        else:
            self.board = list(board)
        self.current_player = current_player

    def copy(self):
        return TicTacToe(board=self.board, current_player=self.current_player)

    def get_available_moves(self):
        return [i for i, cell in enumerate(self.board) if cell == EMPTY]

    def is_valid_move(self, pos):
        return isinstance(pos, int) and 0 <= pos <= 8 and self.board[pos] == EMPTY

    def make_move(self, pos, player=None):
        """Place a mark. If player is omitted, uses current_player and switches turn."""
        if not self.is_valid_move(pos):
            return False
        mark = player if player is not None else self.current_player
        self.board[pos] = mark
        if player is None:
            self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X
        return True

    def undo_move(self, pos):
        if 0 <= pos <= 8:
            self.board[pos] = EMPTY
            self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X

    def check_winner(self):
        for a, b, c in WIN_LINES:
            if self.board[a] != EMPTY and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def get_winning_line(self):
        for line in WIN_LINES:
            a, b, c = line
            if self.board[a] != EMPTY and self.board[a] == self.board[b] == self.board[c]:
                return line
        return None

    def is_draw(self):
        return self.check_winner() is None and EMPTY not in self.board

    def is_game_over(self):
        return self.check_winner() is not None or EMPTY not in self.board

    def to_dict(self):
        return {
            'board': list(self.board),
            'current_player': self.current_player,
            'winner': self.check_winner(),
            'winning_line': list(self.get_winning_line()) if self.get_winning_line() else None,
            'is_draw': self.is_draw(),
            'is_game_over': self.is_game_over(),
            'available_moves': self.get_available_moves(),
        }
