class Solver:
    def __init__(self, size=8):
        self.size = size
        self._generator = None

    def start(self):
        """Reset solving process."""
        self._generator = self._solve_row(0, [])

    def next_step(self):
        """Advance one step in the search."""
        if self._generator is None:
            self.start()
        try:
            return next(self._generator)
        except StopIteration:
            return None  # search finished

    def heuristic(self, queens):
        """Number of attacking pairs (lower = better)."""
        conflicts = 0
        for i in range(len(queens)):
            for j in range(i + 1, len(queens)):
                r1, c1 = queens[i]
                r2, c2 = queens[j]
                if r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                    conflicts += 1
        return conflicts

    def is_safe(self, queens, row, col):
        """Check if placing at (row, col) is valid given queens."""
        for r, c in queens:
            if r == row or c == col or abs(r - row) == abs(c - col):
                return False
        return True

    def _solve_row(self, row, queens):
        if row == self.size:
            yield queens  # full solution
            return

        # Check all *safe* columns in this row
        candidates = [
            (col, self.heuristic(queens + [(row, col)]))
            for col in range(self.size)
            if self.is_safe(queens, row, col)
        ]

        # Greedy: best heuristic first
        candidates.sort(key=lambda x: x[1])

        for col, _ in candidates:
            new_queens = queens + [(row, col)]
            yield new_queens                     # step: place queen
            yield from self._solve_row(row + 1, new_queens)
            yield queens                         # step: backtrack (remove queen)
