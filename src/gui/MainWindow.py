import tkinter as tk
from .Board import Board
from .ControlPanel import ControlPanel

class MainWindow(tk.Tk):
    def __init__(self, board_size, square_size, window_size):
        super().__init__()

        # Initialize vars
        self.board_size = board_size
        self.square_size = square_size
        self.window_size = window_size

        # Initialize window
        self.title("Eight Queens Problem")
        self.geometry(self.window_size)
        self.resizable(True, True)
        
        # Create board
        self.board = Board(self, self.board_size, self.square_size)
        self.board.pack()

        # Create control panel
        self.control_panel = ControlPanel(self)
        self.control_panel.pack()
        
        # Place window infront
        self.focus_force()

    def update(self, model):
        message = self.control_panel.display_message 
        message
    
        self.board.draw_board()

        candidate = model.candidate
        if candidate:
            self.board.draw_candidate(candidate[0], candidate[1])

        for r, c in model.queens:
            self.board.draw_queen(r, c)
        
        if model.is_solved():
            message.configure(text="Puzzle Solved!", font=("Arial", 16, "bold"), fg="Lime")
            for r in range(self.board_size):
                for c in range(self.board_size):
                    self.board.highlight_square(r, c, (-60, 60, -60))
        else:
            num_queens = len(model.queens)
            total_queens = model.size

            message.configure(text=f'{num_queens}/{total_queens} Queens Placed', font=("Arial", 16), fg="White")
            unsafe = model.get_unsafe_positions()
            for r, c in unsafe:
                self.board.highlight_square(r, c)
