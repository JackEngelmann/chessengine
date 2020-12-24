from typing import NamedTuple
from abc import ABC, abstractmethod
from chessbackend.engine import colouring

class Position(NamedTuple):
  # Number between 0 and 8; 0 is "A" column in normal chess notation.
  x: int
  # Number between 0 and 8; 0 is "0" row in normal chess notation.
  y: int


class Figure(ABC):
  def __init__(self, colour: colouring.Colour, position: Position):
    self.colour = colour
    self.position = position

  @abstractmethod
  def is_move_valid(self, new_position) -> bool:
    pass

  @property
  @abstractmethod
  def name(self):
    pass

# TODO: think about how to implement castling, en passant

class King(Figure):
  name = "King"

  def is_move_valid(self, new_position) -> bool:
    x_difference = abs(new_position[0] - self.position[0])
    y_difference = abs(new_position[1] - self.position[1]) 
    return x_difference <= 1 and y_difference <= 1

