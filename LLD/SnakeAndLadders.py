"""
Classes

1. Board
2. Jump -> Snake, Ladder
3. Player 

"""

import random
from collections import deque
import time
class Player:
    
    pid = 1
    def __init__(self, name, position = 0):
        self.player_id = Player.pid 
        Player.pid += 1
        self.name  = name
        self.position = position

    def setPosition(self, position):
        self.position = position

    def getPosition(self):
        return self.position
    
    def __repr__(self):
        return str(self.name)

class Jump:
    def __init__(self, start,end):
        self.start = start
        self.end = end

class Board:
    def __init__(self, size, noOfSnakes, noOfLadders):
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]
        self.initialize(size, noOfSnakes, noOfLadders)
    
    def initialize(self, size, noOfSnakes, noOfLadders):
        while noOfSnakes > 0:
            start = random.randint(1, size*size -1)
            end = random.randint(1,size*size -1)
            if start <= end and start!=size*size-1:
                continue
            noOfSnakes -= 1
            self.board[start//size][start%size] = Jump(start,end)
        
        while noOfLadders > 0:
            start = random.randint(1, size*size -1)
            end = random.randint(1,size*size -1)
            if start >= end:
                continue
            noOfLadders -= 1
            self.board[start//size][start%size] = Jump(start,end)
    
    def movement(self, current_player, steps):
        new_pos = current_player.getPosition() + steps
        if new_pos >= self.size * self.size:
            new_pos = current_player.getPosition()
            return new_pos
        row, col = new_pos//10, new_pos%10
        if isinstance(self.board[row][col], Jump):
            new_pos = self.board[row][col].end
        return new_pos

class Dice:
    def __init__(self, noOfDice):
        self.noOfDice = noOfDice
    
    def getDiceRoll(self):
        cnt = 0
        for i in range(self.noOfDice):
            cnt += random.randint(1,6)
        return cnt

def main():
    size = 10
    noOfSnakes = 3
    noOfLadders = 4
    boardObj = Board(size, noOfSnakes, noOfLadders)
    player1 = Player('Rohit')
    player2 = Player('Suresh')
    dice = Dice(3)
    queue = deque()
    queue.append(player1)
    queue.append(player2)
    isWinner = False
    Winner = ""
    while not isWinner:
        curr_player = queue.popleft()
        print(str(curr_player)+"Turn")
        steps = dice.getDiceRoll()
        print(steps)
        time.sleep(1)
        new_pos = boardObj.movement(curr_player,steps)
        if new_pos>=size*size:
            queue.appendleft(curr_player)
            continue
        curr_player.setPosition(new_pos)
        if new_pos == size*size -1:
            isWinner = True
            Winner = str(curr_player)
        
        queue.append(curr_player)
    
    print("Winner is " + Winner)

if __name__ == "__main__":
    main()