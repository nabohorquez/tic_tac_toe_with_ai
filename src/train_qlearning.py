import os
import numpy as np
import matplotlib.pyplot as plt
from src.tic_tac_toe import TicTacToe
import pickle

episodes = 1000
alpha = 0.1
gamma = 0.9
epsilon = 0.1

Q = {}
Q_FILE = 'static/q_table.pkl'
rewards = []
rng = np.random.default_rng(seed=42)

def state_to_tuple(board):
    return tuple(board.reshape(-1))

def choose_action(game, epsilon):
    actions = [i*3+j for i, j in game.available_actions()]
    if not actions:
        return None
    if rng.random() < epsilon:
        return rng.choice(actions)
    state = state_to_tuple(game.board)
    qs = [Q.get((state, a), 0) for a in actions]
    max_q = max(qs)
    max_actions = [a for a, q in zip(actions, qs) if q == max_q]
    return rng.choice(max_actions)

def agent_move(game, state):
    action = choose_action(game, epsilon)
    if action is None:
        return state, 0, True, 0
    obs, reward, done, _ = game.step(action)
    next_state = state_to_tuple(obs)
    actions = [i*3+j for i, j in game.available_actions()]
    next_q = max([Q.get((next_state, a), 0) for a in actions], default=0)
    Q[(state, action)] = Q.get((state, action), 0) + alpha * (reward + gamma * next_q - Q.get((state, action), 0))
    return next_state, reward, done

def opponent_move(game, state):
    actions = [i*3+j for i, j in game.available_actions()]
    if not actions:
        return state, 0, True
    action = rng.choice(actions)
    obs, reward, done, _ = game.step(action)
    return state_to_tuple(obs), reward, done

def train_q_learning():
    Q = get_q_memory()

    for _ in range(episodes):
        game = TicTacToe()
        # Alternar quién empieza
        game.current_player = 1 if rng.random() < 0.5 else -1

        state, _ = game.reset()
        state = state_to_tuple(state)
        done = False
        total_reward = 0

        while not done:
            if game.current_player == 1:
                state, reward, done = agent_move(game, state)
                total_reward += reward
            else:
                state, _, done = opponent_move(game, state)

        rewards.append(total_reward)

    # Guardar la gráfica
    plt.figure(figsize=(8,4))
    plt.plot(rewards, alpha=0.5, label="Recompensa por episodio")
    plt.xlabel("Episodio")
    plt.ylabel("Recompensa total")
    plt.title("Recompensa por episodio (Q-Learning)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("static/rewards.png")
    print("Entrenamiento terminado y gráfica guardada en static/rewards.png")

    # Generar la tabla Q
    with open(Q_FILE, "wb") as f:
        pickle.dump(Q, f)
    print("Q-table guardada en static/q_table.pkl")

def get_q_memory():
    q_memory = {}
    if os.path.exists(Q_FILE):
        with open(Q_FILE, "rb") as f:
            q_memory = pickle.load(f)
        print(f"Q-table cargada desde {Q_FILE}")
    return q_memory