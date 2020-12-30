from typing import Tuple
from chessbackend.engine import engine


class Game:
  def __init__(self, figures: Tuple[engine.Figure, ...], in_turn = engine.Colour.WHITE):
    self.in_turn = in_turn
    self.figures = figures
  
  def is_move_possible(self, move: engine.Move) -> bool:
    figure_to_move = engine.get_figure_at_position(self.figures, move.source)

    if figure_to_move is None:
      return False

    valid_figure_move = figure_to_move.is_move_possible(move, self.figures)
    outside_of_board = _is_outside_board(move.target)
    right_colour = figure_to_move.colour == self.in_turn
    return right_colour and valid_figure_move and not outside_of_board

  def make_move(self, move: engine.Move):
    if not self.is_move_possible(move):
      raise ValueError("Invalid move")
    figure_to_move = engine.get_figure_at_position(self.figures, move.source)
    self.figures = figure_to_move.execute_move(move, self.figures)
    self._toggle_in_turn()
  
  def get_all_target_positions(self, source_position: engine.Position) -> Tuple[engine.Position, ...]:
    size_x = 8 # TODO: constants
    size_y = 8
    all_target_positions = []
    for x in range(size_x):
      for y in range(size_y):
        target_position = engine.Position(x, y)
        if self.is_move_possible(engine.Move(source_position, target_position)):
          all_target_positions.append(target_position)
    return tuple(all_target_positions)
  
  def _toggle_in_turn(self):
    if self.in_turn == engine.Colour.WHITE:
      self.in_turn = engine.Colour.BLACK
    else:
      self.in_turn = engine.Colour.WHITE


def _is_outside_board(position: engine.Position):
  return position.x < 0 or position.y < 0 or position.x > 7 or position.y > 7

