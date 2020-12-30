from chessbackend.engine import newengine
import unittest
import pytest

@pytest.mark.parametrize("create_figure", (
  newengine.FigureFactory.create_queen,
  newengine.FigureFactory.create_rook,
))
class TestLinearMovements:
  @staticmethod
  def test_horizontal_move(create_figure):
    moving_figure = create_figure(newengine.Colour.WHITE, newengine.Position(3, 3))
    move = newengine.Move(
      newengine.Position(3, 3),
      newengine.Position(3, 4)
    )
    assert moving_figure.is_move_possible(move, (moving_figure,))
    moving_figure, *_ = moving_figure.execute_move(move, (moving_figure,))
    assert moving_figure.position == move.target

  @staticmethod
  def test_vertical_move(create_figure):
    moving_figure = create_figure(newengine.Colour.WHITE, newengine.Position(3, 3))
    move = newengine.Move(
      newengine.Position(3, 3),
      newengine.Position(4, 3)
    )
    assert moving_figure.is_move_possible(move, (moving_figure,))
    moving_figure, *_ = moving_figure.execute_move(move, (moving_figure,))
    assert moving_figure.position == move.target

  @staticmethod
  def test_illegal_move(create_figure):
    moving_figure = create_figure(newengine.Colour.WHITE, newengine.Position(3, 3))
    move = newengine.Move(
      newengine.Position(3, 3),
      newengine.Position(4, 5)
    )
    assert not moving_figure.is_move_possible(move, (moving_figure,))

  @staticmethod
  def test_beat_figure(create_figure):
    moving_figure = create_figure(newengine.Colour.WHITE, newengine.Position(3, 3))
    fig_opposite_color = create_figure(newengine.Colour.BLACK, newengine.Position(4, 3))
    move = newengine.Move(
      newengine.Position(3, 3),
      newengine.Position(4, 3)
    )
    figures = (moving_figure, fig_opposite_color)
    assert moving_figure.is_move_possible(move, figures)
    figures_after_move = moving_figure.execute_move(move, figures)
    assert len(figures_after_move) == 1
    moving_figure, *_ = figures_after_move
    assert moving_figure.position == move.target

  @staticmethod
  def test_cannot_beat_figure_of_same_color(create_figure):
    moving_figure = create_figure(newengine.Colour.WHITE, newengine.Position(3, 3))
    fig_same_color = create_figure(newengine.Colour.WHITE, newengine.Position(4, 3))
    move = newengine.Move(
      newengine.Position(3, 3),
      newengine.Position(4, 3)
    )
    figures = (moving_figure, fig_same_color)
    assert not moving_figure.is_move_possible(move, figures)

  @staticmethod
  def test_cannot_jump_over_figures(create_figure):
    moving_figure = create_figure(newengine.Colour.WHITE, newengine.Position(3, 3))
    fig_in_vertical_way = create_figure(newengine.Colour.WHITE, newengine.Position(4, 3))
    fig_in_horizontal_way = create_figure(newengine.Colour.WHITE, newengine.Position(3, 4))
    vertical_move = newengine.Move(
      newengine.Position(3, 3),
      newengine.Position(5, 3)
    )
    horizontal_move = newengine.Move(
      newengine.Position(3, 3),
      newengine.Position(3, 5)
    )
    figures = (moving_figure, fig_in_vertical_way, fig_in_horizontal_way)
    assert not moving_figure.is_move_possible(vertical_move, figures)
    assert not moving_figure.is_move_possible(horizontal_move, figures)
 

@pytest.mark.parametrize("create_figure", (
  newengine.FigureFactory.create_queen,
  newengine.FigureFactory.create_bishop,
))
class TestLinearMovements:
  @staticmethod
  def test_diagonal_move(create_figure):
    moving_figure = create_figure(newengine.Colour.WHITE, newengine.Position(3, 3))
    move = newengine.Move(
      newengine.Position(3, 3),
      newengine.Position(5, 5)
    )
    assert moving_figure.is_move_possible(move, (moving_figure,))
    moving_figure, *_ = moving_figure.execute_move(move, (moving_figure,))
    assert moving_figure.position == move.target

  @staticmethod
  def test_illegal_move(create_figure):
    moving_figure = create_figure(newengine.Colour.WHITE, newengine.Position(3, 3))
    move = newengine.Move(
      newengine.Position(3, 3),
      newengine.Position(4, 5)
    )
    assert not moving_figure.is_move_possible(move, (moving_figure,))

  @staticmethod
  def test_beat_figure(create_figure):
    moving_figure = create_figure(newengine.Colour.WHITE, newengine.Position(3, 3))
    fig_opposite_color = create_figure(newengine.Colour.BLACK, newengine.Position(4, 4))
    move = newengine.Move(
      newengine.Position(3, 3),
      newengine.Position(4, 4)
    )
    figures = (moving_figure, fig_opposite_color)
    assert moving_figure.is_move_possible(move, figures)
    figures_after_move = moving_figure.execute_move(move, figures)
    assert len(figures_after_move) == 1
    moving_figure, *_ = figures_after_move
    assert moving_figure.position == move.target

  @staticmethod
  def test_cannot_beat_figure_of_same_color(create_figure):
    moving_figure = create_figure(newengine.Colour.WHITE, newengine.Position(3, 3))
    fig_same_color = create_figure(newengine.Colour.WHITE, newengine.Position(4, 4))
    move = newengine.Move(
      newengine.Position(3, 3),
      newengine.Position(4, 4)
    )
    figures = (moving_figure, fig_same_color)
    assert not moving_figure.is_move_possible(move, figures)

  @staticmethod
  def test_cannot_jump_over_figures(create_figure):
    moving_figure = create_figure(newengine.Colour.WHITE, newengine.Position(3, 3))
    fig_in_way = create_figure(newengine.Colour.WHITE, newengine.Position(4, 4))
    move = newengine.Move(
      newengine.Position(3, 3),
      newengine.Position(5, 5)
    )
    figures = (moving_figure, fig_in_way)
    assert not moving_figure.is_move_possible(move, figures)

class TestKnightMovements:
  @pytest.mark.parametrize("source_position, target_position", (
    (
      newengine.Position(4, 4),
      newengine.Position(2, 3),
    ),
    (
      newengine.Position(4, 4),
      newengine.Position(3, 2),
    ),
    (
      newengine.Position(4, 4),
      newengine.Position(6, 5),
    ),
  ))
  def test_knight_movement(self, source_position, target_position):
    moving_figure = newengine.FigureFactory.create_knight(
      newengine.Colour.WHITE, source_position,
    )
    move = newengine.Move(
      source_position,
      target_position
    )
    figures = (moving_figure,)
    assert moving_figure.is_move_possible(move, figures)
    moving_figure, *_ = moving_figure.execute_move(move, figures)
    assert moving_figure.position == target_position


  @pytest.mark.parametrize("source_position, target_position", (
    (
      newengine.Position(4, 4),
      newengine.Position(4, 5),
    ),
    (
      newengine.Position(4, 4),
      newengine.Position(3, 3),
    ),
    (
      newengine.Position(4, 4),
      newengine.Position(7, 4),
    ),
  ))
  def test_invalid_knight_movement(self, source_position, target_position):
    moving_figure = newengine.FigureFactory.create_knight(
      newengine.Colour.WHITE, source_position,
    )
    move = newengine.Move(
      source_position,
      target_position
    )
    figures = (moving_figure,)
    assert not moving_figure.is_move_possible(move, figures)

  @staticmethod
  def test_cannot_beat_figure_of_same_color():
    moving_figure = newengine.FigureFactory.create_knight(newengine.Colour.WHITE, newengine.Position(4, 4))
    fig_same_color = newengine.FigureFactory.create_knight(newengine.Colour.WHITE, newengine.Position(2, 3))
    move = newengine.Move(
      newengine.Position(4, 4),
      newengine.Position(2, 3),
    )
    figures = (moving_figure, fig_same_color)
    assert not moving_figure.is_move_possible(move, figures)

  @staticmethod
  def test_beat_figure():
    moving_figure = newengine.FigureFactory.create_knight(newengine.Colour.WHITE, newengine.Position(4, 4))
    fig_opposite_color = newengine.FigureFactory.create_knight(newengine.Colour.BLACK, newengine.Position(2, 3))
    move = newengine.Move(
      newengine.Position(4, 4),
      newengine.Position(2, 3),
    )
    figures = (moving_figure, fig_opposite_color)
    assert moving_figure.is_move_possible(move, figures)
    figures_after_move = moving_figure.execute_move(move, figures)
    assert len(figures_after_move) == 1
    moving_figure, *_ = figures_after_move
    assert moving_figure.position == move.target


class TestKingRegularMovements:
  @pytest.mark.parametrize("source_position, target_position", (
    (
      newengine.Position(4, 4),
      newengine.Position(4, 5),
    ),
    (
      newengine.Position(4, 4),
      newengine.Position(5, 4),
    ),
    (
      newengine.Position(4, 4),
      newengine.Position(5, 5),
    ),
    (
      newengine.Position(4, 4),
      newengine.Position(3, 3),
    ),
  ))
  def test_king_movement(source_position, target_position):
    moving_figure = newengine.FigureFactory.create_king(newengine.Colour.WHITE, source_position)
    move = newengine.Move(
      source_position,
      target_position
    )
    figures = (moving_figure,)
    assert moving_figure.is_move_possible(move, figures)
    moving_figure, *_ = moving_figure.execute_move(move, figures)
    assert moving_figure.position == target_position

  @pytest.mark.parametrize("source_position, target_position", (
    (
      newengine.Position(4, 4),
      newengine.Position(4, 4),
    ),
    (
      newengine.Position(4, 4),
      newengine.Position(6, 4),
    ),
    (
      newengine.Position(4, 4),
      newengine.Position(6, 6),
    ),
    (
      newengine.Position(4, 4),
      newengine.Position(3, 2),
    ),
  ))
  def test_king_movement(self, source_position, target_position):
    moving_figure = newengine.FigureFactory.create_king(newengine.Colour.WHITE, source_position)
    move = newengine.Move(
      source_position,
      target_position
    )
    figures = (moving_figure,)
    assert not moving_figure.is_move_possible(move, figures)

class TestPawnForwardMovement:
  @pytest.mark.parametrize("colour,source_position,target_position", (
    (
      newengine.Colour.WHITE,
      newengine.Position(2, 2),
      newengine.Position(2, 3),
    ),
    (
      newengine.Colour.BLACK,
      newengine.Position(2, 3),
      newengine.Position(2, 2),
    ),
    ( # Move two field forward from start field (white).
      newengine.Colour.WHITE,
      newengine.Position(2, 1),
      newengine.Position(2, 3),
    ),
    ( # Move two field forward from start field (white).
      newengine.Colour.BLACK,
      newengine.Position(2, 6),
      newengine.Position(2, 4),
    ),
  ))
  def test_pawn_move_forward(self, colour, source_position, target_position):
    moving_figure = newengine.FigureFactory.create_pawn(colour, source_position)
    move = newengine.Move(
      source_position,
      target_position
    )
    figures = (moving_figure,)
    assert moving_figure.is_move_possible(move, figures)

  @pytest.mark.parametrize("colour,source_position,target_position", (
    (
      newengine.Colour.WHITE,
      newengine.Position(2, 3),
      newengine.Position(2, 2),
    ),
    (
      newengine.Colour.WHITE,
      newengine.Position(2, 2),
      newengine.Position(3, 2),
    ),
    (
      newengine.Colour.BLACK,
      newengine.Position(2, 2),
      newengine.Position(2, 3),
    ),
    (
      newengine.Colour.BLACK,
      newengine.Position(2, 2),
      newengine.Position(3, 2),
    ),
  ))
  def test_pawn_invalid_move_forward(self, colour, source_position, target_position):
    moving_figure = newengine.FigureFactory.create_pawn(colour, source_position)
    move = newengine.Move(
      source_position,
      target_position
    )
    figures = (moving_figure,)
    assert not moving_figure.is_move_possible(move, figures)
  
  @staticmethod
  def test_pawn_cannot_capture_forward():
    moving_figure = newengine.FigureFactory.create_pawn(
      newengine.Colour.WHITE,
      newengine.Position(2, 2),
    )
    figure_in_way = newengine.FigureFactory.create_pawn(
      newengine.Colour.BLACK,
      newengine.Position(2, 3),
    )
    move = newengine.Move(
      moving_figure.position,
      figure_in_way.position
    )
    assert moving_figure.is_move_possible(move, (moving_figure,))
    assert not moving_figure.is_move_possible(move, (moving_figure, figure_in_way))

class TestPawnCaptureMovement:
  @staticmethod
  def test_pawn_capture_movement_white():
    moving_figure = newengine.FigureFactory.create_pawn(
      newengine.Colour.WHITE,
      newengine.Position(2, 2),
    )
    fig_to_capture = newengine.FigureFactory.create_pawn(
      newengine.Colour.BLACK,
      newengine.Position(3, 3),
    )
    move = newengine.Move(
      moving_figure.position,
      fig_to_capture.position
    )
    figures = (moving_figure, fig_to_capture)
    assert moving_figure.is_move_possible(move, figures)
    assert not moving_figure.is_move_possible(move, (moving_figure,))

    figures_after_move = moving_figure.execute_move(move, figures)
    assert len(figures_after_move) == 1
    moving_figure, *_ = figures_after_move
    assert moving_figure.position == move.target

  @staticmethod
  def test_pawn_capture_movement_black():
    moving_figure = newengine.FigureFactory.create_pawn(
      newengine.Colour.BLACK,
      newengine.Position(3, 3),
    )
    fig_to_capture = newengine.FigureFactory.create_pawn(
      newengine.Colour.WHITE,
      newengine.Position(2, 2),
    )
    move = newengine.Move(
      moving_figure.position,
      fig_to_capture.position
    )
    figures = (moving_figure, fig_to_capture)
    assert moving_figure.is_move_possible(move, figures)
    assert not moving_figure.is_move_possible(move, (moving_figure,))

    figures_after_move = moving_figure.execute_move(move, figures)
    assert len(figures_after_move) == 1
    moving_figure, *_ = figures_after_move
    assert moving_figure.position == move.target

def test_build_default_figures():
  figures = newengine.build_default_figures()
  assert isinstance(figures, tuple)
  assert len(figures) == 32
  white_figures = tuple(fig for fig in figures if fig.colour == newengine.Colour.WHITE)
  black_figures = tuple(fig for fig in figures if fig.colour == newengine.Colour.BLACK)
  assert len(black_figures) == len(white_figures)

def test_game_only_fugre_in_turn_can_move():
  black_rook = newengine.FigureFactory.create_rook(newengine.Colour.BLACK, newengine.Position(3, 3))
  white_rook = newengine.FigureFactory.create_rook(newengine.Colour.WHITE, newengine.Position(4, 4))
  figures = (white_rook, black_rook)
  white_in_turn_game = newengine.Game(figures, newengine.Colour.WHITE)
  black_in_turn_game = newengine.Game(figures, newengine.Colour.BLACK)

  move_white_rook = newengine.Move(
    white_rook.position,
    newengine.Position(white_rook.position.x, white_rook.position.y + 1)
  )
  move_black_rook = newengine.Move(
    black_rook.position,
    newengine.Position(black_rook.position.x, black_rook.position.y + 1)
  )

  assert white_in_turn_game.is_move_possible(
    move_white_rook
  )
  assert not white_in_turn_game.is_move_possible(
    move_black_rook
  )

  assert black_in_turn_game.is_move_possible(
    move_black_rook
  )
  assert not black_in_turn_game.is_move_possible(
    move_white_rook
  )
  
def test_game_in_turn_toggles():
  black_rook = newengine.FigureFactory.create_rook(newengine.Colour.BLACK, newengine.Position(3, 3))
  white_rook = newengine.FigureFactory.create_rook(newengine.Colour.WHITE, newengine.Position(4, 4))
  figures = (white_rook, black_rook)
  game = newengine.Game(figures, newengine.Colour.WHITE)
  assert game.in_turn == newengine.Colour.WHITE
  game.make_move(
    newengine.Move(
      newengine.Position(4, 4),
      newengine.Position(4, 5),
    )
  )
  assert game.in_turn == newengine.Colour.BLACK
  game.make_move(
    newengine.Move(
      newengine.Position(3, 3),
      newengine.Position(3, 4),
    )
  )
  assert game.in_turn == newengine.Colour.WHITE

def test_position_equal():
  assert newengine.Position(3, 3) == newengine.Position(3, 3)
  assert newengine.Position(3, 3) != newengine.Position(3, 4)

def test_game_get_all_target_positions():
  king = newengine.FigureFactory.create_king(newengine.Colour.WHITE, newengine.Position(3, 3))
  game = newengine.Game((king,))
  all_target_positions = game.get_all_target_positions(king.position)
  assert len(all_target_positions) == 8
  assert (2, 2) in all_target_positions
  assert (2, 3) in all_target_positions
  assert (2, 4) in all_target_positions
  assert (3, 2) in all_target_positions
  assert (3, 4) in all_target_positions
  assert (4, 2) in all_target_positions
  assert (4, 3) in all_target_positions
  assert (4, 4) in all_target_positions