from .Solver import Solver

class GameState:
    def __init__(self, size=8):
       self.size = size
       self.queens = []
       self.candidate = None
    
    # Place a queen on the board
    def place_queen(self, row, col):
        if self.is_safe(row, col):
            self.queens.append((row, col))
            return True
        return False
    
    # Remove a queen from the board
    def remove_queen(self, row, col):
        if (row, col) in self.queens:
            self.queens.remove((row, col))
            return True
        return False
    
    # Reset
    def reset(self):
        self.candidate = None
        for row, col in list(self.queens):
            self.remove_queen(row, col)

    # Check if a row and column in the board is unsafe
    def is_safe(self, row, col):
        return (row,col) not in self.get_unsafe_positions()

    # Set a candidate (hover a queen over a cell)
    def set_candidate(self, row, col):
        self.candidate = (row, col)
    
    # Clear candidate from the board
    def clear_candidate(self):
        self.candidate = None

    # Check if the puzzle is solved
    def is_solved(self):
        return len(self.queens) >= self.size

    # Get all the positions on the board that can be attacked by a queen
    def get_unsafe_positions(self):
        unsafe = set()

        for r, c in self.queens:
                
            # Mark same row of queen unsafe
            for col in range(self.size):
                unsafe.add((r, col))

            # Mark same column of queen unsafe
            for row in range(self.size):
                unsafe.add((row, c))

            # Mark diagonals of queen unsafe
            for offset in range(self.size):
                if 0 <= r + offset < self.size and 0 <= c + offset < self.size:
                    unsafe.add((r + offset, c + offset))
                if 0 <= r - offset < self.size and 0 <= c - offset < self.size:
                    unsafe.add((r - offset, c - offset))
                if 0 <= r + offset < self.size and 0 <= c - offset < self.size:
                    unsafe.add((r + offset, c - offset))
                if 0 <= r - offset < self.size and 0 <= c + offset < self.size:
                    unsafe.add((r - offset, c + offset))
            
        return unsafe

                
                