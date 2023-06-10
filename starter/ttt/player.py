from abc import ABC, abstractmethod
from board import Board, BOARD_SIZE, Cell
import random as rd
import numpy as np

class Player(ABC):
    def __init__(self, value, name):
        self.value = value
        self.name = name

    @abstractmethod
    def move(self, board):
        pass
    @property
    def Value(self):
        return self.value
    
class Human(Player):
    def __init__(self, value, name):
        super().__init__(value, name)

    def move(self, board):
        while True:
            x = int(input("Enter x: "))
            y = int(input("Enter y: "))
            if board.get(x, y) == 0:
                break
            else:
                print("Invalid move! Try again.")

        board.move(x, y, self.value)
        return x, y

class StupidBot(Player):
    def __init__(self, value, name):
        super().__init__(value, name)

    def move(self, board):
        while True:
            x = rd.randint(0, BOARD_SIZE - 1)
            y = rd.randint(0, BOARD_SIZE - 1)
            if board.get(x, y) == 0:
                break

        board.move(x, y, self.value)
        return x, y

class SmartBot(StupidBot):
    def __init__(self, value, name, model=None):
        super().__init__(value, name)
        self.model = model

    def board_to_state(self, board):
        state = ''
        for i in range(3):
            for j in range(3):
                state += '_' if board.get(i, j) == 0 else 'X' if board.get(i, j) == 1 else 'O'
        return state
    
    def action_to_move(self, action):
        return action // 3, action % 3

    # TODO: override the move method to make a smarter move
    def move(self, board):
        # load model from model.txt to q_table
        q_tables = [{}, {}]
        with open(self.model, 'r') as f:
            n_states1 = int(f.readline().strip())
            n_states2 = int(f.readline().strip())
            for i in range(n_states1):
                state = f.readline().strip()
                if not state or state == '':
                    break
                values = f.readline().strip().split(',')[:-1]
                values = [float(v) for v in values]
                q_tables[0][state] = np.array(values)
            for i in range(n_states2):
                state = f.readline().strip()
                if not state or state == '':
                    break
                values = f.readline().strip().split(',')[:-1]
                values = [float(v) for v in values]
                q_tables[1][state] = np.array(values)
        # find action with max Q at the current state also check if the action is valid
        state = self.board_to_state(board)
        # if it's a new state which is not trained, use StupidBot
        if state not in q_tables[self.value-1]:
            return super().move(board)
        values = q_tables[self.value-1][state]
        max_q_value = max(values)
        i_max = [i for i, v in enumerate(values) if v == max_q_value and state[i] == '_']
        if len(i_max) == 0:
            return super().move(board)
        # select random action from valid actions
        action = rd.choice(i_max)
        x, y = self.action_to_move(action)
        board.move(x, y, self.value)
        return x, y
        # if there is no valid action, use StupidBot
        # return super().move(board)
        
