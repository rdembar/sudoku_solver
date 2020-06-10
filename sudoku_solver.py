#sudoku_solver.py
import tkinter as tk
from functools import partial
from tkinter import messagebox
import math

class Sudoku:
    def __init__(self, root):
        self.puzzle = tk.Frame(root, borderwidth = 1, relief = tk.SOLID)
        valid = self.puzzle.register(self.check_entry)
    
        #add 3x3 boxes with thick border
        self.frames = []
        for i in range(3):
            self.frames.append([])
            for j in range(3):
                self.frames[i].append(tk.Frame(
                    master = self.puzzle,
                    borderwidth = 1,
                    relief = tk.SOLID,
                    bg = "white",
                ))
                self.frames[i][j].grid(row=i, column=j, sticky = "nsew")
                for k in range(3):
                    self.frames[i][j].columnconfigure(k, weight=1, minsize=50)
                    self.frames[i][j].rowconfigure(k, weight=1, minsize=50)
    
        #add 9x9 grid of entries
        self.entries = []
        for i in range(9):
                self.entries.append([])
                for j in range(9):
                    self.entries[i].append(tk.Entry(
                        master = self.frames[math.floor(i/3)][math.floor(j/3)],
                        relief = tk.GROOVE,
                        borderwidth = 1,
                        width = 1,
                        font = (50),
                        justify = tk.CENTER,
                        validate = 'all',
                        validatecommand=(valid, '%P', i, j)
                    ))
                    self.entries[i][j].grid(row=i%3, column=j%3, sticky="nsew")
         
    def is_valid(self, i, r,c):
        """
        given integer i, row r, column c, checks if
        i is a valid entry in position [r,c]
        """
        #check row/column
        for k in range(9):
            if k != c and self.entries[r][k].get() == str(i): #check row
                return False
            if k != r and self.entries[k][c].get() == str(i): #check col
                return False          
        #check block
        sections = [[0,1,2],[3,4,5],[6,7,8]]
        for sec in sections:
            if r in sec:
                rows = sec
            if c in sec:
                cols = sec
        for row in rows:
            for col in cols:
                if [row, col] != [r,c] and self.entries[row][col].get() == str(i):
                    return False    
        return True
    
    def check_entry(self, val, i, j):
        """
        given a user entry into Sudoku board and a position
        (i,j), checks if user entry is valid in that position
        """
        if val == '':
            return True
        if val in ['1','2','3','4','5','6','7','8','9']:
            if self.is_valid(int(val), int(i), int(j)):
                return True
        return False
    
def solve(sud):
    board = []
    for i in range(9):
        board.append([])
        for j in range(9):
            if sud.entries[i][j].get() == '':
                board[i].append(0)
            else:
                board[i].append(int(sud.entries[i][j].get()))
                
    #stores list of zero positions
    list_zeros = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                list_zeros.append([i,j])
                
    #backtracking algorithm
    enum = 0
    while enum < len(list_zeros) and 0 <= enum:
        r = list_zeros[enum][0]
        c = list_zeros[enum][1]
        is_changed = False
        for k in range(1 + board[r][c], 10):
            if is_changed == False and sud.is_valid(k, r,c):
                board[r][c] = k
                sud.entries[r][c].delete(0)
                sud.entries[r][c].insert(0, str(k))
                enum = enum+1
                is_changed = True
        if is_changed == False:
            board[r][c] = 0
            sud.entries[r][c].delete(0)
            enum = enum - 1
    if enum == -1:
        tk.messagebox.showwarning(message="This puzzle does not have a solution!")
    
def main():
    root = tk.Tk()
    title = tk.Label(root, text="Sudoku solver", font = 50)
    instr = tk.Label(root, wraplength = 400,
                     text = 'Fill in entries on the Sudoku board below, '\
                         'then hit solve. The program will fill in the '\
                         'remaining entries!')
    sud = Sudoku(root)
    button = tk.Button(
            master = sud.puzzle,
            text = "Solve",
            font = (30),
            command = partial(solve, sud),
            width = 50,
            fg = "white",
            bg = "red"
        )
    button.grid(columnspan=3)
    title.pack()
    instr.pack()
    sud.puzzle.pack()
    root.mainloop()
    
main()