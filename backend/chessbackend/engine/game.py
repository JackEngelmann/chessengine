from typing import Tuple, Optional
from chessbackend.engine import engine


class Game:
    def __init__(self, figures: Tuple[engine.Figure, ...], in_turn=engine.Colour.WHITE):
        self.in_turn = in_turn
        self.figures = figures

    def is_move_possible(self, move: engine.Move) -> bool:
        return _is_move_possible(move, self.figures, self.in_turn)

    def make_move(self, move: engine.Move):
        new_figures = _make_move(move, self.figures, self.in_turn)
        self.figures = new_figures
        self.in_turn = engine.get_opposite_color(self.in_turn)

    def get_all_target_positions(
        self, source_position: engine.Position
    ) -> Tuple[engine.Position, ...]:
        return _get_possible_target_positions(
            source_position, self.figures, self.in_turn
        )

    def is_check(self) -> bool:
        return _is_check(self.figures, self.in_turn)

    def is_checkmate(self) -> bool:
        if not self.is_check():
            return False

        return all(
            not fig.can_do_some_move(self.figures)
            for fig in self.figures
            if fig.colour == self.in_turn
        )

    def is_stalemate(self) -> bool:
        if self.is_check():
            return False

        all_possible_moves = _get_all_possible_moves(self.figures, self.in_turn)
        return len(all_possible_moves) == 0


def _is_outside_board(position: engine.Position):
    return (
        position.x < 0
        or position.y < 0
        or position.x >= engine.BOARD_SIZE
        or position.y >= engine.BOARD_SIZE
    )


def _is_move_possible(
    move: engine.Move, figures: Tuple[engine.Figure, ...], in_turn: engine.Colour
):
    figure_to_move = engine.get_figure_at_position(figures, move.source)

    if figure_to_move is None:
        return False

    valid_figure_move = figure_to_move.is_move_possible(move, figures)
    outside_of_board = _is_outside_board(move.target)
    right_colour = figure_to_move.colour == in_turn
    return right_colour and valid_figure_move and not outside_of_board


def _make_move(
    move: engine.Move, figures: Tuple[engine.Figure, ...], in_turn: engine.Colour
):
    if not _is_move_possible(move, figures, in_turn):
        raise ValueError("Invalid move")
    figure_to_move = engine.get_figure_at_position(figures, move.source)
    new_figures = figure_to_move.execute_move(move, figures)
    return new_figures


# TODO: rename _get_all_taget_positions, _get_possible_target_positions
def _get_possible_target_positions(
    source_position: engine.Position,
    figures: Tuple[engine.Figure, ...],
    in_turn: engine.Colour,
):
    figure = engine.get_figure_at_position(figures, source_position)

    if figure.colour != in_turn:
        return tuple()

    all_possible_moves = figure.get_all_possible_moves(figures)
    possible_positions = []

    for move in all_possible_moves:
        new_figures = _make_move(move, figures, in_turn)
        # After the move, the player in turn shouldn't be in check (anymore).
        if not _is_check(new_figures, in_turn):
            possible_positions.append(move.target)

    return tuple(possible_positions)


def _get_all_possible_moves(
    figures: Tuple[engine.Figure, ...], in_turn: engine.Colour
) -> Tuple[engine.Move, ...]:
    possible_moves = []
    for figure in figures:
        for target_position in _get_possible_target_positions(
            figure.position, figures, in_turn
        ):
            move = engine.Move(figure.position, target_position)
            possible_moves.append(move)
    return possible_moves


def _is_check(figures: Tuple[engine.Figure, ...], in_turn: engine.Colour):
    king = _find_king(figures, in_turn)

    # Only for test cases. In practice, both kings must always exist.
    if king is None:
        return False

    for figure in figures:
        move_to_beat_king = engine.Move(figure.position, king.position)
        if figure.is_move_possible(move_to_beat_king, figures):
            return True
    return False


def _find_king(
    figures: Tuple[engine.Figure, ...], colour: engine.Colour
) -> Optional[engine.Figure]:
    return next(
        (fig for fig in figures if fig.name == "King" and fig.colour == colour), None
    )
