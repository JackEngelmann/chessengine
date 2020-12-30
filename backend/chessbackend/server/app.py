import json
from typing import Tuple, Type
from flask import Flask, jsonify, request, Response, make_response
from chessbackend import engine
from chessbackend.server import data

app = Flask(__name__)
game_repository = data.GameRepository()
figure_repository = data.FigureRepository()


def reset_data():
    game_repository.clear()
    figure_repository.clear()


@app.route('/game', methods=["POST"])
def create_game():
    game_factory = data.GameDataAdapterFactory()
    game = game_factory.create()

    figure_factory = data.FigureDataAdapterFactory(game.id)
    figure_builder = engine.FigureBuilder(figure_factory)
    figures = engine.build_default_figures(figure_builder)

    game.figures = figures

    game_repository.add(game)
    for figure in game.figures:
        figure_repository.add(figure)

    return make_response(jsonify({
        "id": game.id,
        "inTurn": game.in_turn.value,
    }), 201)


@app.route('/game/<game_id>', methods=["GET"])
def get_game(game_id):
    game = game_repository.get(game_id)
    return jsonify({
        "id": game.id,
        "inTurn": game.in_turn.value,
    })


@app.route('/game/<game_id>/figures', methods=["GET"])
def get_figures(game_id):
    figures = figure_repository.get_game_figures(game_id)
    figures_data = tuple(
        {
            'positionX': fig.position[0],
            'positionY': fig.position[1],
            'colour': fig.colour.value,
            'id': fig.id,
            'name': fig.name
        }
        for fig in figures
    )
    return jsonify(figures_data)

@app.route('/game/<game_id>/figures/<figure_id>', methods=["GET"])
def get_figure_details(game_id, figure_id):
    figure = figure_repository.get(figure_id)
    game = game_repository.get(game_id)
    game_figures = figure_repository.get_game_figures(game_id)
    game.figures = game_figures
    valid_moves = game.get_all_target_positions(figure.position)
    return jsonify({
        'id': figure.id,
        'positionX': figure.position[0],
        'positionY': figure.position[1],
        'colour': figure.colour.value,
        'validMoves': tuple(valid_moves),
        'name': figure.name
    })

# TODO: should route be different?
@app.route('/game/<game_id>', methods=["PATCH"])
def make_move(game_id):
    json = request.get_json()
    from_position = engine.Position(json['from']['x'], json['from']['y'])
    to_position = engine.Position(json['to']['x'], json['to']['y'])
    game = game_repository.get(game_id)
    game.figures = figure_repository.get_game_figures(game_id)
    old_figure_ids = tuple(fig.id for fig in game.figures)

    try:
        game.make_move(
            engine.Move(from_position, to_position)
        )
        game_repository.update(game)
        new_figure_ids = tuple(fig.id for fig in game.figures)
        for figure in game.figures:
            figure_repository.update(figure)
        for fig_id in old_figure_ids:
            print(fig_id)
            if fig_id not in new_figure_ids:
                print("delete!")
                figure_repository.delete(fig_id)
        return jsonify({}), 204
    except engine.NoFigureError:
        return jsonify("No figure"), 409 # TODO: other status code? error message
    except engine.InvalidMoveError:
        return jsonify("Invalid move"), 409 # TODO: other status code? error message