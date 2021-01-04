from chessbackend import engine


class BoardRenderer:
    def __init__(self, game: engine.Game):
        self._game = game

    def render(self):
        grid = []
        for x in range(self._game.size[0]):
            row = []
            for y in range(self._game.size[0]):
                row.append("")
            grid.append(row)
        for fig in self._game.figures:
            x, y = fig.position
            grid[y][x] = f"({x},{y}) {fig.name} ({fig.colour.value[0]})"
        for row in grid:
            for cell in row:
                content = cell.ljust(18)
                print(f"{content}|", end="")
            print("")
