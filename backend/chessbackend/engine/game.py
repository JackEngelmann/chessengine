from typing import NamedTuple, Optional, Tuple
from chessbackend.engine import colouring
from chessbackend.engine import figure

class NoFigureError(Exception):
  pass

class InvalidMoveError(Exception):
  pass

class NotInTurnError(Exception):
  pass

class OutsideBoardError(Exception):
  pass

BoardSize = Tuple[int, int]

class Game:
  def __init__(self, figures: Tuple[figure.Figure, ...] = tuple(), size = (8, 8)):
    self.in_turn = colouring.Colour.WHITE
    self.figures = figures
    self.size = size

  def make_move(self, from_position: Tuple[int, int], to_position: Tuple[int, int]):
    # Returns True if sucess, else False.

    figure_to_move = self._get_figure_at_position(from_position)

    if from_position == to_position:
      raise InvalidMoveError()

    if figure_to_move is None:
      raise NoFigureError()

    if figure_to_move.colour != self.in_turn:
      raise NotInTurnError()

    if not figure_to_move.is_move_valid(to_position):
      raise InvalidMoveError()

    if _is_outside_board(to_position, self.size):
      raise OutsideBoardError()
    
    # TODO: move must resolve check if own king is in check.
    # TODO: move must not result in to own king being in check.

    figure.position = to_position
    self._toggle_in_turn()
  
  def _toggle_in_turn(self):
    if self.in_turn == colouring.Colour.WHITE:
      self.in_turn = colouring.Colour.BLACK
    else:
      self.in_turn = colouring.Colour.WHITE

  def _get_figure_at_position(self, position: figure.Position) -> Optional[figure.Figure]:
    for fig in self.figures:
      if fig.position == position:
        return fig
    return None
  
def _is_outside_board(position: figure.Position, board_size: BoardSize):
  return position[0] < 0 or position[1] < 0 or position[0] >= board_size[0] or position[1] >= board_size[1]