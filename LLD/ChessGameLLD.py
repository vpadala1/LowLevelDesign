from abc import ABC, abstractmethod

class MoveStrategy(ABC):
    @abstractmethod
    def can_move(self, start_row, start_col, end_row, end_col):
        pass

class StraightMoveStrategy(MoveStrategy):
    def can_move(self, start_row, start_col, end_row, end_col):
        return start_row == end_row or start_col == end_col

class DiagonalMoveStrategy(MoveStrategy):
    def can_move(self, start_row, start_col, end_row, end_col):
        return abs(start_row - end_row) == abs(start_col - end_col)

class LShapeMoveStrategy(MoveStrategy):
    def can_move(self, start_row, start_col, end_row, end_col):
        return (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or \
               (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2)

class ChessPiece(ABC):
    def __init__(self, color, move_strategy):
        self.color = color
        self.move_strategy = move_strategy


    def can_move(self, start_row, start_col, end_row, end_col):
        return self.move_strategy.can_move(start_row, start_col, end_row, end_col)

class King(ChessPiece):
    def __init__(self, color):
        super().__init__(color, None)  # King will have its custom move strategy

    def can_move(self, start_row, start_col, end_row, end_col):
        # King can move one step in any direction
        return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1

class Queen(ChessPiece):
    def __init__(self, color):
        super().__init__(color, StraightMoveStrategy())

    def can_move(self, start_row, start_col, end_row, end_col):
        return StraightMoveStrategy().can_move(start_row, start_col, end_row, end_col) or \
               DiagonalMoveStrategy().can_move(start_row, start_col, end_row, end_col)

class Rook(ChessPiece):
    def __init__(self, color):
        super().__init__(color, StraightMoveStrategy())

class Bishop(ChessPiece):
    def __init__(self, color):
        super().__init__(color, DiagonalMoveStrategy())

class Knight(ChessPiece):
    def __init__(self, color):
        super().__init__(color, LShapeMoveStrategy())

class Pawn(ChessPiece):
    def __init__(self, color):
        super().__init__(color, None)  # Pawn will have its custom move strategy

    def can_move(self, start_row, start_col, end_row, end_col):
        # Assuming white pawns move up and black pawns move down
        if self.color == 'white':
            return start_row - end_row == 1 and start_col == end_col
        else:
            return end_row - start_row == 1 and start_col == end_col

class ChessPieceFactory:
    _instance = None

    @staticmethod
    def get_instance():
        if ChessPieceFactory._instance is None:
            ChessPieceFactory._instance = ChessPieceFactory()
        return ChessPieceFactory._instance

    def create_piece(self, piece_type, color):
        if piece_type == "king":
            return King(color)
        elif piece_type == "queen":
            return Queen(color)
        elif piece_type == "rook":
            return Rook(color)
        elif piece_type == "bishop":
            return Bishop(color)
        elif piece_type == "knight":
            return Knight(color)
        elif piece_type == "pawn":
            return Pawn(color)
        else:
            return None

class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.piece_factory = ChessPieceFactory.get_instance()

    def place_piece(self, piece_type, color, row, col):
        piece = self.piece_factory.create_piece(piece_type, color)
        self.board[row][col] = piece

    def move_piece(self, start_row, start_col, end_row, end_col):
        piece = self.board[start_row][start_col]
        if piece and piece.can_move(start_row, start_col, end_row, end_col):
            self.board[end_row][end_col] = piece
            self.board[start_row][start_col] = None
            print(f"Moved {piece.__class__.__name__} from ({start_row}, {start_col}) to ({end_row}, {end_col})")
        else:
            print("Invalid move")

    def display_board(self):
        for row in self.board:
            print(" ".join([piece.__class__.__name__[0] if piece else "." for piece in row]))

class ChessGame:
    def __init__(self):
        self.board = ChessBoard()
        self.initialize_board()

    def initialize_board(self):
        # Place some initial pieces for demonstration
        self.board.place_piece("rook", "white", 0, 0)
        self.board.place_piece("knight", "white", 0, 1)
        self.board.place_piece("bishop", "white", 0, 2)
        self.board.place_piece("queen", "white", 0, 3)
        self.board.place_piece("king", "white", 0, 4)
        self.board.place_piece("pawn", "white", 1, 0)
        self.board.place_piece("pawn", "white", 1, 1)
        
        self.board.place_piece("rook", "black", 7, 0)
        self.board.place_piece("knight", "black", 7, 1)
        self.board.place_piece("bishop", "black", 7, 2)
        self.board.place_piece("queen", "black", 7, 3)
        self.board.place_piece("king", "black", 7, 4)
        self.board.place_piece("pawn", "black", 6, 0)
        self.board.place_piece("pawn", "black", 6, 1)

    def play(self):
        self.board.display_board()
        self.board.move_piece(0, 0, 3, 0)  # Rook moves straight
        self.board.move_piece(1, 1, 3, 1)  # Pawn moves straight
        self.board.move_piece(0, 1, 2, 2)  # Knight moves L-shape
        self.board.display_board()

if __name__ == "__main__":
    game = ChessGame()
    game.play()
