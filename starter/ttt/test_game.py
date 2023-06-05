from game import TicTacToeGame
from player import Human, SmartBot

game = TicTacToeGame(Human(1, "Human"), SmartBot(2, "Bot"))
game.start()