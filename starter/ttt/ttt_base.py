BUFFER_SIZE = 1024

class TicTacToeNetworkBase:
    def __init__(self, host='127.0.0.1', port=12345, interact=False, verbose=False):
        self.host = host
        self.port = port
        self.interact = interact
        self.verbose = verbose
    
    def send_message(self, conn, message):
        whites = ' ' * (BUFFER_SIZE - len(msg))
        msg += whites
        conn.send(msg.encode('utf8'))
    
    def send_move(self, conn, x, y, value):
        msg = f"{x},{y},{value}"
        self.send_message(conn, msg)
    
    def receive_message(self, conn):
        msg = conn.recv(BUFFER_SIZE).decode('utf8').strip()
        return msg.strip()

    def receive_move(self, conn):
        msg = self.receive_message(conn)
        x, y = msg.split(',')
        return int(x), int(y)

    def debug(self, *messges):
        if not self.verbose:
            return
        for msg in messges:
            print(msg)
        if self._interact:
            input('Press any key to continue...')