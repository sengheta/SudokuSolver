############################################################
# CIS 521: Sudoku Homework
############################################################

student_name = "Sarah Engheta"

############################################################
# Imports
############################################################

import math
import itertools
import collections
import copy
import queue


############################################################
# Section 1: Sudoku Solver
############################################################

def sudoku_cells():
    li = [(x, y) for x in range(9) for y in range(9)]
    return li


def sudoku_arcs():
    li = []
    table = sudoku_cells()
    for first in table:
        for second in table:
            if first == second:
                continue
            if first[0] == second[0]:
                li.append((first, second))
                continue
            if first[1] == second[1]:
                li.append((first, second))
                continue
            if first[0] // 3 == second[0] // 3 and first[1] // 3 == second[1] // 3:
                li.append((first, second))

    return li


def read_board(path):
    file = open(path)
    board = {}
    row = 0
    for line in file:
        for x in range(9):
            if line[x] == '*':
                board[(row, x)] = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
            else:
                board[(row, x)] = set([int(line[x])])
        row += 1
    return board


class Sudoku(object):
    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def get_values(self, cell):
        return self.board[cell]

    def helper_checker(self, cell1, cell2):
        for x in self.board[cell1]:
            for y in self.board[cell2]:
                if (x, y) in self.ARCS:
                    yield x, y

    def is_solved(self):
        for cell in self.CELLS:
            if len(self.board[cell]) != 1:
                return False
        return True

#get first element of set without making it a list
    def remove_inconsistent_values(self, cell1, cell2):
        if (cell1, cell2) in self.ARCS: #might not be necessary
            if len(self.board[cell2]) == 1:
                if list(self.board[cell2])[0] in list(self.board[cell1]):
                    self.board[cell1].remove(list(self.board[cell2])[0])
                    return True
        return False

    def infer_ac3(self):
        queue = collections.deque(self.ARCS)
        while queue:
            arc = queue.popleft()
            if self.remove_inconsistent_values(arc[0], arc[1]):  # c1's domain has been reduced

                for x1, x2 in self.ARCS:  # add all neighbors of c1
                    if x2 == arc[0]:  # i.e. all cells that have an arc with c1
                        queue.append((x1, x2))

    def is_unique(self, value, cell):
        # #check all cells in same row
        # for c in range(9):
        #     temp = (cell[0], c)
        #     if cell == temp:
        #         continue
        #     if value in self.board[temp]:
        #         return False
        #
        # #check all cells in same col
        # for r in range(9):
        #     temp = (r, cell[1])
        #     if cell == temp:
        #         continue
        #     if value in self.board[temp]:
        #         return False

        # check all cells in same block (1,3)
        row = int(cell[0] / 3) * 3
        col = int(cell[1] / 3) * 3 #rounds down

        for r in range(3):
            for c in range(3):
                temp = (row + r, col + c)
                if cell == temp:
                    continue
                if value in self.board[temp]:
                    return False

        return True

    def infer_improved(self):
        made_additional_inference = True
        while made_additional_inference:
            self.infer_ac3()
            made_additional_inference = False
            for cell in self.CELLS:
                if len(self.board[cell]) > 1:
                    for x in self.board[cell]:
                        if self.is_unique(x, cell):
                            self.board[cell] = set([x])
                            made_additional_inference = True
                            break

    def is_valid(self):
        for cell in self.CELLS:
            if len(self.board[cell]) == 0:
                return False
        return True
    #
    # def infer_with_guessing_helper(self):
    #     if self.is_solved():
    #         return self.board
    #
    #     for cell in self.CELLS:
    #         if len(self.board[cell]) > 1:
    #             for x in list(self.board[cell]):
    #                 s = copy.deepcopy(self)
    #                 s.board[cell] = set([x]) #try one of the x values
    #                 s.infer_improved()
    #                 if s.is_valid():
    #                     solution = s.infer_with_guessing_helper()
    #                     if solution is not None:
    #                         return solution
    #
    # def infer_with_guessing(self):
    #     self.infer_improved()
    #     self.board = self.infer_with_guessing_helper()




def main():
    sudoku = Sudoku(read_board("sudoku/medium1.txt"))
    sudoku.infer_improved()
    print(sudoku.is_solved())
    print(sudoku.board)



if __name__ == "__main__":
    main()

############################################################
# Section 2: Feedback
############################################################

# Just an approximation is fine.
feedback_question_1 = 12

feedback_question_2 = """
I found the remove_inconsistent_values to be challenging because
 I was confused about how many values could be removed in one call
"""

feedback_question_3 = """
I like the game aspect of this assignment and also the fact that it built 
upon each function, so each consecutive function used a previous function
"""
