from chessbackend import engine
import pytest


class TestKing:
  def test_is_move_valid_when_valid(self):
    king = engine.King(engine.Colour.WHITE, (3, 3))
    assert king.is_move_valid((2, 2))
    assert king.is_move_valid((2, 3))
    assert king.is_move_valid((2, 4))

    assert king.is_move_valid((3, 2))
    assert king.is_move_valid((3, 4))

    assert king.is_move_valid((4, 2))
    assert king.is_move_valid((4, 3))
    assert king.is_move_valid((4, 4))

  def test_is_move_valid_when_invalid(self):
    king = engine.King(engine.Colour.WHITE, (3, 3))
    assert not king.is_move_valid((3, 5))
    assert not king.is_move_valid((6, 6))
    assert not king.is_move_valid((5, 3))

def test_afterstart_whiteinturn():
  game_ = engine.Game()
  assert game_.in_turn == engine.Colour.WHITE

def test_defaults():
  game_ = engine.Game()
  assert game_.size == (8, 8)
  assert game_.figures == ()

def test_make_move_success():
  game_builder = engine.GameBuilder()
  game_builder.add_figure(engine.FigureType.KING, (0, 0), engine.Colour.WHITE)
  game = game_builder.build()
  game.make_move((0, 0), (0, 1))

def test_make_move_colour_toggles():
  game_builder = engine.GameBuilder()
  game_builder.add_figure(engine.FigureType.KING, (0, 0), engine.Colour.WHITE)
  game_builder.add_figure(engine.FigureType.KING, (5, 5), engine.Colour.BLACK)
  game = game_builder.build()

  assert game.in_turn == engine.Colour.WHITE
  game.make_move((0, 0), (0, 1))
  assert game.in_turn == engine.Colour.BLACK
  game.make_move((5, 5), (5, 6))
  assert game.in_turn == engine.Colour.WHITE

def test_is_move_valid_not_in_turn():
  game_builder = engine.GameBuilder()
  game_builder.add_figure(engine.FigureType.KING, (0, 0), engine.Colour.BLACK)
  game = game_builder.build()
  with pytest.raises(engine.InvalidMoveError):
    game.make_move((0, 0), (0, 1))

def test_make_move_no_figure():
  game_builder = engine.GameBuilder()
  game_builder.add_figure(engine.FigureType.KING, (0, 0), engine.Colour.BLACK)
  game = game_builder.build()
  with pytest.raises(engine.NoFigureError):
    game.make_move((1, 1), (0, 1))


def test_make_move_outside_board():
  game_builder = engine.GameBuilder()
  game_builder.add_figure(engine.FigureType.KING, (0, 0), engine.Colour.BLACK)
  game_builder.add_figure(engine.FigureType.KING, (7, 7), engine.Colour.BLACK)
  game = game_builder.build()

  with pytest.raises(engine.InvalidMoveError):
    game.make_move((0, 0), (-1, 0))

  with pytest.raises(engine.InvalidMoveError):
    game.make_move((0, 0), (0, -1))

  with pytest.raises(engine.InvalidMoveError):
    game.make_move((7, 7), (7, 8))

  with pytest.raises(engine.InvalidMoveError):
    game.make_move((7, 7), (8, 7))


def test_make_move_same_position_raises_invalid_move():
  game_builder = engine.GameBuilder()
  game_builder.add_figure(engine.FigureType.KING, (0, 0), engine.Colour.WHITE)
  game = game_builder.build()

  with pytest.raises(engine.InvalidMoveError):
    game.make_move((0, 0), (0, 0))


def test_get_all_valid_moves():
  game_builder = engine.GameBuilder()
  game_builder.add_figure(engine.FigureType.KING, (3, 3), engine.Colour.WHITE)
  game = game_builder.build()

  king = game.figures[0]

  valid_moves = game.get_all_valid_moves(king)
  assert len(valid_moves) == 8
  assert (2, 2) in valid_moves
  assert (2, 3) in valid_moves
  assert (2, 4) in valid_moves
  assert (3, 2) in valid_moves
  assert (3, 4) in valid_moves
  assert (4, 2) in valid_moves
  assert (4, 3) in valid_moves
  assert (4, 4) in valid_moves

# TODO: test move not valid
def test_build_empty():
  builder = engine.GameBuilder()
  game = builder.build()
  assert game.figures == tuple()


def test_build_a_king():
  builder = engine.GameBuilder()
  builder.add_figure(engine.FigureType.KING, (0, 0), engine.Colour.WHITE)
  game = builder.build()
  assert len(game.figures) == 1
  assert isinstance(game.figures[0], engine.King)
  assert game.figures[0].colour == engine.Colour.WHITE
