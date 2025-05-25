import numpy as np
import gymnasium as gym
from gymnasium import spaces

class TicTacToe(gym.Env):  # Hereda de gym.Env
    metadata = {"render_modes": ["human"]}

    def __init__(self):
        super().__init__()
        self.observation_space = spaces.Box(low=-1, high=1, shape=(3,3), dtype=np.int8)
        self.action_space = spaces.Discrete(9)
        self.reset()

    def reset(self, seed=None, options=None):
        self.board = np.zeros((3, 3), dtype=np.int8)  # Asegúrate de que sea un array de NumPy
        self.current_player = 1
        self.done = False
        self.winner = None
        return self.board.copy(), {}

    def available_actions(self):
        return list(zip(*np.where(self.board == 0)))

    def check_game_status(self):
        for player in [1, -1]:
            if any(np.all(self.board[i, :] == player) for i in range(3)) or \
            any(np.all(self.board[:, j] == player) for j in range(3)) or \
            np.all(np.diag(self.board) == player) or \
            np.all(np.diag(np.fliplr(self.board)) == player):
                return (1 if player == 1 else -1), True, player
        if not np.any(self.board == 0):
            return 0, True, 0  # Empate
        return 0, False, None

    def step(self, action):
        if not isinstance(self.board, np.ndarray):
            self.board = np.array(self.board, dtype=np.int8)  # Convierte a array si no lo es

        if action is None:
            return self.board.copy(), 0, True, {"winner": self.winner}
        if isinstance(action, tuple):
            row, col = action
        else:
            row, col = divmod(action, 3)
        if self.done or self.board[row, col] != 0:
            return self.board.copy(), -10, True, {"winner": self.winner}

        self.board[row, col] = self.current_player
        reward, self.done, self.winner = self.check_game_status()
        if not self.done:
            self.current_player *= -1
        return self.board.copy(), reward, self.done, {"winner": self.winner}