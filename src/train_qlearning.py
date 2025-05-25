import numpy as np
import matplotlib.pyplot as plt
from src.tic_tac_toe import TicTacToe
import pickle

episodes = 10000
alpha = 0.1
gamma = 0.9
epsilon = 0.1

Q = {}
rewards = []
rng = np.random.default_rng()

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

def train_q_learning():
    for _ in range(episodes):
        game = TicTacToe()
        state, _ = game.reset()
        state = state_to_tuple(state)
        done = False
        total_reward = 0
        reward = 0
        info = {}

        while not done:
            if game.current_player == 1:
                action = choose_action(game, epsilon)
                if action is None:
                    break
                obs, reward, done, info = game.step(action)
                next_state = state_to_tuple(obs)
                total_reward += reward

                # Q-learning actualizado
                actions = [i*3+j for i, j in game.available_actions()]
                next_q = max([Q.get((next_state, a), 0) for a in actions], default=0)
                Q[(state, action)] = Q.get((state, action), 0) + alpha * (reward + gamma * next_q - Q.get((state, action), 0))
                state = next_state
            else:
                actions = [i*3+j for i, j in game.available_actions()]
                if not actions:
                    break
                action = rng.choice(actions)
                obs, reward, done, info = game.step(action)
                state = state_to_tuple(obs)
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
    with open("static/q_table.pkl", "wb") as f:
        pickle.dump(Q, f)
    print("Q-table guardada en static/q_table.pkl")