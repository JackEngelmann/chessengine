from typing import Tuple, Optional
from chessbackend.engine import engine
import copy


class Game:
    def __init__(self, figures: Tuple[engine.Figure, ...], in_turn=engine.Colour.WHITE):
        self.in_turn = in_turn
        self.figures = figures

    def is_move_possible(self, move: engine.Move) -> bool:
        figure_to_move = engine.get_figure_at_position(self.figures, move.source)

        # There must be a figure to move.
        if figure_to_move is None:
            return False

        # The target position must be inside board.
        if _is_outside_board(move.target):
            return False

        # Cannot expose own king.
        game_copy = Game(self.figures, self.in_turn)
        game_copy._unsafe_make_move(move)
        if game_copy.is_colour_in_check(self.in_turn):
            return False

        # Player can only move figures of matching color.
        if not figure_to_move.colour == self.in_turn:
            return False

        return figure_to_move.is_move_possible(move, self.figures)

    def make_move(self, move: engine.Move):
        if not self.is_move_possible(move):
            raise ValueError("Invalid move")
        self._unsafe_make_move(move)

    def get_all_target_positions(
        self, source_position: engine.Position
    ) -> Tuple[engine.Position, ...]:
        figure_to_move = engine.get_figure_at_position(self.figures, source_position)
        possible_moves = figure_to_move.get_all_possible_moves(self.figures)
        return tuple(
            move.target for move in possible_moves if self.is_move_possible(move)
        )

    def is_check(self) -> bool:
        king = _find_king(self.figures, self.in_turn)

        # Only for test cases. In practice, both kings must always exist.
        if king is None:
            return False

        for figure in self.figures:
            move_to_beat_king = engine.Move(figure.position, king.position)
            if figure.is_move_possible(move_to_beat_king, self.figures):
                return True
        return False

    def is_colour_in_check(self, colour: engine.Colour) -> bool:
        king = _find_king(self.figures, colour)

        # Only for test cases. In practice, both kings must always exist.
        if king is None:
            return False

        for figure in self.figures:
            move_to_beat_king = engine.Move(figure.position, king.position)
            if figure.is_move_possible(move_to_beat_king, self.figures):
                return True
        return False

    def is_checkmate(self) -> bool:
        if not self.is_check():
            return False

        all_possible_moves = self._get_all_possible_moves()
        return len(all_possible_moves) == 0

    def is_stalemate(self) -> bool:
        if self.is_check():
            return False

        all_possible_moves = self._get_all_possible_moves()
        return len(all_possible_moves) == 0

    def _get_all_possible_moves(self):
        possible_figure_moves = []
        for figure in self.figures:
            possible_figure_moves.extend(figure.get_all_possible_moves(self.figures))
        return tuple(
            move for move in possible_figure_moves if self.is_move_possible(move)
        )

    def _unsafe_make_move(self, move: engine.Move):
        # This applies a move without checking for validity first.
        # This is necessary, because the check for validity needs to move figures to
        # check if the resulting board would be invalid (e.g. expose own king to check).
        figure_to_move = engine.get_figure_at_position(self.figures, move.source)
        self.figures = figure_to_move.execute_move(move, self.figures)
        self.in_turn = engine.get_opposite_color(self.in_turn)


def _is_outside_board(position: engine.Position):
    return (
        position.x < 0
        or position.y < 0
        or position.x >= engine.BOARD_SIZE
        or position.y >= engine.BOARD_SIZE
    )


def _find_king(
    figures: Tuple[engine.Figure, ...], colour: engine.Colour
) -> Optional[engine.Figure]:
    return next(
        (fig for fig in figures if fig.name == "King" and fig.colour == colour), None
    )
