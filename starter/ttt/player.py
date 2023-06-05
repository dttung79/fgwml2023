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
    def __init__(self, value, name):
        super().__init__(value, name)

    # TODO: override the move method to make a smarter move
