from abc import ABC, abstractmethod
from chessbackend.infrastructure import entity
from typing import NamedTuple, Tuple, Optional
import enum
import copy

class Position(NamedTuple):
  x: int
  y: int

class Colour(enum.Enum):
  WHITE = "white"
  BLACK = "black"

class Move(NamedTuple):
  source: Position
  target: Position

class Movement(ABC):
  @abstractmethod
  def is_move_possible(self, move: Move, figures: Tuple["Figure", ...]) -> bool:
    pass

  def execute_move(self, move: Move, figures: Tuple["Figure", ...]) -> Tuple["Figure", ...]:
    figure = _get_figure_at_position(figures, move.source)
    moved_figure = copy.copy(figure)
    moved_figure.position = move.target
    untouched_figures = tuple(fig for fig in figures if fig.position != move.source and fig.position != move.target)
    return untouched_figures + (moved_figure,)
  
class PawnCaptureMovement(Movement):
  def is_move_possible(self, move: Move, figures: Tuple["Figure", ...]) -> bool:
    source_figure = _get_figure_at_position(figures, move.source)
    target_figure = _get_figure_at_position(figures, move.target)

    # Must capture something.
    if not target_figure:
      return False

    # Cannot capture same color.
    if target_figure.colour == source_figure.colour:
      return False
    
    allowed_direction = 1 if source_figure.colour == Colour.WHITE else -1
    moves_one_field_forward = move.target.y == move.source.y + allowed_direction

    x_diff = abs(move.target.x - move.source.x)
    move_one_field_to_side = x_diff == 1
    return moves_one_field_forward and move_one_field_to_side


class PawnForwardMovement(Movement):
  def is_move_possible(self, move: Move, figures: Tuple["Figure", ...]) -> bool:
    source_figure = _get_figure_at_position(figures, move.source)
    target_figure = _get_figure_at_position(figures, move.target)

    # Cannot beat figure of same colour.
    if target_figure is not None:
      return False
    
    if move.source.x != move.target.x:
      return False

    # Regular movement.
    allowed_direction = 1 if source_figure.colour == Colour.WHITE else -1
    if move.target.y == move.source.y + allowed_direction:
      return True
    
    # White moves two field foward from start.
    if source_figure.colour == Colour.WHITE:
      jump_over_field_is_free = _get_figure_at_position(figures, Position(move.source.x, 2)) is None
      return move.source.y == 1 and move.target.y == 3 and jump_over_field_is_free

    # White moves two field foward from start.
    if source_figure.colour == Colour.BLACK:
      jump_over_field_is_free = _get_figure_at_position(figures, Position(move.source.x, 5)) is None
      return move.source.y == 6 and move.target.y == 4 and jump_over_field_is_free

    return False


class LinearMovement(Movement):
  def is_move_possible(self, move: Move, figures: Tuple["Figure", ...]) -> bool:
    source_figure = _get_figure_at_position(figures, move.source)
    target_figure = _get_figure_at_position(figures, move.target)

    # Cannot beat figure of same colour.
    if target_figure and target_figure.colour == source_figure.colour:
      return False

    # If vertical, vertical path must be free.
    vertical_move = move.source.x == move.target.x and move.source.y != move.target.y
    if vertical_move:
      y_values = (move.source.y, move.target.y)
      for y in range(min(y_values) + 1, max(y_values)):
        if _get_figure_at_position(figures, Position(move.source.x, y)) is not None:
          return False
      return True

    # If horizontal, horizontal path must be free.
    horizontal_move = move.source.x != move.target.x and move.source.y == move.target.y
    if horizontal_move:
      x_values = (move.source.x, move.target.x)
      for x in range(min(x_values) + 1, max(x_values)):
        if _get_figure_at_position(figures, Position(x, move.source.y)) is not None:
          return False
      return True

    return False


class KingRegularMovement(Movement):
  def is_move_possible(self, move: Move, figures: Tuple["Figure", ...]) -> bool:
    source_figure = _get_figure_at_position(figures, move.source)
    target_figure = _get_figure_at_position(figures, move.target)

    # Cannot beat figure of same colour.
    if target_figure and target_figure.colour == source_figure.colour:
      return False
    
    x_diff = abs(move.target.x - move.source.x)
    y_diff = abs(move.target.y - move.source.y)
    did_move = x_diff > 0 or y_diff > 0
    return did_move and x_diff <= 1 and y_diff <= 1


class DiagonalMovement(Movement):
  def is_move_possible(self, move: Move, figures: Tuple["Figure", ...]) -> bool:
    source_figure = _get_figure_at_position(figures, move.source)
    target_figure = _get_figure_at_position(figures, move.target)

    # Cannot beat figure of same colour.
    if target_figure and target_figure.colour == source_figure.colour:
      return False

    x_diff = abs(move.target.x - move.source.x)
    y_diff = abs(move.target.y - move.source.y)
    
    # Figure must move.
    if x_diff == 0 or y_diff == 0:
      return False
    
    # Figure must move diagonally.
    if x_diff != y_diff:
      return False
    
    # Path must be free.
    x_values = (move.source.x, move.target.x)
    y_values = (move.source.y, move.target.y)
    for x in range(min(x_values) + 1, max(x_values)):
      for y in range(min(y_values) + 1, max(y_values)):
        if _get_figure_at_position(figures, Position(x, y)) is not None:
          return False
    return True


class KnightMovement(Movement):
  def is_move_possible(self, move: Move, figures: Tuple["Figure", ...]) -> bool:
    source_figure = _get_figure_at_position(figures, move.source)
    target_figure = _get_figure_at_position(figures, move.target)

    # Cannot beat figure of same colour.
    if target_figure and target_figure.colour == source_figure.colour:
      return False

    x_diff = abs(move.target.x - move.source.x)
    y_diff = abs(move.target.y - move.source.y)
    return x_diff == 2 and y_diff == 1 or x_diff == 1 and y_diff == 2
  

class Figure:
  def __init__(self, colour: Colour, position: Position, movements: Tuple[Movement, ...], name: str):
    self.colour = colour
    self.position = position
    self._movements = movements
    self.name = name
  
  def is_move_possible(self, move: Move, figures: Tuple["Figure", ...]) -> bool:
    return any(movement.is_move_possible(move, figures) for movement in self._movements)
  
  def execute_move(self, move: Move, figures: Tuple["Figure", ...]) -> Tuple["Figure", ...]:
    possible_movement = None
    for movement in self._movements:
      if movement.is_move_possible(move, figures):
        possible_movement = movement
    assert possible_movement is not None
    return possible_movement.execute_move(move, figures)
  
  def __copy__(self):
    return Figure(
      self.colour,
      self.position,
      self._movements,
      self.name
    )
  

class FigureFactory:
  @staticmethod
  def create_queen(colour: Colour, position: Position):
    movements = (
      LinearMovement(),
      DiagonalMovement(),
    )
    return Figure(colour, position, movements, "Queen")
  
  @staticmethod
  def create_rook(colour: Colour, position: Position):
    movements = (
      LinearMovement(),
    )
    return Figure(colour, position, movements, "Rook")
  
  @staticmethod
  def create_bishop(colour: Colour, position: Position):
    movements = (
      DiagonalMovement(),
    )
    return Figure(colour, position, movements, "Bishop")
  
  @staticmethod
  def create_knight(colour: Colour, position: Position):
    movements = (
      KnightMovement(),
    )
    return Figure(colour, position, movements, "Knight")
  
  @staticmethod
  def create_king(colour: Colour, position: Position):
    movements = (
      KingRegularMovement(),
    )
    return Figure(colour, position, movements, "King")

  @staticmethod
  def create_pawn(colour: Colour, position: Position):
    movements = (
      PawnForwardMovement(),
      PawnCaptureMovement(),
    )
    return Figure(colour, position, movements, "Pawn")


def _get_figure_at_position(figures: Tuple[Figure, ...], position: Position) -> Optional[Figure]:
  for figure in figures:
    if figure.position == position:
      return figure
  return None


def build_default_figures() -> Tuple[Figure, ...]:
  figures = []
  figures.extend([
    FigureFactory.create_rook(Colour.BLACK, Position(0, 7)),
    FigureFactory.create_knight(Colour.BLACK, Position(1, 7)),
    FigureFactory.create_bishop(Colour.BLACK, Position(2, 7)),
    FigureFactory.create_queen(Colour.BLACK, Position(3, 7)),
    FigureFactory.create_king(Colour.BLACK, Position(4, 7)),
    FigureFactory.create_bishop(Colour.BLACK, Position(5, 7)),
    FigureFactory.create_knight(Colour.BLACK, Position(6, 7)),
    FigureFactory.create_rook(Colour.BLACK, Position(7, 7)),
  ])
  for x in range(8):
    figures.append(
      FigureFactory.create_pawn(Colour.BLACK, Position(x, 6))
    )

  figures.extend([
    FigureFactory.create_rook(Colour.WHITE, Position(0, 0)),
    FigureFactory.create_knight(Colour.WHITE, Position(1, 0)),
    FigureFactory.create_bishop(Colour.WHITE, Position(2, 0)),
    FigureFactory.create_queen(Colour.WHITE, Position(3, 0)),
    FigureFactory.create_king(Colour.WHITE, Position(4, 0)),
    FigureFactory.create_bishop(Colour.WHITE, Position(5, 0)),
    FigureFactory.create_knight(Colour.WHITE, Position(6, 0)),
    FigureFactory.create_rook(Colour.WHITE, Position(7, 0)),
  ])
  for x in range(8):
    figures.append(
      FigureFactory.create_pawn(Colour.WHITE, Position(x, 1))
    )
  return tuple(figures)

class Game(entity.Entity):
  def __init__(self, figures: Tuple[Figure, ...], in_turn = Colour.WHITE, id: Optional[int] = None):
    super().__init__(id)
    self.in_turn = in_turn
    # TODO: pass board as argument instead
    self.figures = figures
  
  def is_move_possible(self, move: Move) -> bool:
    figure_to_move = _get_figure_at_position(self.figures, move.source)

    if figure_to_move is None:
      return False

    valid_figure_move = figure_to_move.is_move_possible(move, self.figures)
    outside_of_board = _is_outside_board(move.target)
    right_colour = figure_to_move.colour == self.in_turn
    return right_colour and valid_figure_move and not outside_of_board

  def make_move(self, move: Move):
    if not self.is_move_possible(move):
      raise ValueError("Invalid move")
    figure_to_move = _get_figure_at_position(self.figures, move.source)
    self.figures = figure_to_move.execute_move(move, self.figures)
    self._toggle_in_turn()
  
  def get_all_target_positions(self, source_position: Position) -> Tuple[Position, ...]:
    size_x = 8 # TODO: constants
    size_y = 8
    all_target_positions = []
    for x in range(size_x):
      for y in range(size_y):
        target_position = Position(x, y)
        if self.is_move_possible(Move(source_position, target_position)):
          all_target_positions.append(target_position)
    return tuple(all_target_positions)
  
  def _toggle_in_turn(self):
    if self.in_turn == Colour.WHITE:
      self.in_turn = Colour.BLACK
    else:
      self.in_turn = Colour.WHITE


def _is_outside_board(position: Position):
  return position.x < 0 or position.y < 0 or position.x > 7 or position.y > 7