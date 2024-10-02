from itertools import islice
import random
import time


class Node:
    def __init__(self, row, col, val):
        self.row = row
        self.col = col
        self.val = val

        self.next = None

class Stack:
    def __init__(self):
        self.top = None

    def push(self, row, col, val):
        newNode = Node(row, col, val)
        newNode.next = self.top
        self.top = newNode

    def pop(self):
        if self.isEmpty():
            raise IndexError("Pop from an empty stack")
        poppedNode = self.top
        self.top = self.top.next
        return poppedNode.row, poppedNode.col, poppedNode.val

    def peek(self):
        if self.isEmpty():
            raise IndexError("Peek from an empty stack")
        return self.top.row, self.top.col, self.top.val

    def isEmpty(self):
        return self.top is None



class Board:

    def __init__(self, boardsLocation, boardNumber):
        self.boardsLocation = boardsLocation
        self.boardNumber = boardNumber

        startIndex = (boardNumber - 1) * 10
        with open(boardsLocation) as file:
            self.board = [
                [int(char) for char in line.strip()]
                for line in islice(file, startIndex, startIndex + 9)
            ]

    def printBoard(self):
        print("\033[H\033[J", end="")
        print(f'Board number: {self.boardNumber}\n')
        print('+------+-------+-------+')
        for i, row in enumerate(self.board):
            formattedRow = ['#' if num == 0 else str(num) for num in row]
            print(' ' + ' | '.join(' '.join(formattedRow[i:i+3]) for i in range(0, 9, 3)))
            if (i + 1) % 3 == 0:
                print('+------+-------+-------+')



class Solver:
    def __init__(self, board):
        self.board = board
        self.moveStack = Stack()
        self.currentRowIdx = 0
        self.currentColIdx = 0
        self.guess = 1
        self.incorrectGuesses = 0

    def backtrackingSolver(self):
        while self.currentColIdx < 9 and self.currentRowIdx < 9:
            self.updateStoredValues()
            if int(self.board.board[self.currentRowIdx][self.currentColIdx]) != 0:
                self.moveToNextCell()
                self.guess = 1
                continue

            while self.guess <= 9:
                self.board.printBoard()
                time.sleep(0.005)
                if self.isValidMove(self.currentRow, self.currentCol, self.currentBox, self.guess):
                    self.board.board[self.currentRowIdx][self.currentColIdx] = self.guess
                    self.moveStack.push(self.currentRowIdx, self.currentColIdx, self.guess)
                    self.moveToNextCell()
                    self.guess = 1
                    break
                else:
                    self.guess += 1
            else:
                if self.moveStack.isEmpty():
                    print("No solution exists")
                    return
                self.backtrack()

        self.currentColIdx = 0
        self.board.printBoard()
        print(f'Solved with {self.incorrectGuesses} incorrect guesses')

    def isValidMove(self, row, col, box, val):
        if val in row or val in col or val in box:
            return False
        return True

    def backtrack(self):
        self.incorrectGuesses += 1
        poppedRow, poppedCol, poppedVal = self.moveStack.pop()
        self.board.board[poppedRow][poppedCol] = 0
        self.currentRowIdx = poppedRow
        self.currentColIdx = poppedCol
        self.guess = poppedVal + 1

    def updateStoredValues(self):
        self.currentRow = self.board.board[self.currentRowIdx][0:9]
        self.currentCol = [self.board.board[i][self.currentColIdx] for i in range(9)]
        self.currentBox = self.getBox(self.currentRowIdx, self.currentColIdx)

    def getBox(self, currentRow, currentCol):
        box = []
        boxX = currentCol // 3
        boxY = currentRow // 3

        for row in self.board.board[boxY*3:(boxY*3) + 3]:
            for square in row[boxX*3:(boxX*3) + 3]:
                box.append(square)

        return box

    def moveToNextCell(self):
        if self.currentColIdx == 8:
            self.currentRowIdx += 1
            self.currentColIdx = 0
        else:
            self.currentColIdx += 1



class Interface:

    def __init__(self):
        print("\033[H\033[J", end="")
        self.boardsLocation = input("Please enter the location of your boards.txt file, or leave blank to use the current directory: ")

        if self.boardsLocation == '':
            self.boardsLocation = 'boards.txt'
        print("\033[H\033[J", end="")

    def menu(self):
        print("Welcome to Tom's Sudoku Solver")
        print('================================================================')
        print('Would you like to:')
        print('    1. Pick a board')
        print('    2. Use a random one')

        userInput = None
        while userInput not in [1, 2]:
            try:
                userInput = int(input("Please enter either 1 or 2: ").strip())
                if userInput not in [1, 2]:
                    print("Invalid input. Please enter 1 or 2.\n")
            except ValueError:
                print("Invalid input. Please enter a valid number (1 or 2).\n")

        if userInput == 1:
            self.chooseBoard()
        elif userInput == 2:
            self.randomBoard()

    def chooseBoard(self):
        boardChoice = None
        while boardChoice not in range(1, 51):
            try:
                boardChoice = int(input("Please choose a board: ").strip())
                if boardChoice not in range(1, 51):
                    print("Invalid input. Please enter a number between 1 and 50\n")
            except ValueError:
                print("Invalid input. Please enter a valid number between 1 and 50.\n")

        self.boardNumber = boardChoice
        self.startSolver()

    def randomBoard(self):
        self.boardNumber = random.randint(1, 50)
        self.startSolver()


    def startSolver(self):
        board = Board(self.boardsLocation, self.boardNumber)
        board.printBoard()

        solver = Solver(board)

        solver.backtrackingSolver()



if __name__ == '__main__':
    interface = Interface()
    interface.menu()
