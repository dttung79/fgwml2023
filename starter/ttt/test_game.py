from game import TicTacToeGame
from player import Human, StupidBot

game = TicTacToeGame(Human(1, "Human"), StupidBot(2, "Bot"))
game.start()