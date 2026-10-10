"""Flask backend for the Tic-Tac-Toe AI visualizer."""

import os
from flask import Flask, render_template, request, jsonify

from game import TicTacToe, PLAYER_X, PLAYER_O, EMPTY
from agent import (
    RandomAgent,
    HeuristicAgent,
    MinimaxAgent,
    create_agent,
    simulate_match,
)

app = Flask(__name__)


def _agent_stats(agent):
    scores = getattr(agent, 'move_scores', {}) or {}
    # Normalize keys to strings for JSON
    matrix = [None] * 9
    for pos, score in scores.items():
        matrix[int(pos)] = score
    return {
        'nodes_explored': getattr(agent, 'nodes_explored', 0),
        'move_scores': {str(k): v for k, v in scores.items()},
        'score_matrix': matrix,
        'agent_name': getattr(agent, 'name', type(agent).__name__),
    }


def _game_payload(game, extra=None):
    payload = game.to_dict()
    if extra:
        payload.update(extra)
    return payload


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/new_game', methods=['POST'])
def new_game():
    data = request.get_json(silent=True) or {}
    mode = data.get('mode', 'human_ai')  # human_ai | two_player | ai_ai
    difficulty = data.get('difficulty', 'unbeatable')
    human_plays = data.get('human_plays', 'X')  # X or O

    game = TicTacToe()
    ai_move = None
    stats = None

    # If human plays O in human_ai, AI (X) moves first
    if mode == 'human_ai' and human_plays == PLAYER_O:
        agent = create_agent(difficulty, PLAYER_X)
        ai_move = agent.get_move(game)
        if ai_move is not None:
            game.make_move(ai_move)
        stats = _agent_stats(agent)

    return jsonify(_game_payload(game, {
        'mode': mode,
        'difficulty': difficulty,
        'human_plays': human_plays,
        'last_ai_move': ai_move,
        'ai_stats': stats,
    }))


@app.route('/api/move', methods=['POST'])
def make_human_move():
    data = request.get_json(silent=True) or {}
    board = data.get('board', [EMPTY] * 9)
    current_player = data.get('current_player', PLAYER_X)
    position = data.get('position')
    mode = data.get('mode', 'human_ai')
    difficulty = data.get('difficulty', 'unbeatable')
    human_plays = data.get('human_plays', PLAYER_X)

    game = TicTacToe(board=board, current_player=current_player)

    if game.is_game_over():
        return jsonify({'error': 'Game is already over', **game.to_dict()}), 400

    if position is None or not game.is_valid_move(int(position)):
        return jsonify({'error': 'Invalid move', **game.to_dict()}), 400

    game.make_move(int(position))

    ai_move = None
    stats = None

    if mode == 'human_ai' and not game.is_game_over():
        ai_player = PLAYER_O if human_plays == PLAYER_X else PLAYER_X
        agent = create_agent(difficulty, ai_player)
        ai_move = agent.get_move(game)
        if ai_move is not None:
            game.make_move(ai_move)
        stats = _agent_stats(agent)

    return jsonify(_game_payload(game, {
        'last_ai_move': ai_move,
        'ai_stats': stats,
        'mode': mode,
        'difficulty': difficulty,
        'human_plays': human_plays,
    }))


@app.route('/api/ai_move', methods=['POST'])
def ai_single_move():
    """One AI step for AI-vs-AI mode (or stepping)."""
    data = request.get_json(silent=True) or {}
    board = data.get('board', [EMPTY] * 9)
    current_player = data.get('current_player', PLAYER_X)
    difficulty_x = data.get('difficulty_x', 'unbeatable')
    difficulty_o = data.get('difficulty_o', 'medium')

    game = TicTacToe(board=board, current_player=current_player)

    if game.is_game_over():
        return jsonify(_game_payload(game, {'last_ai_move': None, 'ai_stats': None}))

    difficulty = difficulty_x if game.current_player == PLAYER_X else difficulty_o
    agent = create_agent(difficulty, game.current_player)
    move = agent.get_move(game)
    if move is not None:
        game.make_move(move)

    return jsonify(_game_payload(game, {
        'last_ai_move': move,
        'ai_stats': _agent_stats(agent),
        'difficulty_x': difficulty_x,
        'difficulty_o': difficulty_o,
    }))


@app.route('/api/analyze', methods=['POST'])
def analyze_position():
    """Return Minimax score matrix for the current board without playing."""
    data = request.get_json(silent=True) or {}
    board = data.get('board', [EMPTY] * 9)
    current_player = data.get('current_player', PLAYER_X)
    use_alpha_beta = data.get('use_alpha_beta', True)

    game = TicTacToe(board=board, current_player=current_player)
    agent = MinimaxAgent(player=current_player, use_alpha_beta=use_alpha_beta)

    if game.is_game_over() or not game.get_available_moves():
        return jsonify({
            'ai_stats': _agent_stats(agent),
            'board': game.board,
            'current_player': current_player,
            'suggested_move': None,
        })

    suggested = agent.get_move(game)
    return jsonify({
        'ai_stats': _agent_stats(agent),
        'board': game.board,
        'current_player': current_player,
        'suggested_move': suggested,
    })


@app.route('/api/simulate', methods=['POST'])
def run_simulation():
    data = request.get_json(silent=True) or {}
    agent1_type = data.get('agent1', 'minimax')
    agent2_type = data.get('agent2', 'random')
    num_games = int(data.get('num_games', 50))
    num_games = max(1, min(num_games, 200))

    def build(kind, player):
        kind = kind.lower()
        if kind in ('random', 'easy'):
            return RandomAgent(player=player)
        if kind in ('heuristic', 'medium'):
            return HeuristicAgent(player=player)
        return MinimaxAgent(player=player, use_alpha_beta=True)

    a1 = build(agent1_type, PLAYER_X)
    a2 = build(agent2_type, PLAYER_O)
    results = simulate_match(a1, a2, num_games=num_games)
    results['agent1'] = a1.name
    results['agent2'] = a2.name
    results['agent1_type'] = agent1_type
    results['agent2_type'] = agent2_type
    return jsonify(results)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
