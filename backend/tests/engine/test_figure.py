from chessbackend.engine import figure
from chessbackend import engine


class TestKing:
  def test_is_move_valid_when_valid(self):
    king = figure.King(engine.colouring.Colour.WHITE, (3, 3))
    assert king.is_move_valid((2, 2))
    assert king.is_move_valid((2, 3))
    assert king.is_move_valid((2, 4))

    assert king.is_move_valid((3, 2))
    assert king.is_move_valid((3, 4))

    assert king.is_move_valid((4, 2))
    assert king.is_move_valid((4, 3))
    assert king.is_move_valid((4, 4))

  def test_is_move_valid_when_invalid(self):
    king = figure.King(engine.colouring.Colour.WHITE, (3, 3))
    assert not king.is_move_valid((3, 5))
    assert not king.is_move_valid((6, 6))
    assert not king.is_move_valid((5, 3))
