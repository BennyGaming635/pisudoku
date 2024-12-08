import tkinter as tk
from tkinter import ttk
import random
from datetime import datetime

class PySudoku:
    def __init__(self, root):
        self.root = root
        self.root.title("PySudoku")

        # Sudoku Grid
        self.frame = ttk.Frame(root, padding=10)
        self.frame.grid()
        
        self.grid = []
        self.puzzle = self.generate_daily_puzzle()
        self.create_grid()

        self.add_controls()

    def create_grid(self):
        for row in range(9):
            row_widgets = []
            for col in range(9):
                value = self.puzzle[row][col]
                entry = ttk.Entry(self.frame, width=2, justify="center", font=("Arial", 18))
                if value != 0:
                    entry.insert(0, value)
                    entry.config(state="disabled")
                entry.grid(row=row, column=col, padx=5, pady=5)
                row_widgets.append(entry)
            self.grid.append(row_widgets)

    def add_controls(self):
        ttk.Button(self.frame, text="Check", command=self.validate).grid(row=10, column=0, columnspan=3, pady=10)
        ttk.Button(self.frame, text="Reset", command=self.reset).grid(row=10, column=3, columnspan=3, pady=10)
        ttk.Button(self.frame, text="Solve", command=self.solve).grid(row=10, column=6, columnspan=3, pady=10)

    def validate(self):
        """Check if the current grid is valid."""
        board = self.get_board()
        if self.is_valid_sudoku(board):
            print("The Sudoku is valid so far!")
        else:
            print("Try changing the current Sudoku. Something here is wrong. :/")

    def solve(self):
        """Solve the puzzle and update the grid."""
        board = self.get_board()
        if self.sudoku_solver(board):
            self.update_grid(board)
            print("You solved the puzzle!")
        else:
            print("No solution exists.")

    def reset(self):
        """Clear all entries."""
        for row in self.grid:
            for cell in row:
                if cell.cget("state") != "disabled":
                    cell.delete(0, tk.END)

    def get_board(self):
        """Read the current state of the Sudoku Grid."""
        board = []
        for row in self.grid:
            current_row = []
            for cell in row:
                value = cell.get()
                current_row.append(int(value) if value.isdigit() else 0)
            board.append(current_row)
        return board
    
    def update_grid(self, board):
        """Update the grid with the solved board."""
        for row in range(9):
            for col in range(9):
                if self.grid[row][col].cget("state") != "disabled":
                    self.grid[row][col].delete(0, tk.END)
                    self.grid[row][col].insert(0, board[row][col])

    def is_valid_sudoku(self, board):
        """ Validate the Sudoku rules."""
        def is_unique(values):
            nums = [v for v in values if v != 0]
            return len(nums) == len(set(nums))

        for row in board:
            if not is_unique(row):
                return False

        for col in zip(*board):
            if not is_unique(col):
                return False
        
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = [
                    board[r][c]
                    for r in range(box_row, box_row + 3)
                    for c in range(box_col, box_col + 3)
                ]
                if not is_unique(box):
                    return False
                
        return True
        
    def sudoku_solver(self, board):
        """Solve the Sudoku using backtracking."""
        empty = self.find_empty_cell(board)
        if not empty:
            return True  # Solved
        row, col = empty

        for num in range(1, 10):
            if self.is_safe(board, row, col, num):
                board[row][col] = num
                if self.sudoku_solver(board):
                    return True
                board[row][col] = 0  # Backtrack

        return False

    def find_empty_cell(self, board):
        """Find an empty cell (represented as 0)."""
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    return (row, col)
        return None

    def is_safe(self, board, row, col, num):
        """Check if it's safe to place a number."""
        if num in board[row]:
            return False
        if num in [board[r][col] for r in range(9)]:
            return False
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if board[r][c] == num:
                    return False
        return True

    def generate_daily_puzzle(self):
        """Generate a random puzzle based on today's date."""
        random.seed(datetime.now().strftime("%Y-%m-%d"))
        base = [[0] * 9 for _ in range(9)]
        for i in range(9):
            base[i][i] = (i + 1)  # Diagonal example for demo
        return base

if __name__ == "__main__":
    root = tk.Tk()
    PySudoku(root)
    root.mainloop()