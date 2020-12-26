import pytest
from chessbackend.server import app
from flask import json


def test_create_game(client):
  response = client.put('/game')
  data = json.loads(response.data)
  assert data['id'] == 0


def test_get_game(client):
  create_response = client.put('/game')
  create_data = json.loads(create_response.data)

  game_id = create_data['id']

  get_response = client.get(f'/game/{game_id}')
  get_data = json.loads(get_response.data)
  assert get_data['in-turn'] == 'white'


def test_get_game_figures(client):
  create_response = client.put('/game')
  create_data = json.loads(create_response.data)

  game_id = create_data['id']

  figures_response = client.get(f'/game/{game_id}/figures')
  figures_data = json.loads(figures_response.data)
  assert len(figures_data) > 0
  for figure in figures_data:
    assert isinstance(figure['position-x'], int)
    assert isinstance(figure['position-y'], int)
    assert figure['colour'] == "white" or figure['colour'] == "black"
  
  


@pytest.fixture
def client():
  app.app.config["TESTING"] = True
  # TODO: app.app.app_context is pretty ugly.
  with app.app.test_client() as client:
    yield client