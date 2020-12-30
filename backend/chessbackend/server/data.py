import uuid
from chessbackend import engine
from typing import Tuple, Type

class GameDataAdapter(engine.Game):
  def __init__(self, figures: Tuple[engine.Figure, ...], in_turn = engine.Colour.WHITE, id=str):
      super().__init__(figures, in_turn)
      self.id = id


class GameDataAdapterFactory:
  def create(self, in_turn = engine.Colour.WHITE):
      return GameDataAdapter(
          tuple(),
          in_turn,
          str(uuid.uuid4())
      )


class FigureDataAdapter(engine.Figure):
    def __init__(
        self,
        colour: engine.Colour,
        position: engine.Position,
        movements: Tuple[engine.Movement, ...],
        name: str,
        id: str,
        game_id: str
    ):
        super().__init__(
            colour,
            position,
            movements,
            name
        )
        self.id = id
        self.game_id = game_id

    def __copy__(self):
        return FigureDataAdapter(
            self.colour,
            self.position,
            self._movements,
            self.name,
            self.id,
            self.game_id
        )


class FigureDataAdapterFactory(Type[engine.FigureFactory]):
    def __init__(self, game_id: str):
        self._game_id = game_id
    
    def create(
        self,
        colour: engine.Colour,
        position: engine.Position,
        movements: Tuple[engine.Movement, ...],
        name: str
    ):
        return FigureDataAdapter(
            colour,
            position,
            movements,
            name,
            str(uuid.uuid4()),
            self._game_id,
        )


class GameRepository:
    def __init__(self):
        self._games = []
    
    def add(self, game: GameDataAdapter):
        self._games.append(game)
    
    def update(self, game: engine.Game):
        pass
    
    def get(self, game_id: int) -> engine.Game:
        for game in self._games:
            if game.id == game_id:
                return game
        raise ValueError("Not found")
    
    def clear(self):
        self._games = []

class FigureRepository:
    def __init__(self):
        self._figures = []
    
    def add(self, figure: FigureDataAdapter):
        self._figures.append(figure)
    
    def update(self, figure: FigureDataAdapter):
        self.delete(figure.id)
        self._figures.append(figure)
    
    def get(self, figure_id: int) -> FigureDataAdapter:
        for figure in self._figures:
            if figure.id == figure_id:
                return figure
        raise ValueError("Not found")

    def get_game_figures(self, game_id: str) -> Tuple[FigureDataAdapter, ...]:
        game_figures = []
        for figure in self._figures:
            if figure.game_id == game_id:
                game_figures.append(figure)
        return tuple(game_figures)

    def clear(self):
        self._figures = []
    
    def delete(self, figure_id: str):
        self._figures = list(
            fig
            for fig in self._figures
            if fig.id != figure_id
        )

