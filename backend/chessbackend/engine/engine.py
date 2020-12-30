import enum
from typing import NamedTuple, Optional, Tuple
from abc import ABC, abstractmethod
from chessbackend.infrastructure import entity

# TODO: think about how to implement castling, en passant

class Colour(enum.Enum):
  WHITE = "white"
  BLACK = "black"


class Figure(ABC, entity.Entity):
  def __init__(self, colour: Colour, position: Tuple[int, int], id: Optional[int] = None, game: Optional["Game"] = None):
    super().__init__(id)
    self.colour = colour
    self.position = position
    self.game = game

  @abstractmethod
  def is_move_valid(self, new_position) -> bool:
    pass

  @property
  @abstractmethod
  def name(self):
    pass

def get_opposite_color(colour: Colour):
  if colour == Colour.WHITE:
    return Colour.BLACK
  return Colour.WHITE


class King(Figure):
  name = "King"

  def is_move_valid(self, new_position) -> bool:
    x_difference = abs(new_position[0] - self.position[0])
    y_difference = abs(new_position[1] - self.position[1]) 
    return x_difference <= 1 and y_difference <= 1

BoardSize = Tuple[int, int]


class NoFigureError(Exception):
  pass


class InvalidMoveError(Exception):
  pass

class Board:
  def __init__(self, size = (8, 8)):
    self.size = size
    self.figures = tuple()

  def get_figure_at_position(self, position: Tuple[int, int]) -> Optional[Figure]:
    for fig in self.figures:
      if fig.position == position:
        return fig
    return None
  
  def is_occupied(self, position: Tuple[int, int]) -> bool:
    return self.get_figure_at_position(position) is not None
  
  def is_occupied_by_opposite_color(self, position: Tuple[int, int], colour: Colour) -> bool:
    figure = self.get_figure_at_position(position)
    if figure is None:
      return False
    opposite_colour = get_opposite_colour(colour)
    return figure.colour == opposite_colour
  
  def is_occupied_by_same_color(self, position: Tuple[int, int], colour: Colour) -> bool:
    figure = self.get_figure_at_position(position)
    if figure is None:
      return False
    return figure.colour == colour
  
  def make_move(self, from_position: Tuple[int, int], to_position: Tuple[int, int]):
    # this method assumes the validity of the move was already checked
    from_figure = self.get_figure_at_position(from_position)
    from_figure.position = to_position

    to_figure = self.get_figure_at_position(to_position)
    if to_figure:
      self.figures.remove(to_figure)


class Game(entity.Entity):
  def __init__(self, size = (8, 8), in_turn = Colour.WHITE, id: Optional[int] = None):
    super().__init__(id)
    self.in_turn = in_turn
    # TODO: pass board as argument instead
    self.board = Board(size)
  
  def is_move_valid(self, figure_to_move: Figure, to_position: Tuple[int, int]) -> bool:
    same_position = figure_to_move.position == to_position
    right_colour = figure_to_move.colour == self.in_turn
    valid_figure_move = figure_to_move.is_move_valid(to_position)
    outside_of_board = _is_outside_board(to_position, self.size)
    # TODO: move must resolve check if own king is in check.
    # TODO: move must not result in to own king being in check.
    return not same_position and right_colour and valid_figure_move and not outside_of_board

  def make_move(self, from_position: Tuple[int, int], to_position: Tuple[int, int]):
    # Returns True if sucess, else False.

    figure_to_move = self._get_figure_at_position(from_position)

    if figure_to_move is None:
      raise NoFigureError()

    if not self.is_move_valid(figure_to_move, to_position):
      raise InvalidMoveError()

    figure_to_move.position = to_position
    self._toggle_in_turn()
  
  def get_all_valid_moves(self, figure_to_move: Figure) -> Tuple[Tuple[int, int], ...]:
    size_x, size_y = self.size
    valid_moves = []
    for x in range(size_x):
      for y in range(size_y):
        to_position = (x, y)
        if self.is_move_valid(figure_to_move, to_position):
          valid_moves.append(to_position)
    return tuple(valid_moves)
  
  def _toggle_in_turn(self):
    if self.in_turn == Colour.WHITE:
      self.in_turn = Colour.BLACK
    else:
      self.in_turn = Colour.WHITE

  def _get_figure_at_position(self, position: Tuple[int, int]) -> Optional[Figure]:
    for fig in self.figures:
      if fig.position == position:
        return fig
    return None
  
def _is_outside_board(position: Tuple[int, int], board_size: BoardSize):
  return position[0] < 0 or position[1] < 0 or position[0] >= board_size[0] or position[1] >= board_size[1]


class FigureType(enum.Enum):
  KING = "king"

class AddFigureInfo(NamedTuple):
  colour: Colour
  position: Tuple[int, int]
  figure_type: FigureType

class GameBuilder:
  def __init__(self):
    self._size = (8, 8)
    self._in_turn = Colour.WHITE
    self._add_figure_infos = []
  
  def add_figure(self, figure_type: FigureType, position: Tuple[int, int], colour: Colour):
    self._add_figure_infos.append(
      AddFigureInfo(
        colour,
        position,
        figure_type
      )
    )

  def build(self):
    game = Game(
      self._size,
      self._in_turn,
    )

    figures = []
    for info in self._add_figure_infos:
      if info.figure_type == FigureType.KING:
        new_figure = King(
          info.colour,
          info.position,
          None,
          game
        )
      figures.append(new_figure)

    game.figures = tuple(figures)

    return game

def build_default_game():
  game_builder = GameBuilder()
  game_builder.add_figure(
    FigureType.KING, (4, 0), Colour.WHITE,
  )
  game_builder.add_figure(
    FigureType.KING, (4, 7), Colour.BLACK,
  )
  return game_builder.build()
