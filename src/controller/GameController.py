import random

class GameController:
    def __init__(self, model, solver, view):
        self.model = model
        self.solver = solver
        self.view = view

        self.view.update(self.model)
    
    def on_next(self):
        if not self.model.is_solved():
            queens = self.solver.next_step()
            if queens is not None:
                self.model.reset()
                for r, c in queens:
                    self.model.place_queen(r, c)
                self.view.update(self.model)


    def on_reset(self):
        self.model.reset()
        self.solver.start()
        self.view.update(self.model)