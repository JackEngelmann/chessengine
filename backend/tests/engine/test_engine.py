from chessbackend.engine import engine
import unittest
import pytest

figure_factory = engine.FigureFactory()
figure_builder = engine.FigureBuilder(figure_factory)


@pytest.mark.parametrize(
    "build_figure", (figure_builder.build_queen, figure_builder.build_rook)
)
class TestLinearMovements:
    @staticmethod
    def test_horizontal_move(build_figure):
        moving_figure = build_figure(engine.Colour.WHITE, engine.Position(3, 3))
        move = engine.Move(engine.Position(3, 3), engine.Position(3, 4))
        assert moving_figure.is_move_possible(move, (moving_figure,))
        moving_figure, *_ = moving_figure.execute_move(move, (moving_figure,))
        assert moving_figure.position == move.target

    @staticmethod
    def test_vertical_move(build_figure):
        moving_figure = build_figure(engine.Colour.WHITE, engine.Position(3, 3))
        move = engine.Move(engine.Position(3, 3), engine.Position(4, 3))
        assert moving_figure.is_move_possible(move, (moving_figure,))
        moving_figure, *_ = moving_figure.execute_move(move, (moving_figure,))
        assert moving_figure.position == move.target

    @staticmethod
    def test_illegal_move(build_figure):
        moving_figure = build_figure(engine.Colour.WHITE, engine.Position(3, 3))
        move = engine.Move(engine.Position(3, 3), engine.Position(4, 5))
        assert not moving_figure.is_move_possible(move, (moving_figure,))

    @staticmethod
    def test_beat_figure(build_figure):
        moving_figure = build_figure(engine.Colour.WHITE, engine.Position(3, 3))
        fig_opposite_color = build_figure(engine.Colour.BLACK, engine.Position(4, 3))
        move = engine.Move(engine.Position(3, 3), engine.Position(4, 3))
        figures = (moving_figure, fig_opposite_color)
        assert moving_figure.is_move_possible(move, figures)
        figures_after_move = moving_figure.execute_move(move, figures)
        assert len(figures_after_move) == 1
        moving_figure, *_ = figures_after_move
        assert moving_figure.position == move.target

    @staticmethod
    def test_cannot_beat_figure_of_same_color(build_figure):
        moving_figure = build_figure(engine.Colour.WHITE, engine.Position(3, 3))
        fig_same_color = build_figure(engine.Colour.WHITE, engine.Position(4, 3))
        move = engine.Move(engine.Position(3, 3), engine.Position(4, 3))
        figures = (moving_figure, fig_same_color)
        assert not moving_figure.is_move_possible(move, figures)

    @staticmethod
    def test_cannot_jump_over_figures(build_figure):
        moving_figure = build_figure(engine.Colour.WHITE, engine.Position(3, 3))
        fig_in_vertical_way = build_figure(engine.Colour.WHITE, engine.Position(4, 3))
        fig_in_horizontal_way = build_figure(engine.Colour.WHITE, engine.Position(3, 4))
        vertical_move = engine.Move(engine.Position(3, 3), engine.Position(5, 3))
        horizontal_move = engine.Move(engine.Position(3, 3), engine.Position(3, 5))
        figures = (moving_figure, fig_in_vertical_way, fig_in_horizontal_way)
        assert not moving_figure.is_move_possible(vertical_move, figures)
        assert not moving_figure.is_move_possible(horizontal_move, figures)


@pytest.mark.parametrize(
    "build_figure", (figure_builder.build_queen, figure_builder.build_bishop)
)
class TestLinearMovements:
    @staticmethod
    def test_diagonal_move(build_figure):
        moving_figure = build_figure(engine.Colour.WHITE, engine.Position(3, 3))
        move = engine.Move(engine.Position(3, 3), engine.Position(5, 5))
        assert moving_figure.is_move_possible(move, (moving_figure,))
        moving_figure, *_ = moving_figure.execute_move(move, (moving_figure,))
        assert moving_figure.position == move.target

    @staticmethod
    def test_illegal_move(build_figure):
        moving_figure = build_figure(engine.Colour.WHITE, engine.Position(3, 3))
        move = engine.Move(engine.Position(3, 3), engine.Position(4, 5))
        assert not moving_figure.is_move_possible(move, (moving_figure,))

    @staticmethod
    def test_beat_figure(build_figure):
        moving_figure = build_figure(engine.Colour.WHITE, engine.Position(3, 3))
        fig_opposite_color = build_figure(engine.Colour.BLACK, engine.Position(4, 4))
        move = engine.Move(engine.Position(3, 3), engine.Position(4, 4))
        figures = (moving_figure, fig_opposite_color)
        assert moving_figure.is_move_possible(move, figures)
        figures_after_move = moving_figure.execute_move(move, figures)
        assert len(figures_after_move) == 1
        moving_figure, *_ = figures_after_move
        assert moving_figure.position == move.target

    @staticmethod
    def test_cannot_beat_figure_of_same_color(build_figure):
        moving_figure = build_figure(engine.Colour.WHITE, engine.Position(3, 3))
        fig_same_color = build_figure(engine.Colour.WHITE, engine.Position(4, 4))
        move = engine.Move(engine.Position(3, 3), engine.Position(4, 4))
        figures = (moving_figure, fig_same_color)
        assert not moving_figure.is_move_possible(move, figures)

    @staticmethod
    def test_cannot_jump_over_figures(build_figure):
        moving_figure = build_figure(engine.Colour.WHITE, engine.Position(3, 3))
        fig_in_way = build_figure(engine.Colour.WHITE, engine.Position(4, 4))
        move = engine.Move(engine.Position(3, 3), engine.Position(5, 5))
        figures = (moving_figure, fig_in_way)
        assert not moving_figure.is_move_possible(move, figures)


class TestKnightMovements:
    @pytest.mark.parametrize(
        "source_position, target_position",
        (
            (engine.Position(4, 4), engine.Position(2, 3)),
            (engine.Position(4, 4), engine.Position(3, 2)),
            (engine.Position(4, 4), engine.Position(6, 5)),
        ),
    )
    def test_knight_movement(self, source_position, target_position):
        moving_figure = figure_builder.build_knight(
            engine.Colour.WHITE, source_position
        )
        move = engine.Move(source_position, target_position)
        figures = (moving_figure,)
        assert moving_figure.is_move_possible(move, figures)
        moving_figure, *_ = moving_figure.execute_move(move, figures)
        assert moving_figure.position == target_position

    @pytest.mark.parametrize(
        "source_position, target_position",
        (
            (engine.Position(4, 4), engine.Position(4, 5)),
            (engine.Position(4, 4), engine.Position(3, 3)),
            (engine.Position(4, 4), engine.Position(7, 4)),
        ),
    )
    def test_invalid_knight_movement(self, source_position, target_position):
        moving_figure = figure_builder.build_knight(
            engine.Colour.WHITE, source_position
        )
        move = engine.Move(source_position, target_position)
        figures = (moving_figure,)
        assert not moving_figure.is_move_possible(move, figures)

    @staticmethod
    def test_cannot_beat_figure_of_same_color():
        moving_figure = figure_builder.build_knight(
            engine.Colour.WHITE, engine.Position(4, 4)
        )
        fig_same_color = figure_builder.build_knight(
            engine.Colour.WHITE, engine.Position(2, 3)
        )
        move = engine.Move(engine.Position(4, 4), engine.Position(2, 3))
        figures = (moving_figure, fig_same_color)
        assert not moving_figure.is_move_possible(move, figures)

    @staticmethod
    def test_beat_figure():
        moving_figure = figure_builder.build_knight(
            engine.Colour.WHITE, engine.Position(4, 4)
        )
        fig_opposite_color = figure_builder.build_knight(
            engine.Colour.BLACK, engine.Position(2, 3)
        )
        move = engine.Move(engine.Position(4, 4), engine.Position(2, 3))
        figures = (moving_figure, fig_opposite_color)
        assert moving_figure.is_move_possible(move, figures)
        figures_after_move = moving_figure.execute_move(move, figures)
        assert len(figures_after_move) == 1
        moving_figure, *_ = figures_after_move
        assert moving_figure.position == move.target


class TestKingRegularMovements:
    @pytest.mark.parametrize(
        "source_position, target_position",
        (
            (engine.Position(4, 4), engine.Position(4, 5)),
            (engine.Position(4, 4), engine.Position(5, 4)),
            (engine.Position(4, 4), engine.Position(5, 5)),
            (engine.Position(4, 4), engine.Position(3, 3)),
        ),
    )
    def test_king_movement(source_position, target_position):
        moving_figure = figure_builder.build_king(engine.Colour.WHITE, source_position)
        move = engine.Move(source_position, target_position)
        figures = (moving_figure,)
        assert moving_figure.is_move_possible(move, figures)
        moving_figure, *_ = moving_figure.execute_move(move, figures)
        assert moving_figure.position == target_position

    @pytest.mark.parametrize(
        "source_position, target_position",
        (
            (engine.Position(4, 4), engine.Position(4, 4)),
            (engine.Position(4, 4), engine.Position(6, 4)),
            (engine.Position(4, 4), engine.Position(6, 6)),
            (engine.Position(4, 4), engine.Position(3, 2)),
        ),
    )
    def test_king_movement(self, source_position, target_position):
        moving_figure = figure_builder.build_king(engine.Colour.WHITE, source_position)
        move = engine.Move(source_position, target_position)
        figures = (moving_figure,)
        assert not moving_figure.is_move_possible(move, figures)


class TestPawnForwardMovement:
    @pytest.mark.parametrize(
        "colour,source_position,target_position",
        (
            (engine.Colour.WHITE, engine.Position(2, 2), engine.Position(2, 3)),
            (engine.Colour.BLACK, engine.Position(2, 3), engine.Position(2, 2)),
            (  # Move two field forward from start field (white).
                engine.Colour.WHITE,
                engine.Position(2, 1),
                engine.Position(2, 3),
            ),
            (  # Move two field forward from start field (white).
                engine.Colour.BLACK,
                engine.Position(2, 6),
                engine.Position(2, 4),
            ),
        ),
    )
    def test_pawn_move_forward(self, colour, source_position, target_position):
        moving_figure = figure_builder.build_pawn(colour, source_position)
        move = engine.Move(source_position, target_position)
        figures = (moving_figure,)
        assert moving_figure.is_move_possible(move, figures)

    @pytest.mark.parametrize(
        "colour,source_position,target_position",
        (
            (engine.Colour.WHITE, engine.Position(2, 3), engine.Position(2, 2)),
            (engine.Colour.WHITE, engine.Position(2, 2), engine.Position(3, 2)),
            (engine.Colour.BLACK, engine.Position(2, 2), engine.Position(2, 3)),
            (engine.Colour.BLACK, engine.Position(2, 2), engine.Position(3, 2)),
        ),
    )
    def test_pawn_invalid_move_forward(self, colour, source_position, target_position):
        moving_figure = figure_builder.build_pawn(colour, source_position)
        move = engine.Move(source_position, target_position)
        figures = (moving_figure,)
        assert not moving_figure.is_move_possible(move, figures)

    @staticmethod
    def test_pawn_cannot_capture_forward():
        moving_figure = figure_builder.build_pawn(
            engine.Colour.WHITE, engine.Position(2, 2)
        )
        figure_in_way = figure_builder.build_pawn(
            engine.Colour.BLACK, engine.Position(2, 3)
        )
        move = engine.Move(moving_figure.position, figure_in_way.position)
        assert moving_figure.is_move_possible(move, (moving_figure,))
        assert not moving_figure.is_move_possible(move, (moving_figure, figure_in_way))


class TestPawnCaptureMovement:
    @staticmethod
    def test_pawn_capture_movement_white():
        moving_figure = figure_builder.build_pawn(
            engine.Colour.WHITE, engine.Position(2, 2)
        )
        fig_to_capture = figure_builder.build_pawn(
            engine.Colour.BLACK, engine.Position(3, 3)
        )
        move = engine.Move(moving_figure.position, fig_to_capture.position)
        figures = (moving_figure, fig_to_capture)
        assert moving_figure.is_move_possible(move, figures)
        assert not moving_figure.is_move_possible(move, (moving_figure,))

        figures_after_move = moving_figure.execute_move(move, figures)
        assert len(figures_after_move) == 1
        moving_figure, *_ = figures_after_move
        assert moving_figure.position == move.target

    @staticmethod
    def test_pawn_capture_movement_black():
        moving_figure = figure_builder.build_pawn(
            engine.Colour.BLACK, engine.Position(3, 3)
        )
        fig_to_capture = figure_builder.build_pawn(
            engine.Colour.WHITE, engine.Position(2, 2)
        )
        move = engine.Move(moving_figure.position, fig_to_capture.position)
        figures = (moving_figure, fig_to_capture)
        assert moving_figure.is_move_possible(move, figures)
        assert not moving_figure.is_move_possible(move, (moving_figure,))

        figures_after_move = moving_figure.execute_move(move, figures)
        assert len(figures_after_move) == 1
        moving_figure, *_ = figures_after_move
        assert moving_figure.position == move.target


def test_build_default_figures():
    figures = engine.build_default_figures(figure_builder)
    assert isinstance(figures, tuple)
    assert len(figures) == 32
    white_figures = tuple(fig for fig in figures if fig.colour == engine.Colour.WHITE)
    black_figures = tuple(fig for fig in figures if fig.colour == engine.Colour.BLACK)
    assert len(black_figures) == len(white_figures)


def test_position_equal():
    assert engine.Position(3, 3) == engine.Position(3, 3)
    assert engine.Position(3, 3) != engine.Position(3, 4)
