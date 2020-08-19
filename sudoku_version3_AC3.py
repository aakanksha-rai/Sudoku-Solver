import sys
import copy
import time

# THIS VERSION IS BACKTRACKING SEARCH + AC3
# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

#This class is used to keep track of what values can be used in that position in the sudoku puzzle
class Position:
    def __init__(self, value):
        self.domain = set()
        self.value = value
        self.unassignedNeighbours = set()
    
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
                self.solution[r][c].unassignedNeighbours = self.getUnassignedNeighbours(r, c)
    
    #Gets all unassigned neighbours of all positions
    def getUnusedNeighbours(self):
        for r in range(9):
            for c in range(9):
                self.solution[r][c].unassignedNeighbours = self.getUnassignedNeighbours(r, c)
    
    #Gets unassigned neighbours of a particulat position
    def getUnassignedNeighbours(self, r, c):
        unassignedNeighbours = set()
        for i in range(9):
            if i != c and self.solution[r][i].value == 0:
                unassignedNeighbours.add((r, i))
            if i != r and self.solution[i][c].value == 0:
                unassignedNeighbours.add((i, c))
        boxRow = r // 3 * 3
        boxColumn = c // 3 * 3
        for i in range(boxRow, boxRow + 3):
            for j in range(boxColumn, boxColumn + 3):
                if i != r and j != c and self.solution[i][j].value == 0:
                    unassignedNeighbours.add((i, j))
        return unassignedNeighbours
    
    #Used to choose the position that will be assigned. It currently just chooses the first unassigned position
    def choosePosition(self):
        for r in range(9):
            for c in range(9):
                if self.solution[r][c].value == 0:
                    return (r,c)
        return None
    
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
    def assignValue(self, row, column, value, changes):
        self.solution[row][column].value = value
        for (r, c) in self.solution[row][column].unassignedNeighbours:
            self.solution[r][c].unassignedNeighbours.remove((row, column))
            if self.solution[r][c].value == 0 and (value in self.solution[r][c].domain):
                self.solution[r][c].domain.remove(value)
                if changes.has_key((r, c)):
                    changes.add(value)
                else:
                    changes[(r, c)] = set([value])
        self.AC3(changes)
        
    #Used to undo the assignment to a position
    def removeAssignment(self, row, column, changes):
        value = self.solution[row][column].value
        self.solution[row][column].value = 0
        for (r, c) in self.solution[row][column].unassignedNeighbours:
            self.solution[r][c].unassignedNeighbours.add((row, column))
        self.undoAC3(changes)
        
    
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
        
    def createQueue(self):
        q = list()
        for row in range(9):
            for column in range(9):
                if self.solution[row][column].value != 0:
                    continue
                for (r, c) in self.solution[row][column].unassignedNeighbours:
                    if len(self.solution[r][c].domain) == 1 and self.solution[r][c].value == 0:
                        q.append(((row, column), (r, c)))
        return q
    
    def updateQueue(self, q, row, column, r, c):
        for (i, j) in self.solution[row][column].unassignedNeighbours:
            if (i, j) != (row, column) and (i, j) != (r, c) and self.solution[i][j].value == 0:
                q.append(((i,j), (row, column)))
    
    def revise(self, row, column, r, c, changes):
        myDomain = self.solution[row][column].domain
        neighbourDomain = self.solution[r][c].domain
        revise = False
        if len(neighbourDomain) != 1:
            return False
        for n in neighbourDomain:
            if n in myDomain:
                myDomain.remove(n)
                revise = True
                if changes.has_key((row, column)):
                    changes[(row, column)].add(n)
                else:
                    changes[(row, column)] = set([n])
        return revise
    
    def AC3(self, changes):
        q = self.createQueue()
        while len(q) != 0:
            (row, column), (r,c) = q.pop(0)
            if self.revise(row, column, r, c, changes):
                if (len(self.solution[row][column].domain) == 0):
                    return False
                if (len(self.solution[row][column].domain) == 1):
                    self.updateQueue(q, row, column, r, c)
        return True
    
    def undoAC3(self, changes):
        for (r,c), change in changes.items():
            while len(change) != 0:
                self.solution[r][c].domain.add(change.pop())
    
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
            changes = dict()
            self.assignValue(row, column, n, changes)
            isPossible = self.backtrack()
            if isPossible:
                return True
            else:
                self.removeAssignment(row, column, changes)
                
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
