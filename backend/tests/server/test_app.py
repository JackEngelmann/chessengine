import pytest
from chessbackend.server import app
from chessbackend import engine
from flask import json


def test_create_game(client):
  response = client.post('/game')
  data = json.loads(response.data)
  assert data['id'] == 0


def test_get_game(client):
  create_response = client.post('/game')
  create_data = json.loads(create_response.data)

  game_id = create_data['id']

  get_response = client.get(f'/game/{game_id}')
  get_data = json.loads(get_response.data)
  assert get_data['inTurn'] == 'white'


def test_get_game_figures(client):
  create_response = client.post('/game')
  create_data = json.loads(create_response.data)

  game_id = create_data['id']

  figures_response = client.get(f'/game/{game_id}/figures')
  figures_data = json.loads(figures_response.data)
  assert len(figures_data) > 0
  for figure in figures_data:
    assert isinstance(figure['id'], int)
    assert isinstance(figure['positionX'], int)
    assert isinstance(figure['positionY'], int)
    assert figure['colour'] == "white" or figure['colour'] == "black"
  
def test_get_figure_details(client):
  create_response = client.post('/game')
  create_data = json.loads(create_response.data)

  game_id = create_data['id']

  figures_response = client.get(f'/game/{game_id}/figures')
  figures_data = json.loads(figures_response.data)

  figure_id = figures_data[0]['id']

  figure_details_response = client.get(f'/game/{game_id}/figures/{figure_id}')
  figure_details_data = json.loads(figure_details_response.data)
  assert isinstance(figure_details_data['id'], int)
  assert isinstance(figure_details_data['positionX'], int)
  assert isinstance(figure_details_data['positionY'], int)
  assert figure_details_data['colour'] == "white" or figure['colour'] == "black"
  assert len(figure_details_data['validMoves']) > 0
  assert len(figure_details_data['validMoves'][0]) == 2


def test_update_figure_location(client):
  game_builder = engine.GameBuilder()
  game_builder.add_figure(engine.FigureType.KING, (3, 3), engine.Colour.WHITE)
  game = game_builder.build()
  app.game_repository.add(game)

  for figure in game.figures:
    app.figure_repository.add(figure)
  
  patch_response = client.patch(f'/game/{game.id}', json={
    "from": {
      "x": 3,
      "y": 3,
    },
    "to": {
      "x": 3,
      "y": 4,
    },
  })
  assert patch_response.status_code == 204

  figures_response = client.get(f'/game/{game.id}/figures')
  figures_data = json.loads(figures_response.data)
  assert len(figures_data) == 1
  assert figures_data[0]['positionX'] == 3
  assert figures_data[0]['positionY'] == 4

  game_response = client.get(f'/game/{game.id}')
  game_data = json.loads(game_response.data)
  assert game_data['inTurn'] == 'black'

@pytest.fixture
def client():
  app.app.config["TESTING"] = True
  # TODO: app.app.app_context is pretty ugly.
  with app.app.test_client() as client:
    yield client
  app.clear_repositories()
