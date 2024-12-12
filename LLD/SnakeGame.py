from enum import Enum

class CellType(Enum):
    EMPTY = 0
    FOOD = 1
    SNAKE_NODE = 2

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.cell_type = CellType.EMPTY

    def get_cell_type(self):
        return self.cell_type

    def set_cell_type(self, cell_type):
        self.cell_type = cell_type

    def __repr__(self):
        return f"Cell({self.row}, {self.col}, {self.cell_type})"

from collections import deque

class Snake:
    def __init__(self, init_pos):
        self.snake_part_list = deque([init_pos])
        self.head = init_pos
        self.head.set_cell_type(CellType.SNAKE_NODE)

    def grow(self):
        self.snake_part_list.append(self.head)

    def move(self, next_cell):
        print(f"Snake is moving to {next_cell.row}, {next_cell.col}")
        tail = self.snake_part_list.pop()
        tail.set_cell_type(CellType.EMPTY)
        
        self.head = next_cell
        self.head.set_cell_type(CellType.SNAKE_NODE)
        self.snake_part_list.appendleft(self.head)

    def check_crash(self, next_cell):
        print("Going to check for crash")
        for cell in self.snake_part_list:
            if cell == next_cell:
                return True
        return False

    def get_snake_part_list(self):
        return self.snake_part_list

    def get_head(self):
        return self.head

import random

class Board:
    def __init__(self, row_count, col_count):
        self.ROW_COUNT = row_count
        self.COL_COUNT = col_count
        self.cells = [[Cell(row, col) for col in range(col_count)] for row in range(row_count)]

    def generate_food(self):
        print("Going to generate food")
        while True:
            row = random.randint(0, self.ROW_COUNT - 1)
            col = random.randint(0, self.COL_COUNT - 1)
            if self.cells[row][col].get_cell_type() != CellType.SNAKE_NODE:
                self.cells[row][col].set_cell_type(CellType.FOOD)
                print(f"Food is generated at: {row}, {col}")
                break

    def get_cells(self):
        return self.cells

class Game:
    DIRECTION_NONE = 0
    DIRECTION_RIGHT = 1
    DIRECTION_LEFT = -1
    DIRECTION_UP = 2
    DIRECTION_DOWN = -2

    def __init__(self, snake, board):
        self.snake = snake
        self.board = board
        self.direction = Game.DIRECTION_NONE
        self.game_over = False

    def update(self):
        print("Going to update the game")
        if not self.game_over:
            if self.direction != Game.DIRECTION_NONE:
                next_cell = self.get_next_cell(self.snake.get_head())
                if self.snake.check_crash(next_cell):
                    self.direction = Game.DIRECTION_NONE
                    self.game_over = True
                else:
                    self.snake.move(next_cell)
                    if next_cell.get_cell_type() == CellType.FOOD:
                        self.snake.grow()
                        self.board.generate_food()

    def get_next_cell(self, current_position):
        print("Going to find next cell")
        row = current_position.row
        col = current_position.col

        if self.direction == Game.DIRECTION_RIGHT:
            col += 1
        elif self.direction == Game.DIRECTION_LEFT:
            col -= 1
        elif self.direction == Game.DIRECTION_UP:
            row -= 1
        elif self.direction == Game.DIRECTION_DOWN:
            row += 1

        return self.board.get_cells()[row][col]

if __name__ == "__main__":
    print("Going to start game")
    
    init_pos = Cell(0, 0)
    snake = Snake(init_pos)
    board = Board(10, 10)
    game = Game(snake, board)

    game.game_over = False
    game.direction = Game.DIRECTION_RIGHT

    # Simulate game loop with manual input for simplicity
    for i in range(5):
        if i == 2:
            game.board.generate_food()
        game.update()
        if i == 3:
            game.direction = Game.DIRECTION_RIGHT
        if game.game_over:
            print("Game Over!")
            break
