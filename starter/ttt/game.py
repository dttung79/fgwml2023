from board import Board, BOARD_SIZE, Cell
class TicTacToeGame:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.board = Board()
    
    def play_turn(self, player):
        print(f"{player.name}'s turn")
        player.move(self.board)
        print(self.board)

        if self.board.is_full() or self.board.who_win() != -1:
            return True
        else:
            return False

    def start(self):
        print("Welcome to Tic Tac Toe game!")
        print(f"Player 1 is {self.player1.name} playing as X")
        print(f"Player 2 is {self.player2.name} playing as O")

        turn = 1
        while True:
            if turn == 1:
                is_over = self.play_turn(self.player1)
                if is_over:
                    break
                turn = 2
            else:
                is_over = self.play_turn(self.player2)
                if is_over:
                    break
                turn = 1

        if self.board.who_win() == 1:
            print(f"Player {self.player1.name} wins!")
            return 1
        if self.board.who_win() == 2:
            print(f"Player {self.player2.name} wins!")
            return 2
        
        print("Draw!")
        return 0