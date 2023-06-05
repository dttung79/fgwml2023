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
                is_over = self.play_turn(name1, conn1, name2, conn2, board)
                if is_over:
                    break
                is_over = self.play_turn(name2, conn2, name1, conn1, board)
            
            print('Game over')
            if board.who_win() == 0:
                print('Draw')
            elif board.who_win() == 1:
                print(f'{name1} win')
            elif board.who_win() == 2:
                print(f'{name2} win')
        except ConnectionResetError:
            print('Client disconnected')
        except Exception as e:
            print('Unknown error', e)
        finally:
            conn1.close()
            conn2.close()

    def play_turn(self, name1, conn1, name2, conn2, board):
        # receive move from conn1
        x, y, value = self.receive_move(conn1)
        self.send_message(conn1, 'OPPONENT_TURN')

        self.debug(f"{name1} move: {x},{y},{value}")
        
        # send conn1's move to conn2
        self.send_move(conn2, x, y, value)
        self.send_message(conn2, 'YOUR_TURN')

        # update server board
        board.move(x, y, value)
        self.debug(board)
        
        # check if game is over
        return board.who_win() != -1