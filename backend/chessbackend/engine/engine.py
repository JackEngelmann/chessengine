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


class Game(entity.Entity):
  def __init__(self, size = (8, 8), in_turn = Colour.WHITE, id: Optional[int] = None):
    super().__init__(id)
    self.in_turn = in_turn
    self.figures = tuple()
    self.size = size
  
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

