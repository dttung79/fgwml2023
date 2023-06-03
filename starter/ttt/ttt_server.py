import socket
from ttt_base import TicTacToeNetworkBase
from board import Board

class TicTacToeServer(TicTacToeNetworkBase):
    def __init__(self, host='127.0.0.1', port=12345, interact=False, verbose=False):
        super().__init__(host, port, interact, verbose)
        self.socket = None

    def start(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            self.debug(f"Bind to {self.host}:{self.port}")

            while True:
                self.socket.listen()
                conn1, _ = self.socket.accept()
                conn2, _ = self.socket.accept()
                self.debug(f"2 players connected")
                self.play(conn1, conn2)
        except ConnectionRefusedError:
            print(f'Cannot connect to {self.host}:{self.port}')
        except KeyboardInterrupt:
            print('Server stopped')
        except Exception as e:
            print('Unknown error', e)
        finally:
            self.socket.close()
    
    def play(self, conn1, conn2):
        try:
            board = Board()
            # receive player names
            name1 = self.receive_message(conn1)
            name2 = self.receive_message(conn2)
            self.debug(f"Player 1: {name1}")
            self.debug(f"Player 2: {name2}")
            
            # send turn message
            self.send_message(conn1, 'YOUR_TURN')
            self.send_message(conn2, 'OPPONENT_TURN')
            
            # play
            is_over = False
            while not is_over:
                is_over = self.play_turn(conn1, conn2, board)
                if is_over:
                    break
                is_over = self.play_turn(conn2, conn1, board)
            
            print('Game over')

        except ConnectionResetError:
            print('Client disconnected')
        except Exception as e:
            print('Unknown error', e)
        finally:
            conn1.close()
            conn2.close()

    def play_turn(self, conn1, conn2, board):
        # receive move
        x, y, value = self.receive_move(conn1)
        self.debug(f"Move: {x},{y},{value}")
        
        # send move
        self.send_move(conn2, x, y, value)

        board.move(x, y, value)
        
        # check if game is over
        if board.who_wins() != 0 or board.is_full():
            self.send_message(conn1, 'END')
            self.send_message(conn2, 'END')
            return True
        else:
            self.send_message(conn2, 'YOUR_TURN')
            self.send_message(conn1, 'OPPONENT_TURN')
            return False