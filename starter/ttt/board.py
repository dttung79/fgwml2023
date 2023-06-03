BOARD_SIZE = 3

class Cell:
    def __init__(self, x=0, y=0, value=0):
        self.x = x
        self.y = y
        self.value = value
    
    @property
    def X(self):
        return self.x

    @property
    def Y(self):
        return self.y
    
    @property
    def Value(self):
        return self.value
    
    @Value.setter
    def Value(self, value):
        self.value = value
    
    def __str__(self):
        if self.value == 0:
            return "_"
        elif self.value == 1:
            return "X"
        else:
            return "O"

class Board:
    def __init__(self):
        self.board = [[Cell(x, y) for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]

    def __str__(self):
        s = ""
        for row in self.board:
            for cell in row:
                s += str(cell) + " "
            s += "\n"
        return s
    
    def move(self, x, y, value):
        self.board[y][x].Value = value
    
    def get(self, x, y):
        return self.board[y][x].Value
    
    def is_full(self):
        for row in self.board:
            for cell in row:
                if cell.Value == 0:
                    return False
        return True
    
    def who_win(self):
        for row in self.board:
            if row[0].Value == row[1].Value == row[2].Value != 0:
                return row[0].Value
        for i in range(BOARD_SIZE):
            if self.board[0][i].Value == self.board[1][i].Value == self.board[2][i].Value != 0:
                return self.board[0][i].Value
        if self.board[0][0].Value == self.board[1][1].Value == self.board[2][2].Value != 0:
            return self.board[0][0].Value
        if self.board[0][2].Value == self.board[1][1].Value == self.board[2][0].Value != 0:
            return self.board[0][2].Value
        return 0
