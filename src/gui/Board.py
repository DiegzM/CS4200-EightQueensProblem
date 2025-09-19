import tkinter as tk
from PIL import Image, ImageTk
import os

CURRENT_DIR = os.path.dirname(__file__)       
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../..")) 
MEDIA_DIR = os.path.join(PROJECT_ROOT, "media")
QUEEN_IMG_PATH = os.path.join(MEDIA_DIR, "queen.png")

class Board(tk.Frame):
    def __init__(self, parent, board_size, square_size):
        super().__init__(parent)
        self.board_size = board_size
        self.square_size = square_size
        self.canvas = tk.Canvas(self, width=board_size*square_size, height=board_size*square_size)
        self.canvas.pack()
        self.squares = {}
        self.color1 = "#eeeed2"
        self.color2 = "#759656"
        self.queen_img = None
        self.candidate_img = None
        
        if os.path.exists(QUEEN_IMG_PATH):
            pil_img = Image.open(QUEEN_IMG_PATH).resize((square_size, square_size), Image.LANCZOS)
            self.queen_img = ImageTk.PhotoImage(pil_img)

            r, g, b, a = pil_img.split()
            a = a.point(lambda p: int(p * 0.5))  # reduce opacity by 50%
            pil_candidate = Image.merge("RGBA", (r, g, b, a))

            self.candidate_img = ImageTk.PhotoImage(pil_candidate)

        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(self.board_size):
            for c in range(self.board_size):
                x1 = c * self.square_size
                y1 = r * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                base_color = self.color1 if (r + c) % 2 == 0 else self.color2
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=base_color, outline="")
                self.squares[(r, c)] = {
                    "rect": rect,
                    "queen": None,
                    "candidate": None,
                    "highlighted": False,
                    "base_color": base_color  # <- store original color
                }
        
    def draw_queen(self, row, col):
            x = col * self.square_size + self.square_size // 2
            y = row * self.square_size + self.square_size // 2

            if self.queen_img:
                queen = self.canvas.create_image(x, y, image=self.queen_img)
            else:
                queen = self.canvas.create_text(x, y, text="Q", font=("Arial", self.square_size // 2), fill="black")

            self.squares[(row, col)]["queen"] = queen
            return
    
    def remove_queen(self, row, col):
        square = self.squares.get((row, col))
        if square and square["queen"]:
            self.canvas.delete(square["queen"])
            square["queen"] = None


    def draw_candidate(self, row, col):
        """Draw a semi-transparent queen (ghost)."""
        x = col * self.square_size + self.square_size // 2
        y = row * self.square_size + self.square_size // 2

        if self.candidate_img:
            queen = self.canvas.create_image(x, y, image=self.candidate_img)
        else:
            queen = self.canvas.create_text(
                x, y, text="Q",
                font=("Arial", self.square_size // 2),
                fill="gray"
            )

        self.squares[(row, col)]["candidate"] = queen

    def remove_candidate(self, row, col):
        """Remove a candidate queen if it exists."""
        square = self.squares.get((row, col))
        if square and square.get("candidate"):
            self.canvas.delete(square["candidate"])
            square["candidate"] = None
            square.pop("candidate_img", None)  # clean up image reference


    def highlight_square(self, row, col, rgb_delta=(60, -60, -60)):
        """Highlight a square by applying an RGB delta tuple to its base color."""
        square = self.squares.get((row, col))
        if not square:
            return

        rect = square["rect"]
        base_color = square["base_color"]
        new_color = self.apply_rgb_delta(base_color, rgb_delta)
        self.canvas.itemconfig(rect, fill=new_color)
        square["highlighted"] = True


    def reset_square_color(self, row, col):
        """Reset square back to its base checkered color."""
        square = self.squares.get((row, col))
        if not square:
            return

        rect = square["rect"]
        self.canvas.itemconfig(rect, fill=square["base_color"])
        square["highlighted"] = False


    def apply_rgb_delta(self, hex_color, delta):
        """Apply an (r,g,b) delta to a hex color string."""
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)

        dr, dg, db = delta

        new_r = min(255, max(0, r + dr))
        new_g = min(255, max(0, g + dg))
        new_b = min(255, max(0, b + db))

        return f"#{new_r:02x}{new_g:02x}{new_b:02x}"