"""AI search agents for Tic-Tac-Toe: Random, Heuristic, and Minimax."""

import random
from game import TicTacToe, PLAYER_X, PLAYER_O, EMPTY


class RandomAgent:
    """Uniform random legal-move baseline (Easy)."""

    def __init__(self, player=PLAYER_X):
        self.player = player
        self.name = "Random"
        self.nodes_explored = 0
        self.move_scores = {}

    def get_move(self, game):
        moves = game.get_available_moves()
        self.nodes_explored = len(moves)
        self.move_scores = {m: 0 for m in moves}
        return random.choice(moves) if moves else None


class HeuristicAgent:
    """
    Rule-based priority strategy (Medium):
    Immediate Win > Immediate Block > Center > Corners > Edges.
    """

    CENTER = 4
    CORNERS = (0, 2, 6, 8)
    EDGES = (1, 3, 5, 7)

    def __init__(self, player=PLAYER_X):
        self.player = player
        self.name = "Heuristic"
        self.nodes_explored = 0
        self.move_scores = {}

    def _opponent(self):
        return PLAYER_O if self.player == PLAYER_X else PLAYER_X

    def _find_winning_move(self, game, player):
        for pos in game.get_available_moves():
            game.board[pos] = player
            won = game.check_winner() == player
            game.board[pos] = EMPTY
            if won:
                return pos
        return None

    def get_move(self, game):
        moves = game.get_available_moves()
        self.nodes_explored = len(moves)
        self.move_scores = {}

        if not moves:
            return None

        # Priority 1: Immediate win
        win = self._find_winning_move(game, self.player)
        if win is not None:
            for m in moves:
                self.move_scores[m] = 100 if m == win else 0
            return win

        # Priority 2: Immediate block
        block = self._find_winning_move(game, self._opponent())
        if block is not None:
            for m in moves:
                self.move_scores[m] = 80 if m == block else 0
            return block

        # Priority 3–5: Center > Corners > Edges
        if self.CENTER in moves:
            for m in moves:
                self.move_scores[m] = 50 if m == self.CENTER else 10
            return self.CENTER

        corners = [m for m in self.CORNERS if m in moves]
        if corners:
            choice = random.choice(corners)
            for m in moves:
                self.move_scores[m] = 30 if m in corners else 5
            return choice

        edges = [m for m in self.EDGES if m in moves]
        choice = random.choice(edges) if edges else moves[0]
        for m in moves:
            self.move_scores[m] = 10 if m in edges else 0
        return choice


class MinimaxAgent:
    """Unbeatable Minimax with optional Alpha-Beta pruning (Hard)."""

    def __init__(self, player=PLAYER_X, use_alpha_beta=True):
        self.player = player
        self.use_alpha_beta = use_alpha_beta
        self.name = "Minimax"
        self.nodes_explored = 0
        self.move_scores = {}

    def _opponent(self):
        return PLAYER_O if self.player == PLAYER_X else PLAYER_X

    def _evaluate(self, game, depth):
        winner = game.check_winner()
        if winner == self.player:
            return 10 - depth
        if winner == self._opponent():
            return depth - 10
        return 0

    def _minimax(self, game, depth, maximizing, alpha, beta):
        self.nodes_explored += 1

        if game.is_game_over():
            return self._evaluate(game, depth)

        if maximizing:
            best = float('-inf')
            for pos in game.get_available_moves():
                game.board[pos] = self.player
                score = self._minimax(game, depth + 1, False, alpha, beta)
                game.board[pos] = EMPTY
                best = max(best, score)
                if self.use_alpha_beta:
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
            return best

        best = float('inf')
        opponent = self._opponent()
        for pos in game.get_available_moves():
            game.board[pos] = opponent
            score = self._minimax(game, depth + 1, True, alpha, beta)
            game.board[pos] = EMPTY
            best = min(best, score)
            if self.use_alpha_beta:
                beta = min(beta, best)
                if beta <= alpha:
                    break
        return best

    def get_move(self, game):
        moves = game.get_available_moves()
        self.nodes_explored = 0
        self.move_scores = {}

        if not moves:
            return None

        best_score = float('-inf')
        best_moves = []

        for pos in moves:
            game.board[pos] = self.player
            score = self._minimax(
                game, depth=0, maximizing=False,
                alpha=float('-inf'), beta=float('inf')
            )
            game.board[pos] = EMPTY
            self.move_scores[pos] = score
            if score > best_score:
                best_score = score
                best_moves = [pos]
            elif score == best_score:
                best_moves.append(pos)

        return random.choice(best_moves)


def simulate_match(agent1, agent2, num_games=50):
    """
    Simulate num_games between agent1 and agent2.
    Agents alternate who starts; each keeps its fixed mark identity
    relative to the match by temporarily aligning player fields
    with the side they play that game.
    """
    results = {
        'agent1_wins': 0,
        'agent2_wins': 0,
        'draws': 0,
        'num_games': num_games,
    }

    original_p1 = agent1.player
    original_p2 = agent2.player

    for i in range(num_games):
        # Alternate who starts; agent1 is always X when it starts
        if i % 2 == 0:
            agent1.player = PLAYER_X
            agent2.player = PLAYER_O
            first, second = agent1, agent2
            first_is_agent1 = True
        else:
            agent2.player = PLAYER_X
            agent1.player = PLAYER_O
            first, second = agent2, agent1
            first_is_agent1 = False

        game = TicTacToe()
        while not game.is_game_over():
            agent = first if game.current_player == PLAYER_X else second
            move = agent.get_move(game)
            if move is None:
                break
            game.make_move(move)

        winner = game.check_winner()
        if winner is None:
            results['draws'] += 1
        elif (winner == PLAYER_X and first_is_agent1) or (winner == PLAYER_O and not first_is_agent1):
            results['agent1_wins'] += 1
        else:
            results['agent2_wins'] += 1

    agent1.player = original_p1
    agent2.player = original_p2
    return results


def create_agent(difficulty, player):
    """Factory used by the Flask app."""
    difficulty = (difficulty or 'unbeatable').lower()
    if difficulty in ('easy', 'random'):
        return RandomAgent(player=player)
    if difficulty in ('medium', 'heuristic'):
        return HeuristicAgent(player=player)
    return MinimaxAgent(player=player, use_alpha_beta=True)
