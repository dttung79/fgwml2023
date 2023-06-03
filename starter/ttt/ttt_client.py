import socket
from ttt_base import TicTacToeNetworkBase
from player import SmartBot
from board import Board

class TicTacToeClient(TicTacToeNetworkBase):
    def __init__(self, player_name, player_move, host='127.0.0.1', port=12345, interact=False, verbose=False):
        super().__init__(host, port, interact, verbose)
        self.player = SmartBot(player_move, player_name)
        self.board = Board()

        if verbose:
            print(self.board)
        
        self.socket = None
    
    def start(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.debug(f"Connected to {self.host}:{self.port}")
            self.debug(f"Player name: {self.player.name}")
            self.send_message(self.socket, self.player.name)
            self.play()
        except ConnectionRefusedError:
            print(f'Cannot connect to {self.host}:{self.port}')
    
    def play(self):
        while True:
            # receive board
            msg = self.receive_message(self.socket)
            if msg == 'END':
                # check if win-loose-draw
                if self.board.who_wins() == self.player.value:
                    print('You win')
                elif self.board.who_wins() == 0:
                    print('Draw')
                else:
                    print('You loose')
                break
            
            if msg == 'YOUR_TURN':
                # make a move
                x, y = self.player.move(self.board)
                self.send_move(self.socket, x, y, self.player.value)
                if self.verbose:
                    print(self.board)
            elif msg == 'OPPONENT_TURN':
                # receive opponent's move
                x, y, value = self.receive_move(self.socket)
                self.board.move(x, y, value)
                if self.verbose:
                    print(self.board)