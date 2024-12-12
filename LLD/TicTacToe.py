from enum import Enum
from abc import ABC
from collections import deque

class PieceType(Enum):
    X = 'X'
    O = 'O'


class PlayingPiece:
    def __init__(self, piece):
        self.Piece = piece
    
    def getPiece(self):
        return self.Piece
    
    def setPiece(self,piece):
        self.Piece = piece
    
    def __str__(self):
        return str(self.Piece.value)
    
    def __repr__(self):
        return str(self.Piece.value)
    
class PlayingPieceX(PlayingPiece):
    def __init__(self):
        super().__init__(PieceType.X)
    
class PlayingPieceO(PlayingPiece):
    def __init__(self):
        super().__init__(PieceType.O)
    

class Player:
    def __init__(self, PlayingPiece):
        self.PlayingPiece = PlayingPiece

    def getPlayingPiece(self):
        return self.PlayingPiece
    
    def __repr__(self):
        return "Player with Playing Piece " +str(self.PlayingPiece)
    
    
class Board:
    def __init__(self):
        self.board = [[None for _ in range(3)] for _ in range(3)]

    
    def isValid(self, row,col):
        if 0<=row<=2 and 0<=col<=2: 
            if not self.board[row][col]: return True
        return False
    
    def addPiece(self, row, col, piece):
        self.board[row][col] = piece


    def printBoard(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is None:
                    print("  ", end = ' |')
                else:
                    print(" " +str(self.board[i][j]), end = ' |')
            print()
    

    def getWinner(self, row, col, piece):
        rowWise = colWise = diagWise = revDiagWise = True
        for i in range(3):
            if self.board[row][i] != piece:
                rowWise = False
        for i in range(3):
            if self.board[i][col] != piece:
                colWise = False
        for i in range(3):
            if self.board[i][i] != piece:
                diagWise = False
            if self.board[2-i][i] != piece:
                revDiagWise = False
        
        return rowWise or colWise or diagWise or revDiagWise


def main():

    board = Board()
    Player1 = Player(PlayingPieceX())
    Player2 = Player(PlayingPieceO())

    print(Player1)
    queue = deque()
    queue.append(Player1)
    queue.append(Player2)

    isWinner = False
    while not isWinner:
        print(board.printBoard())
        row, col = list(int(x) for x in input().split())
        current_player = queue.popleft()
        if board.isValid(row,col):
            board.addPiece(row,col, current_player.getPlayingPiece())
            if board.getWinner(row,col, current_player.getPlayingPiece()):
                isWinner  = True
            queue.append(current_player)
        else:
            print("The position is already filled.. Try a new one..")
            queue.appendleft(current_player)


    print(str(current_player) + " is the winner")

if __name__ == '__main__':
    main()