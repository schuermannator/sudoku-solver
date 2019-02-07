""" Simple sudoku solver based on Z3 SMT Solver - go beat the newspaper """

from z3 import *
import time
import unittest

class Sudoku:
    def __init__(self, data=None):
        if data and data[0] and len(data) == len(data[0]) == 9:
            self.data = data
        else:
            self.data = None

    def __str__(self):
        output = ""
        for i, r in enumerate(self.data):
            if i in [3, 6]:
                output += '------+------+------\n'
            for j, c in enumerate(r):
                if j in [3, 6]:
                    output += '|'
                output += str(self.data[i][j]).rjust(2)
            output += "\n"
        return output

    def solve(self):
        s = Solver()
        # array of cells defined as int
        cells = [[Int("cell_%s_%s" % (i+1, j+1)) for j in range(9)] for i in range(9)]
        self.read_init(s, cells)
        for i in range(9):
            # row and col-wise constraints, respectively
            s.add(Distinct(cells[i]))
            s.add(Distinct([x[i] for x in cells]))
            for j in range(9):
                # cell-wise constraints
                s.add(cells[i][j] >= 1, cells[i][j] <= 9)

        # constraints on 3x3 blocks
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                block = []
                for ii in range(3):
                    for jj in range(3):
                        block.append(cells[i+ii][j+jj])
                s.add(Distinct(block))

        start = time.perf_counter()
        check = s.check()
        end = time.perf_counter()

        if check == sat:
            self.model = s.model()
            matrix = []
            for i in range(9):
                row = []
                for j in range(9):
                    row.append(self.model.evaluate(cells[i][j]))
                matrix.append(row)
            solved = Sudoku(data=matrix)
            return solved, (end - start)*1000
        else:
            self.model = check
            return None, None

    def read_init(self, solver, cells):
        for i in range(9):
            for j in range(9):
                if self.data[i][j] != -1:
                    solver.add(cells[i][j] == self.data[i][j])

class TestSolver(unittest.TestCase):

    # TODO: add more tests

    def test_sat_result(self):
        test_puzzle = [[-1, -1, -1, -1, -1, -1, -1, 1, -1],
                       [-1, -1, -1, -1, -1, 2, -1, -1, 3],
                       [-1, -1, -1, 4, -1, -1, -1, -1, -1],
                       [-1, -1, -1, -1, -1, -1, 5, -1, -1],
                       [4, -1, 1, 6, -1, -1, -1, -1, -1],
                       [-1, -1, 7, 1, -1, -1, -1, -1, -1],
                       [-1, 5, -1, -1, -1, -1, 2, -1, -1],
                       [-1, -1, -1, -1, 8, -1, -1, 4, -1],
                       [-1, 3, -1, 9, 1, -1, -1, -1, -1]]
        puzzle = Sudoku(data=test_puzzle)
        print(puzzle)
        solved, time = puzzle.solve()
        print(solved)
        print("Solved in {} ms".format(time))
        self.assertIsNotNone(solved)

if __name__ == '__main__':
    print("Hello!")
    
