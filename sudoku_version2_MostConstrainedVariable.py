import sys
import copy
import time

#I AM MAKING A CHANGE

# THIS VERSION IS BACKTRACKING SEARCH + MOST CONSTRAINED VARIABLE HEURISTIC
# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

#This class is used to keep track of what values can be used in that position in the sudoku puzzle
class Position:
    def __init__(self, value):
        self.domain = set()
        self.value = value
    
    def __str__(self):
        return str(self.value)

#This class represents the sudoku puzzle and is used to solve a sudoku puzzle
class Puzzle:
    def __init__(self, solution, unusedRowValues, unusedColumnValues, unusedBoxValues):
        self.nodeCount = 0
        self.solution = solution
        self.unusedRowValues = unusedRowValues
        self.unusedColumnValues = unusedColumnValues
        self.unusedBoxValues = unusedBoxValues
        #Seting the domains for all positions
        for r in range(9):
            for c in range(9):
                self.solution[r][c].domain = self.unusedRowValues[r].intersection(self.unusedColumnValues[c], self.unusedBoxValues[r//3][c//3])
                
    #Used to choose the position that will be assigned. It currently just chooses the first unassigned position
    def choosePosition(self):
        row = -1
        column = -1
        min = 10000
        for r in range(9):
            for c in range(9):
                if self.solution[r][c].value == 0:
                    if len(self.solution[r][c].domain) < min:
                        min = len(self.solution[r][c].domain)
                        row = r
                        column = c
        return (row, column)
    
    #Used to removed a value from UnusedValues for a row/column
    def removeFromUnusedValues(self, r, c, value):
        self.unusedRowValues[r].remove(value)
        self.unusedColumnValues[c].remove(value)
        self.unusedBoxValues[r//3][c//3].remove(value)
     
    #Used to add a value to UnusedValues for a row/column
    def addToUnusedValues(self, r, c, value):
        self.unusedRowValues[r].add(value)
        self.unusedColumnValues[c].add(value)
        self.unusedBoxValues[r//3][c//3].add(value)
    
    #Used to update all domains whenever a change is made
    def updatePositionDomains(self):
         for r in range(9):
              for c in range(9):
                  self.solution[r][c].domain = self.unusedRowValues[r].intersection(self.unusedColumnValues[c], self.unusedBoxValues[r//3][c//3])
    
    #Used to assign a value to a position
    def assignValue(self, r, c, value):
        self.solution[r][c].value = value
        self.removeFromUnusedValues(r, c, value)
        self.updatePositionDomains()
        
    #Used to undo the assignment to a position
    def removeAssignment(self, r, c):
        value = self.solution[r][c].value
        self.solution[r][c].value = 0
        self.addToUnusedValues(r, c, value)
        self.updatePositionDomains()
    
    #Used to check if we have found a solution
    def isGoal(self):
        for r in range(9):
            for c in range(9):
                if self.solution[r][c].value == 0:
                    return False
        return True
    
    #Used to check whether a solution is possible after the latest assignment
    def isValidAssignment(self):
        for r in range(9):
            for c in range(9):
                if len(self.solution[r][c].domain) == 0 and self.solution[r][c].value == 0:
                    return False
        return True
        
    #The backtracking algorithm to find a solution
    def backtrack(self):
        self.nodeCount = self.nodeCount + 1
        if not self.isValidAssignment():
            return False
        if self.isGoal():
            return True
        (row, column) = self.choosePosition()
        domainCpy = self.solution[row][column].domain.copy()
        for n in domainCpy:
            self.assignValue(row, column, n)
            isPossible = self.backtrack()
            if isPossible:
                return True
            else:
                self.removeAssignment(row, column)
                
    def __str__(self):
        s = ""
        for r in range(9):
            for c in range(9):
                 s = s + " " + str(self.solution[r][c])
            s = s + "\n"
        return s
        
    def __hash__(self):
        return hash(str(self))
        

class Sudoku(object):
    def __init__(self, puzzle):
        #The sudoku puzzle we are given
        self.puzzle = puzzle
        
        #Initialize the 'answer' matrix (since we want each position in the puzzle to be a Position object)
        self.ans = [[Position(0) for r in range(9)] for c in range(9)]
        for r in range(9):
            for c in range(9):
                self.ans[r][c].value = self.puzzle[r][c]
        
        #Sets to keep track of unused values in rows and columns
        self.unusedRowValues = [set([1, 2, 3, 4, 5, 6, 7, 8, 9]) for i in range(9)]
        self.unusedColumnValues = [set([1, 2, 3, 4, 5, 6, 7, 8, 9]) for i in range(9)]
        self.unusedBoxValues =  [[set([1, 2, 3, 4, 5, 6, 7, 8, 9]) for i in range(3)] for j in range(3)]
        for r in range(9):
            for c in range(9):
                n = self.ans[r][c].value
                if n != 0:
                    self.unusedRowValues[r].remove(n)
                    self.unusedColumnValues[c].remove(n)
                    self.unusedBoxValues[r//3][c//3].remove(n)

    def solve(self):
        start = time.time()
        mySudoku = Puzzle(self.ans, self.unusedRowValues, self.unusedColumnValues, self.unusedBoxValues)
        mySudoku.backtrack()
        end = time.time()
        print("Time taken: " + str(end - start))
        print("Nodes seen: " + str(mySudoku.nodeCount))
        return mySudoku.solution

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
