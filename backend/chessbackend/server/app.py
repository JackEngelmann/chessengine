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
        }
        for fig in figures
    )
    return jsonify(figures_data)
