from typing import Tuple
from chessbackend.engine import engine


class Game:
  def __init__(self, figures: Tuple[engine.Figure, ...], in_turn = engine.Colour.WHITE):
    self.in_turn = in_turn
    self.figures = figures
  
  def is_move_possible(self, move: engine.Move) -> bool:
    return _is_move_possible(move, self.figures, self.in_turn)

  def make_move(self, move: engine.Move):
    new_figures = _make_move(move, self.figures, self.in_turn)
    self.figures = new_figures
    self.in_turn = _get_opposite_color(self.in_turn)
  
  def get_all_target_positions(self, source_position: engine.Position) -> Tuple[engine.Position, ...]:
    if self.is_check():
      target_positions_resolving_check = []
      for target_position in _get_all_target_positions(source_position, self.figures, self.in_turn):
        new_figures = _make_move(
          engine.Move(source_position, target_position),
          self.figures, self.in_turn
        )
        if not _is_check(new_figures, self.in_turn):
          target_positions_resolving_check.append(target_position)
      return tuple(target_positions_resolving_check)
      
    return _get_all_target_positions(source_position, self.figures, self.in_turn)
  
  def is_check(self) -> bool:
    return _is_check(self.figures, self.in_turn)
  
  def is_check_mate(self) -> bool:
    if not self.is_check():
      return False
    for move in _get_all_possible_moves(self.figures, self.in_turn):
      new_figures = _make_move(move, self.figures, self.in_turn)
      if not _is_check(new_figures, self.in_turn):
        return False
    return True


def _is_outside_board(position: engine.Position):
  return position.x < 0 or position.y < 0 or position.x > 7 or position.y > 7


def _is_move_possible(move: engine.Move, figures: Tuple[engine.Figure, ...], in_turn: engine.Colour):
  figure_to_move = engine.get_figure_at_position(figures, move.source)

  if figure_to_move is None:
    return False

  valid_figure_move = figure_to_move.is_move_possible(move, figures)
  outside_of_board = _is_outside_board(move.target)
  right_colour = figure_to_move.colour == in_turn
  return right_colour and valid_figure_move and not outside_of_board


def _make_move(move: engine.Move, figures: Tuple[engine.Figure, ...], in_turn: engine.Colour):
  if not _is_move_possible(move, figures, in_turn):
    raise ValueError("Invalid move")
  figure_to_move = engine.get_figure_at_position(figures, move.source)
  new_figures = figure_to_move.execute_move(move, figures)
  return new_figures


def _get_all_target_positions(source_position: engine.Position, figures: Tuple[engine.Figure, ...], in_turn: engine.Colour) -> Tuple[engine.Position, ...]:
  size_x = 8 # TODO: constants
  size_y = 8
  all_target_positions = []
  for x in range(size_x):
    for y in range(size_y):
      target_position = engine.Position(x, y)
      move = engine.Move(source_position, target_position)
      if _is_move_possible(move, figures, in_turn):
        all_target_positions.append(target_position)
  return tuple(all_target_positions)


def _get_all_possible_moves(figures: Tuple[engine.Figure, ...], in_turn: engine.Colour) -> Tuple[engine.Move, ...]:
  possible_moves = []
  for figure in figures:
    for target_position in _get_all_target_positions(figure.position, figures, in_turn):
      move = engine.Move(
        figure.position,
        target_position,
      )
      possible_moves.append(move)
  return possible_moves


# TODO: move
def _get_opposite_color(colour: engine.Colour):
  if colour == engine.Colour.WHITE:
    return engine.Colour.BLACK
  else:
    return engine.Colour.WHITE


def _is_check(figures: Tuple[engine.Figure, ...], in_turn: engine.Colour):
  king = next(fig for fig in figures if fig.name == 'King' and fig.colour == in_turn)
  opposite_color = _get_opposite_color(in_turn)
  for figure in figures:
    if king.position in _get_all_target_positions(figure.position, figures, opposite_color):
      return True
  return False