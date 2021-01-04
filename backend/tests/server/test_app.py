import pytest
from chessbackend.server import app, data
from chessbackend import engine
from flask import json


def test_create_game(client):
    response = client.post("/game")
    data = json.loads(response.data)
    assert data["id"] is not None


def test_get_game(client):
    create_response = client.post("/game")
    create_data = json.loads(create_response.data)

    game_id = create_data["id"]

    get_response = client.get(f"/game/{game_id}")
    get_data = json.loads(get_response.data)
    assert get_data["inTurn"] == "white"
    assert isinstance(get_data["check"], bool)
    assert isinstance(get_data["checkmate"], bool)
    assert isinstance(get_data["stalemate"], bool)


def test_get_game_figures(client):
    create_response = client.post("/game")
    create_data = json.loads(create_response.data)

    game_id = create_data["id"]

    figures_response = client.get(f"/game/{game_id}/figures")
    figures_data = json.loads(figures_response.data)
    assert len(figures_data) > 0
    for figure in figures_data:
        assert isinstance(figure["id"], str)
        assert isinstance(figure["positionX"], int)
        assert isinstance(figure["positionY"], int)
        assert figure["colour"] == "white" or figure["colour"] == "black"


def test_get_figure_details(client):
    create_response = client.post("/game")
    create_data = json.loads(create_response.data)

    game_id = create_data["id"]

    figures_response = client.get(f"/game/{game_id}/figures")
    figures_data = json.loads(figures_response.data)

    # Pick a pawn, because all pawns should have some valid moves.
    figure_id = None
    for figure in figures_data:
        if figure["name"] == "Pawn":
            figure_id = figure["id"]

    figure_details_response = client.get(f"/game/{game_id}/figures/{figure_id}")
    figure_details_data = json.loads(figure_details_response.data)
    assert isinstance(figure_details_data["id"], str)
    assert isinstance(figure_details_data["positionX"], int)
    assert isinstance(figure_details_data["positionY"], int)
    assert (
        figure_details_data["colour"] == "white"
        or figure_details_data["colour"] == "black"
    )
    assert len(figure_details_data["validMoves"]) > 0
    assert len(figure_details_data["validMoves"][0]) == 2


def test_update_figure_location(client):
    create_response = client.post("/game")
    create_data = json.loads(create_response.data)

    game_id = create_data["id"]

    # Move white pawn one step forward.
    patch_response = client.patch(
        f"/game/{game_id}", json={"from": {"x": 0, "y": 1}, "to": {"x": 0, "y": 2}}
    )
    assert patch_response.status_code == 204

    figures_response = client.get(f"/game/{game_id}/figures")
    figures_data = json.loads(figures_response.data)
    assert len(figures_data) == 32
    moved_figure = (
        next(
            fig
            for fig in figures_data
            if fig["positionX"] == 0 and fig["positionY"] == 2
        )
        is not None
    )
    assert moved_figure is not None

    game_response = client.get(f"/game/{game_id}")
    game_data = json.loads(game_response.data)
    assert game_data["inTurn"] == "black"


@pytest.fixture
def client():
    app.app.config["TESTING"] = True
    # TODO: app.app.app_context is pretty ugly.
    with app.app.test_client() as client:
        yield client
    app.reset_data()
