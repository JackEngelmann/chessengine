from chessbackend import engine
from chessbackend.cli import boardrenderer

def main():
  figures = engine.build_default_figures()
  game = engine.Game(figures)
  renderer = boardrenderer.BoardRenderer(game)
  renderer.render()

if __name__ == '__main__':
  main()