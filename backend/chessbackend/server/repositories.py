from typing import Tuple
from chessbackend import engine

# TODO: use dataclass (would need to update python to 3.7)
# TODO: use db

class GameDataModel:
    def __init__(self, id: int, size: Tuple[int, int], in_turn: str):
        self.id = id
        self.size = size
        self.in_turn = in_turn
    

class FigureDataModel:
    def __init__(self, id: int, colour: str, position: Tuple[int, int], game_id: int, figure_type: str):
        self.id = id
        self.colour = colour
        self.position = position
        self.game_id = game_id
        self.figure_type = figure_type

class GameRepository:
    def __init__(self):
        self._games = []
    
    def add(self, game: engine.Game):
        game.id = len(self._games)
        game_data_model = GameDataModel(
            game.id,
            game.size,
            game.in_turn
        )
        self._games.append(game)
    
    def update(self, game: engine.Game):
        for game_data_model in self._games:
            if game_data_model.id == game.id:
                game_data_model.size = game.size
                game_data_model.in_turn = game.in_turn.value
    
    def get(self, game_id: int) -> engine.Game:
        for game_data_model in self._games:
            if game_data_model.id == game_id:
                return engine.Game(
                    game_data_model.size,
                    engine.Colour(game_data_model.in_turn),
                    game_data_model.id,
                )
        # TODO
        raise ValueError("Not found")
    
    def clear(self):
        self._games = []

class FigureRepository:
    def __init__(self):
        self._figures = []
    
    def add(self, figure: engine.Figure):
        figure.id = len(self._figures)
        figure_data_model = FigureDataModel(
            figure.id,
            figure.colour,
            figure.position,
            figure.game.id,
            "King" # TODO
        )
        self._figures.append(figure_data_model)
    
    def update(self, figure: engine.Figure):
        for figure_data_model in self._figures:
            if figure_data_model.id == figure.id:
                figure_data_model.colour = figure.colour
                figure_data_model.position = figure.position
                if figure.game:
                    figure_data_model.game_id = figure.game.id
                # TODO
                figure_data_model.type = 'King'
    
    def get(self, figure_id: int) -> engine.Figure:
        for figure_data_model in self._figures:
            if figure_data_model.id == figure_id:
                # TODO
                if figure_data_model.figure_type == 'King':
                    return engine.King(
                        figure_data_model.colour,
                        figure_data_model.position,
                        figure_data_model.id,
                    )
                
        # TODO
        raise ValueError("Not found")

    def get_game_figures(self, game_id: int) -> Tuple[engine.Figure, ...]:
        game_figures = []
        for figure_data_model in self._figures:
            if figure_data_model.game_id == game_id:
                game_figures.append(self.get(figure_data_model.id))
        return tuple(game_figures)

    def clear(self):
        self._figures = []