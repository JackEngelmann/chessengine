from abc import ABC, abstractmethod
from typing import NamedTuple, Tuple, Optional, Type
import enum
import copy


BOARD_SIZE = 8


class Position(NamedTuple):
    x: int
    y: int


class Colour(enum.Enum):
    WHITE = "white"
    BLACK = "black"


def get_opposite_color(colour: Colour):
    if colour == Colour.WHITE:
        return Colour.BLACK
    else:
        return Colour.WHITE


class Move(NamedTuple):
    source: Position
    target: Position


class Movement(ABC):
    @abstractmethod
    def is_move_possible(self, move: Move, figures: Tuple["Figure", ...]) -> bool:
        pass

    def execute_move(
        self, move: Move, figures: Tuple["Figure", ...]
    ) -> Tuple["Figure", ...]:
        figure = get_figure_at_position(figures, move.source)
        new_figure = copy.copy(figure)
        new_figure.position = move.target
        untouched_figures = tuple(
            fig
            for fig in figures
            if fig.position != move.source and fig.position != move.target
        )
        return untouched_figures + (new_figure,)


class PawnCaptureMovement(Movement):
    def is_move_possible(self, move: Move, figures: Tuple["Figure", ...]) -> bool:
        source_figure = get_figure_at_position(figures, move.source)
        target_figure = get_figure_at_position(figures, move.target)

        # Must capture something.
        if not target_figure:
            return False

        # Cannot capture same color.
        if target_figure.colour == source_figure.colour:
            return False

        allowed_direction = 1 if source_figure.colour == Colour.WHITE else -1
        moves_one_field_forward = move.target.y == move.source.y + allowed_direction

        x_diff = abs(move.target.x - move.source.x)
        move_one_field_to_side = x_diff == 1
        return moves_one_field_forward and move_one_field_to_side


class PawnForwardMovement(Movement):
    def is_move_possible(self, move: Move, figures: Tuple["Figure", ...]) -> bool:
        source_figure = get_figure_at_position(figures, move.source)
        target_figure = get_figure_at_position(figures, move.target)

        # Cannot beat figure of same colour.
        if target_figure is not None:
            return False

        if move.source.x != move.target.x:
            return False

        # Regular movement.
        allowed_direction = 1 if source_figure.colour == Colour.WHITE else -1
        if move.target.y == move.source.y + allowed_direction:
            return True

        # White moves two field foward from start.
        if source_figure.colour == Colour.WHITE:
            jump_over_field_is_free = (
                get_figure_at_position(figures, Position(move.source.x, 2)) is None
            )
            return move.source.y == 1 and move.target.y == 3 and jump_over_field_is_free

        # White moves two field foward from start.
        if source_figure.colour == Colour.BLACK:
            jump_over_field_is_free = (
                get_figure_at_position(figures, Position(move.source.x, 5)) is None
            )
            return move.source.y == 6 and move.target.y == 4 and jump_over_field_is_free

        return False


class LinearMovement(Movement):
    def is_move_possible(self, move: Move, figures: Tuple["Figure", ...]) -> bool:
        source_figure = get_figure_at_position(figures, move.source)
        target_figure = get_figure_at_position(figures, move.target)

        # Cannot beat figure of same colour.
        if target_figure and target_figure.colour == source_figure.colour:
            return False

        # If vertical, vertical path must be free.
        vertical_move = (
            move.source.x == move.target.x and move.source.y != move.target.y
        )
        if vertical_move:
            y_values = (move.source.y, move.target.y)
            for y in range(min(y_values) + 1, max(y_values)):
                if (
                    get_figure_at_position(figures, Position(move.source.x, y))
                    is not None
                ):
                    return False
            return True

        # If horizontal, horizontal path must be free.
        horizontal_move = (
            move.source.x != move.target.x and move.source.y == move.target.y
        )
        if horizontal_move:
            x_values = (move.source.x, move.target.x)
            for x in range(min(x_values) + 1, max(x_values)):
                if (
                    get_figure_at_position(figures, Position(x, move.source.y))
                    is not None
                ):
                    return False
            return True

        return False


class KingRegularMovement(Movement):
    def is_move_possible(self, move: Move, figures: Tuple["Figure", ...]) -> bool:
        source_figure = get_figure_at_position(figures, move.source)
        target_figure = get_figure_at_position(figures, move.target)

        # Cannot beat figure of same colour.
        if target_figure and target_figure.colour == source_figure.colour:
            return False

        x_diff = abs(move.target.x - move.source.x)
        y_diff = abs(move.target.y - move.source.y)
        did_move = x_diff > 0 or y_diff > 0
        return did_move and x_diff <= 1 and y_diff <= 1


class DiagonalMovement(Movement):
    def is_move_possible(self, move: Move, figures: Tuple["Figure", ...]) -> bool:
        source_figure = get_figure_at_position(figures, move.source)
        target_figure = get_figure_at_position(figures, move.target)

        # Cannot beat figure of same colour.
        if target_figure and target_figure.colour == source_figure.colour:
            return False

        x_diff = abs(move.target.x - move.source.x)
        y_diff = abs(move.target.y - move.source.y)

        # Figure must move.
        if x_diff == 0 or y_diff == 0:
            return False

        # Figure must move diagonally.
        if x_diff != y_diff:
            return False

        # Path must be free.
        x_range = _get_exclusive_range(move.source.x, move.target.x)
        y_range = _get_exclusive_range(move.source.y, move.target.y)
        for (x, y) in zip(x_range, y_range):
            if get_figure_at_position(figures, Position(x, y)) is not None:
                return False
        return True


class KnightMovement(Movement):
    def is_move_possible(self, move: Move, figures: Tuple["Figure", ...]) -> bool:
        source_figure = get_figure_at_position(figures, move.source)
        target_figure = get_figure_at_position(figures, move.target)

        # Cannot beat figure of same colour.
        if target_figure and target_figure.colour == source_figure.colour:
            return False

        x_diff = abs(move.target.x - move.source.x)
        y_diff = abs(move.target.y - move.source.y)
        return x_diff == 2 and y_diff == 1 or x_diff == 1 and y_diff == 2


class Figure:
    def __init__(
        self,
        colour: Colour,
        position: Position,
        movements: Tuple[Movement, ...],
        name: str,
    ):
        self.colour = colour
        self.position = position
        self._movements = movements
        self.name = name

    def is_move_possible(self, move: Move, figures: Tuple["Figure", ...]) -> bool:
        return any(
            movement.is_move_possible(move, figures) for movement in self._movements
        )

    def execute_move(
        self, move: Move, figures: Tuple["Figure", ...]
    ) -> Tuple["Figure", ...]:
        possible_movement = None
        for movement in self._movements:
            if movement.is_move_possible(move, figures):
                possible_movement = movement
        assert possible_movement is not None
        return possible_movement.execute_move(move, figures)

    def __copy__(self):
        return Figure(self.colour, self.position, self._movements, self.name)


class FigureFactory:
    def create(
        self,
        colour: Colour,
        position: Position,
        movements: Tuple[Movement, ...],
        name: str,
    ):
        return Figure(colour, position, movements, name)


class FigureBuilder:
    def __init__(self, figure_factory: Type[FigureFactory]):
        self.figure_factory = figure_factory

    def build_queen(self, colour: Colour, position: Position):
        movements = (LinearMovement(), DiagonalMovement())
        return self.figure_factory.create(colour, position, movements, "Queen")

    def build_rook(self, colour: Colour, position: Position):
        movements = (LinearMovement(),)
        return self.figure_factory.create(colour, position, movements, "Rook")

    def build_bishop(self, colour: Colour, position: Position):
        movements = (DiagonalMovement(),)
        return self.figure_factory.create(colour, position, movements, "Bishop")

    def build_knight(self, colour: Colour, position: Position):
        movements = (KnightMovement(),)
        return self.figure_factory.create(colour, position, movements, "Knight")

    def build_king(self, colour: Colour, position: Position):
        movements = (KingRegularMovement(),)
        return self.figure_factory.create(colour, position, movements, "King")

    def build_pawn(self, colour: Colour, position: Position):
        movements = (PawnForwardMovement(), PawnCaptureMovement())
        return self.figure_factory.create(colour, position, movements, "Pawn")


def get_figure_at_position(
    figures: Tuple[Figure, ...], position: Position
) -> Optional[Figure]:
    for figure in figures:
        if figure.position == position:
            return figure
    return None


def build_default_figures(figure_builder: FigureBuilder) -> Tuple[Figure, ...]:
    figures = []

    # Add all figures except pawns.
    figures.extend(
        [
            # Add all black figures except pawns.
            figure_builder.build_rook(Colour.BLACK, Position(0, 7)),
            figure_builder.build_knight(Colour.BLACK, Position(1, 7)),
            figure_builder.build_bishop(Colour.BLACK, Position(2, 7)),
            figure_builder.build_queen(Colour.BLACK, Position(3, 7)),
            figure_builder.build_king(Colour.BLACK, Position(4, 7)),
            figure_builder.build_bishop(Colour.BLACK, Position(5, 7)),
            figure_builder.build_knight(Colour.BLACK, Position(6, 7)),
            figure_builder.build_rook(Colour.BLACK, Position(7, 7)),
            # Add a white figures except pawns.
            figure_builder.build_rook(Colour.WHITE, Position(0, 0)),
            figure_builder.build_knight(Colour.WHITE, Position(1, 0)),
            figure_builder.build_bishop(Colour.WHITE, Position(2, 0)),
            figure_builder.build_queen(Colour.WHITE, Position(3, 0)),
            figure_builder.build_king(Colour.WHITE, Position(4, 0)),
            figure_builder.build_bishop(Colour.WHITE, Position(5, 0)),
            figure_builder.build_knight(Colour.WHITE, Position(6, 0)),
            figure_builder.build_rook(Colour.WHITE, Position(7, 0)),
        ]
    )

    # Add pawns.
    for x in range(BOARD_SIZE):
        figures.append(figure_builder.build_pawn(Colour.BLACK, Position(x, 6)))
        figures.append(figure_builder.build_pawn(Colour.WHITE, Position(x, 1)))
    return tuple(figures)


def _get_exclusive_range(start: int, end: int):
    # TODO: rename
    if start < end:
        return tuple(range(start + 1, end))
    else:
        return tuple(range(start - 1, end, -1))
