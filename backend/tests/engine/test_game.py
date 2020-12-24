import unittest
from chessbackend import engine

def test_afterstart_whiteinturn():
  game_ = engine.Game()
  game_.in_turn = engine.Color.WHITE