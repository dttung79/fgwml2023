from game import TicTacToeGame
from player import Human, SmartBot, StupidBot

#game = TicTacToeGame(Human(1, "Human"), SmartBot(2, "Bot"))
#game = TicTacToeGame(SmartBot(1, "SmartBot"), Human(2, "Human"))
#game = TicTacToeGame(SmartBot(1, "SmartBot"), StupidBot(2, "StupidBot"))
#game = TicTacToeGame(StupidBot(1, "StupidBot"), SmartBot(2, "SmartBot"))
#game = TicTacToeGame(SmartBot(1, "SmartBot 1"), SmartBot(2, "SmartBot 2"))
model = 'model.txt'
wins = 0
looses = 0
draws = 0
# for i in range(1000):
#     game = TicTacToeGame(SmartBot(1, "SmartBot", model), StupidBot(2, "StupidBot"))
#     result = game.start()
#     if result == 1:
#         wins += 1
#     elif result == 2:
#         looses += 1
#     else:
#         draws += 1
# print(f"SmartBot plays first. Wins: {wins}, Looses: {looses}, Draws: {draws}")

# wins = 0
# looses = 0
# draws = 0
# for i in range(1000):
#     game = TicTacToeGame(StupidBot(1, "StupidBot"), SmartBot(2, "SmartBot", model))
#     result = game.start()
#     if result == 2:
#         wins += 1
#     elif result == 1:
#         looses += 1
#     else:
#         draws += 1
# print(f"StupidBot plays first. Wins: {wins}, Looses: {looses}, Draws: {draws}")

wins = 0
looses = 0
draws = 0
for i in range(1000):
    game = TicTacToeGame(SmartBot(1, "SmartBot1", model), SmartBot(2, "SmartBot2", model))
    result = game.start()
    if result == 2:
        wins += 1
    elif result == 1:
        looses += 1
    else:
        draws += 1
print(f"Both SmartBot plays. Wins: {wins}, Looses: {looses}, Draws: {draws}")