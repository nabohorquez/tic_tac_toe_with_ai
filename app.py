import pickle
from flask import Flask, render_template, request, jsonify, session
import numpy as np
from src.tic_tac_toe import TicTacToe
from src.train_qlearning import train_q_learning

app = Flask(__name__)
app.secret_key = 'secret-key'

def get_game():
    board = session.get('board', [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    current_player = session.get('current_player', 1)
    done = session.get('done', False)
    winner = session.get('winner', None)
    game = TicTacToe()
    game.board = np.array(board, dtype=np.int8)
    game.current_player = current_player
    game.done = done
    game.winner = winner
    return game

def save_game(game):
    session['board'] = game.board.tolist()
    session['current_player'] = game.current_player
    session['done'] = game.done
    session['winner'] = game.winner

@app.route('/')
def home():
    return render_template('Descripcion.html')

@app.route('/juego')
def juego():
    return render_template('tic_tac_toe.html')

@app.route('/reset', methods=['POST'])
def reset():
    game = TicTacToe()
    save_game(game)
    return jsonify({'board': game.board.tolist(), 'current_player': game.current_player})

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    row, col = data['row'], data['col']
    game = get_game()
    board, reward, done, info = game.step((row, col))
    save_game(game)

    ia_move = None
    # Si el juego no ha terminado, deja que la IA juegue
    if not done:
        try:
            with open("static/q_table.pkl", "rb") as f:
                memory_ai = pickle.load(f)

            # Cuando la IA juega:
            action = ia_best_action(game, memory_ai)
            ia_row, ia_col = divmod(action, 3)
            board, reward, done, info = game.step(action)
            save_game(game)
            ia_move = {'row': int(ia_row), 'col': int(ia_col)}
        except Exception as _:
            ia_move = None

    return jsonify({
        'board': board.tolist(),
        'reward': reward,
        'done': done,
        'winner': info['winner'],
        'current_player': game.current_player,
        'ia_move': ia_move
    })

@app.route('/generate_results_train', methods=['POST'])
def train():
    train_q_learning()
    return jsonify({'status': 'ok'})

def ia_best_action(game: TicTacToe, memory_ai):
    actions = [i*3+j for i, j in game.available_actions()]
    state = tuple(game.board.reshape(-1))
    # Selección de las mejores opciones
    qs = [memory_ai.get((state, a), 0) for a in actions]
    max_q = max(qs)
    max_actions = [a for a, q in zip(actions, qs) if q == max_q]
    return np.random.default_rng(seed=42).choice(max_actions)

if __name__ == '__main__':
    app.run(debug=True)