from typing import Tuple
from flask import Flask, jsonify
from chessbackend import engine
from chessbackend.server import repositories

app = Flask(__name__)

game_repository = repositories.GameRepository()
figure_repository = repositories.FigureRepository()


@app.route('/game', methods=["PUT"])
def create_game():
    game_builder = engine.GameBuilder()
    game_builder.add_figure(engine.FigureType.KING, (1, 1), engine.Colour.WHITE)
    game = game_builder.build()

    game_repository.add(game)
    for figure in game.figures:
        figure_repository.add(figure)

    return jsonify({
        "id": game.id
    })


@app.route('/game/<int:game_id>', methods=["GET"])
def get_game(game_id):
    game = game_repository.get(game_id)
    return jsonify({
        "in-turn": game.in_turn.value
    })


@app.route('/game/<int:game_id>/figures', methods=["GET"])
def get_figures(game_id):
    figures = figure_repository.get_game_figures(game_id)
    figures_data = tuple(
        {
            'position-x': fig.position[0],
            'position-y': fig.position[1],
            'colour': fig.colour.value,
            'id': fig.id
        }
        for fig in figures
    )
    return jsonify(figures_data)

@app.route('/game/<int:game_id>/figures/<int:figure_id>', methods=["GET"])
def get_figure_details(game_id, figure_id):
    figure = figure_repository.get(figure_id)
    game = game_repository.get(game_id)
    game_figures = figure_repository.get_game_figures(game_id)
    game.figures = game_figures
    valid_moves = game.get_all_valid_moves(figure)
    return jsonify({
        'id': figure.id,
        'position-x': figure.position[0],
        'position-y': figure.position[1],
        'colour': figure.colour.value,
        'valid-moves': tuple(valid_moves),
    })