import enum
from typing import Tuple
from chessbackend.engine import colouring, figure

class FigureType(enum.Enum):
  KING = "king"

class FiguresBuilder():
  def __init__(self, colour: colouring.Colour):
    self._colour = colour
    self._figures = []
  
  def set_colour(self, colour: colouring.Colour):
    self._colour = colour
  
  def add_figure(self, figure_type: FigureType, position: figure.Position):
    new_figure = None
    if figure_type == FigureType.KING:
      new_figure = figure.King(
        self._colour,
        position,
      )
    self._figures.append(new_figure)
  
  def build(self) -> Tuple[figure.Figure]:
    return tuple(self._figures)


def build_default_figures() -> Tuple[figure.Figure]:
  # Build the classic chess start up figures.
  # TODO: IN PROGRESS!
  builder = FiguresBuilder(colouring.Colour.WHITE)
  builder.add_figure(FigureType.KING, (5, 0))
  builder.set_colour(colouring.Colour.BLACK)
  builder.add_figure(FigureType.KING, (5, 7))
  return builder.build()

