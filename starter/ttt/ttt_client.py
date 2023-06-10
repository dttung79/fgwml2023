import socket
from ttt_base import TicTacToeNetworkBase
from player import SmartBot, StupidBot
from board import Board

class TicTacToeClient(TicTacToeNetworkBase):
    def __init__(self, player_name, player_move, host='127.0.0.1', port=12345, interact=False, verbose=False):
        super().__init__(host, port, interact, verbose)
        self.player = SmartBot(int(player_move), player_name, 'model_800k_2q_df.txt')
        self.board = Board()        
        self.socket = None
    
    def start(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))

            self.debug(f"Connected to {self.host}:{self.port}")
            self.debug(f"Player name: {self.player.name}")

            self.send_message(self.socket, self.player.name)
            self.debug('Waiting for another player')

            self.play()
        except ConnectionRefusedError:
            print(f'Cannot connect to {self.host}:{self.port}')
        except Exception as e:
            print('Unknown error', e)
        finally:
            self.socket.close()
    
    def play(self):
        while True:
            # receive board
            msg = self.receive_message(self.socket)
            self.debug(f"Received message: {msg}")
            
            if msg == 'YOUR_TURN':
                # make a move
                x, y = self.player.move(self.board)
                # send move to server
                self.send_move(self.socket, x, y, self.player.value)
                
                self.debug(f"Sent move: {x} {y} {self.player.value} to opponent")
                self.debug(self.board)
            elif msg == 'OPPONENT_TURN':
                # receive opponent's move
                x, y, value = self.receive_move(self.socket)
                # update board
                self.board.move(x, y, value)
                self.debug(f"Received move: {x} {y} {value} from opponent")
                self.debug(self.board)
            
            # check if win-loose-draw or not over
            game_status = self.board.who_win()
            if game_status != -1:
                if game_status == self.player.value:
                    print('You win')
                elif game_status == 0:
                    print('Draw')
                else:
                    print('You loose')
                break
