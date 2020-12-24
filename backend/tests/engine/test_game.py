import pytest
import unittest
from chessbackend import engine
from chessbackend.engine import game

def test_afterstart_whiteinturn():
  game_ = engine.Game()
  assert game_.in_turn == engine.Colour.WHITE

def test_defaults():
  game_ = engine.Game()
  assert game_.size == (8, 8)
  assert game_.figures == ()

def test_make_move_success():
  builder = engine.FiguresBuilder(engine.Colour.WHITE)
  builder.add_figure(engine.FigureType.KING, (0, 0))
  figures = builder.build()

  game_ = engine.Game(figures=figures)
  game_.make_move((0, 0), (0, 1))

def test_make_move_colour_toggles():
  builder = engine.FiguresBuilder(engine.Colour.WHITE)
  builder.add_figure(engine.FigureType.KING, (0, 0))
  builder.set_colour(engine.Colour.BLACK)
  builder.add_figure(engine.FigureType.KING, (5, 5))
  figures = builder.build()

  game_ = engine.Game(figures=figures)
  assert game_.in_turn == engine.Colour.WHITE
  game_.make_move((0, 0), (0, 1))
  assert game_.in_turn == engine.Colour.BLACK
  game_.make_move((5, 5), (5, 6))
  assert game_.in_turn == engine.Colour.WHITE

def test_make_move_not_in_turn():
  builder = engine.FiguresBuilder(engine.Colour.BLACK)
  builder.add_figure(engine.FigureType.KING, (0, 0))
  figures = builder.build()

  game_ = engine.Game(figures=figures)
  with pytest.raises(game.NotInTurnError):
    game_.make_move((0, 0), (0, 1))

def test_make_move_no_figure():
  builder = engine.FiguresBuilder(engine.Colour.BLACK)
  builder.add_figure(engine.FigureType.KING, (0, 0))
  figures = builder.build()

  game_ = engine.Game(figures=figures)
  with pytest.raises(game.NoFigureError):
    game_.make_move((1, 1), (0, 1))


def test_make_move_outside_board():
  builder = engine.FiguresBuilder(engine.Colour.WHITE)
  builder.add_figure(engine.FigureType.KING, (0, 0))
  builder.add_figure(engine.FigureType.KING, (7, 7))
  figures = builder.build()

  game_ = engine.Game(figures=figures)

  with pytest.raises(game.OutsideBoardError):
    game_.make_move((0, 0), (-1, 0))

  with pytest.raises(game.OutsideBoardError):
    game_.make_move((0, 0), (0, -1))

  with pytest.raises(game.OutsideBoardError):
    game_.make_move((7, 7), (7, 8))

  with pytest.raises(game.OutsideBoardError):
    game_.make_move((7, 7), (8, 7))

def test_make_move_same_position_raises_invalid_move():
  builder = engine.FiguresBuilder(engine.Colour.WHITE)
  builder.add_figure(engine.FigureType.KING, (0, 0))
  figures = builder.build()

  game_ = engine.Game(figures=figures)
  with pytest.raises(game.InvalidMoveError):
    game_.make_move((0, 0), (0, 0))

# TODO: test move not valid
