from gui import MainWindow, Board
from controller import GameController
from core import GameState, Solver

BOARD_SIZE = 8
SQUARE_SIZE = 70
WINDOW_SIZE = "800x700"

if __name__ == "__main__":
    game_state = GameState(BOARD_SIZE)
    solver = Solver(BOARD_SIZE)
    app = MainWindow(BOARD_SIZE, SQUARE_SIZE, WINDOW_SIZE)
    controller = GameController(game_state, solver, app)

    # Connect Events
    app.control_panel.on_next = controller.on_next
    app.control_panel.on_reset = controller.on_reset

    app.mainloop()

    
