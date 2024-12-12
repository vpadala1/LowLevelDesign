from abc import ABC, abstractmethod
from collections import deque

class Square:
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece

class MoveStrategy(ABC):
    def is_valid():
        pass

    
class Piece(ABC):
    def __init__(self, white, isKilled = False):
        self.isKilled = isKilled
        self.white = white # Boolean field for True or False

    @abstractmethod
    def isValid(self, curr_row, curr_col, end_row, end_col):
        return False

class King(Piece):
    def __init__(self, white):
        return super().__init__(white)

    def isValid(self, curr_row, curr_col, end_row, end_col):
        if abs(curr_col - end_col) == 1 and abs(curr_row - end_row) == 1: return True
        return False
    
    def __repr__(self):
        return "K"

class Queen(Piece):
    def __init__(self, white):
        return super().__init__(white)
    def isValid(self, curr_row, curr_col, end_row, end_col):
        if (end_row - curr_row) == 0 or (end_col - curr_col) == 0 or (abs(end_row-curr_row) == abs(end_col - curr_col)): return True
        return False
    
    def __repr__(self):
        return "Q"
    
class Bishop(Piece):
    def __init__(self, white):
        return super().__init__(white)
    
    def isValid(self, curr_row, curr_col, end_row, end_col):
        if abs(end_row-curr_row) == abs(end_col-curr_col): return True
        return False
    
    def __repr__(self):
        return "B"
    

class Knight(Piece):
    def __init__(self, white):
        return super().__init__(white)
    
    def isValid(self, curr_row, curr_col, end_row, end_col):
        drow = abs(curr_row-end_row)
        dcol = abs(curr_col-end_col)
        return drow*dcol == 2
    
    def __repr__(self):
        return "Kn"
       
class Rook(Piece):
    def __init__(self, white):
        return super().__init__(white)
    
    def isValid(self, curr_row, curr_col, end_row, end_col):
        if (curr_row-end_row)==0 or (curr_col - end_col) == 0: return True
        return False
    
    def __repr__(self):
        return "R"
    
class Pawn(Piece):
    def __init__(self, white, isKilled=False):
        super().__init__(white, isKilled)

    def isValid(self, curr_row, curr_col, end_row, end_col):
        return (self.white and end_row == curr_row+1 and (curr_col-end_col) == 0) or (self.white == False and (end_row+1 == curr_row) and (curr_col-end_col) == 0)
    
    def __repr__(self):
        return "P"
    

class ChessBoard:
    def __init__(self): 
        self.board = [[Square(row,col) for col in range(8)] for row in range(8)]
    
    def initialise(self):
        for i in range(8):
            self.board[1][i].piece = Pawn(True)
            self.board[6][i].piece = Pawn(False)

        self.board[7][0].piece = Rook(False)
        self.board[7][7].piece = Rook(False)
        self.board[0][0].piece = Rook(True)
        self.board[0][7].piece = Rook(True)

        self.board[7][1].piece = Knight(False)
        self.board[7][6].piece = Knight(False)
        self.board[0][1].piece = Knight(True)
        self.board[0][6].piece = Knight(True)

        self.board[7][2].piece = Bishop(False)
        self.board[7][5].piece = Bishop(False)
        self.board[0][2].piece = Bishop(True)
        self.board[0][5].piece = Bishop(True)

        self.board[7][3].piece = Queen(False)
        self.board[7][4].piece = King(False)
        self.board[0][3].piece = King(True)
        self.board[0][4].piece = Queen(True)

    def validateInput(self,curr_row, curr_col, end_row, end_col):
        if 0<=curr_row<8 and 0<=curr_col<8 and 0<=end_row<8 and 0<=end_col<8: return True
        return False
    
    def move(self, start_position, end_position, player):
        curr_row, curr_col, piece = start_position.row, start_position.col, start_position.piece
        end_row, end_col = end_position.row, end_position.col

        if not self.validateInput(curr_row, curr_col,end_row, end_col):
            raise Exception('Input provided is out of Boundary')
        
        if player.isWhite != piece.white:
            raise Exception('Invalid Move.. You have given a wrong number to move.. Please check and move the pieces only you belong with.. ')
        
        if(piece.isValid(curr_row, curr_col,end_row,end_col)):
            piece_at_end = self.board[end_row][end_col].piece 
            if piece_at_end is not None:
                if piece_at_end.white != piece.white:
                    piece_at_end.isKilled = True
                else:
                    raise Exception('Invalid Move.. Your piece exists in the location you want to move'+ str(piece_at_end))
                
            end_position.piece = start_position.piece
            start_position.piece = None
        else:
            raise Exception('Invalid Move')

    def printBoard(self, board):
        for i in range(8):
            for j in range(8):
                if board[i][j].piece is None:
                    print('  ', end = '| ')
                else:
                    print(str(board[i][j].piece), end = ' | ')
            print()
    
class Player:
    def __init__(self, isWhite):
        self.isWhite = isWhite
    
    def __repr__(self):
        return "Player with White Piece" if self.isWhite else "Player with Black Piece"
    

def main():
    chessBoard = ChessBoard()
    chessBoard.initialise()
    
    player1 = Player(True)
    player2 = Player(False)

    queue = deque()
    queue.append(player1)
    queue.append(player2)

    isWinner = False

    while not isWinner:
        
        chessBoard.printBoard(chessBoard.board)

        player = queue.popleft()

        print('Give current position and the position to place the piece one by one')
        curr_row, curr_col = [int(x) for x in input().split()]
        dest_row, dest_col = [int(x) for x in input().split()]
        start_position = chessBoard.board[curr_row][curr_col]
        end_position = chessBoard.board[dest_row][dest_col]
        try:
            chessBoard.move(start_position,end_position, player)

        except Exception as e:
            print(e)
            queue.appendleft(player)
            continue

        ## Turns of Players & Movements.. 


        queue.append(player)
    



if __name__ == "__main__":
    main()
