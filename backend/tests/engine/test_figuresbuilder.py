from chessbackend import engine
from chessbackend.engine import figure


def test_build_empty():
  builder = engine.FiguresBuilder(engine.Colour.WHITE)
  figures = builder.build()
  assert figures == tuple()


def test_build_a_king():
  builder = engine.FiguresBuilder(engine.Colour.WHITE)
  builder.add_figure(engine.FigureType.KING, (0, 0))
  figures = builder.build()
  assert len(figures) == 1
  assert isinstance(figures[0], figure.King)
  assert figures[0].colour == engine.Colour.WHITE


def test_switch_color():
  builder = engine.FiguresBuilder(engine.Colour.WHITE)
  builder.add_figure(engine.FigureType.KING, (0, 0))
  builder.set_colour(engine.Colour.BLACK)
  builder.add_figure(engine.FigureType.KING, (3, 3))
  figures = builder.build()
  assert len(figures) == 2
  assert any(fig.colour == engine.Colour.BLACK for fig in figures)
  assert any(fig.colour == engine.Colour.WHITE for fig in figures)