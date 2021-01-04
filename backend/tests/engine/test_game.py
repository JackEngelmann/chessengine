from chessbackend import engine


figure_factory = engine.FigureFactory()
figure_builder = engine.FigureBuilder(figure_factory)


def test_game_get_all_target_positions():
    king = figure_builder.build_king(engine.Colour.WHITE, engine.Position(3, 3))
    game = engine.Game((king,))
    all_target_positions = game.get_all_target_positions(king.position)
    assert len(all_target_positions) == 8
    assert (2, 2) in all_target_positions
    assert (2, 3) in all_target_positions
    assert (2, 4) in all_target_positions
    assert (3, 2) in all_target_positions
    assert (3, 4) in all_target_positions
    assert (4, 2) in all_target_positions
    assert (4, 3) in all_target_positions
    assert (4, 4) in all_target_positions


def test_game_only_fugre_in_turn_can_move():
    black_rook = figure_builder.build_rook(engine.Colour.BLACK, engine.Position(3, 3))
    white_rook = figure_builder.build_rook(engine.Colour.WHITE, engine.Position(4, 4))
    figures = (white_rook, black_rook)
    white_in_turn_game = engine.Game(figures, engine.Colour.WHITE)
    black_in_turn_game = engine.Game(figures, engine.Colour.BLACK)

    move_white_rook = engine.Move(
        white_rook.position,
        engine.Position(white_rook.position.x, white_rook.position.y + 1),
    )
    move_black_rook = engine.Move(
        black_rook.position,
        engine.Position(black_rook.position.x, black_rook.position.y + 1),
    )

    assert white_in_turn_game.is_move_possible(move_white_rook)
    assert not white_in_turn_game.is_move_possible(move_black_rook)

    assert black_in_turn_game.is_move_possible(move_black_rook)
    assert not black_in_turn_game.is_move_possible(move_white_rook)


def test_game_in_turn_toggles():
    black_rook = figure_builder.build_rook(engine.Colour.BLACK, engine.Position(3, 3))
    white_rook = figure_builder.build_rook(engine.Colour.WHITE, engine.Position(4, 4))
    figures = (white_rook, black_rook)
    game = engine.Game(figures, engine.Colour.WHITE)
    assert game.in_turn == engine.Colour.WHITE
    game.make_move(engine.Move(engine.Position(4, 4), engine.Position(4, 5)))
    assert game.in_turn == engine.Colour.BLACK
    game.make_move(engine.Move(engine.Position(3, 3), engine.Position(3, 4)))
    assert game.in_turn == engine.Colour.WHITE


class TestGameIsCheck:
    @staticmethod
    def test_game_is_check():
        black_rook = figure_builder.build_rook(
            engine.Colour.BLACK, engine.Position(3, 4)
        )
        white_king = figure_builder.build_king(
            engine.Colour.WHITE, engine.Position(4, 4)
        )
        figures = (white_king, black_rook)
        game = engine.Game(figures, engine.Colour.WHITE)
        assert game.is_check()

    @staticmethod
    def test_game_is_check_false():
        black_rook = figure_builder.build_rook(
            engine.Colour.BLACK, engine.Position(3, 3)
        )
        white_king = figure_builder.build_king(
            engine.Colour.WHITE, engine.Position(4, 4)
        )
        figures = (white_king, black_rook)
        game = engine.Game(figures, engine.Colour.WHITE)
        assert not game.is_check()


class TestGameIsCheckMate:
    @staticmethod
    def test_game_is_checkmate():
        first_black_rook = figure_builder.build_rook(
            engine.Colour.BLACK, engine.Position(0, 7)
        )
        second_black_rook = figure_builder.build_rook(
            engine.Colour.BLACK, engine.Position(1, 7)
        )
        white_king = figure_builder.build_king(
            engine.Colour.WHITE, engine.Position(0, 0)
        )
        figures = (white_king, first_black_rook, second_black_rook)
        game = engine.Game(figures, engine.Colour.WHITE)
        assert game.is_checkmate()

    @staticmethod
    def test_game_is_check_but_not_checkmate():
        black_rook = figure_builder.build_rook(
            engine.Colour.BLACK, engine.Position(0, 7)
        )
        white_king = figure_builder.build_king(
            engine.Colour.WHITE, engine.Position(0, 0)
        )
        figures = (white_king, black_rook)
        game = engine.Game(figures, engine.Colour.WHITE)
        assert not game.is_checkmate()


def test_game_get_all_target_positions_must_resolve_check_situation():
    black_rook = figure_builder.build_rook(engine.Colour.BLACK, engine.Position(0, 7))
    white_king = figure_builder.build_king(engine.Colour.WHITE, engine.Position(0, 0))
    figures = (white_king, black_rook)
    game = engine.Game(figures, engine.Colour.WHITE)

    assert game.is_check()

    king_target_positions = game.get_all_target_positions(white_king.position)
    assert engine.Position(1, 0) in king_target_positions
    assert engine.Position(1, 1) in king_target_positions
    assert len(king_target_positions) == 2


def test_game_get_all_target_positions_cannot_introduce_check():
    black_rook = figure_builder.build_rook(engine.Colour.BLACK, engine.Position(1, 7))
    white_king = figure_builder.build_king(engine.Colour.WHITE, engine.Position(0, 0))
    figures = (white_king, black_rook)
    game = engine.Game(figures, engine.Colour.WHITE)

    king_target_positions = game.get_all_target_positions(white_king.position)
    assert len(king_target_positions) == 1
    assert engine.Position(0, 1) in king_target_positions


class TestGameIsCheckMate:
    @staticmethod
    def test_game_no_stalemate_when_figure_can_move():
        black_rook = figure_builder.build_rook(
            engine.Colour.BLACK, engine.Position(1, 7)
        )
        white_king = figure_builder.build_king(
            engine.Colour.WHITE, engine.Position(0, 0)
        )
        figures = (white_king, black_rook)
        game = engine.Game(figures, engine.Colour.WHITE)
        assert not game.is_stalemate()

    @staticmethod
    def test_game_no_stalemate_when_checkmate():
        first_black_rook = figure_builder.build_rook(
            engine.Colour.BLACK, engine.Position(0, 7)
        )
        second_black_rook = figure_builder.build_rook(
            engine.Colour.BLACK, engine.Position(1, 7)
        )
        white_king = figure_builder.build_king(
            engine.Colour.WHITE, engine.Position(0, 0)
        )
        figures = (white_king, first_black_rook, second_black_rook)
        game = engine.Game(figures, engine.Colour.WHITE)
        assert not game.is_stalemate()

    @staticmethod
    def test_game_is_stalemate():
        first_black_rook = figure_builder.build_rook(
            engine.Colour.BLACK, engine.Position(1, 7)
        )
        second_black_rook = figure_builder.build_rook(
            engine.Colour.BLACK, engine.Position(7, 1)
        )
        white_king = figure_builder.build_king(
            engine.Colour.WHITE, engine.Position(0, 0)
        )
        figures = (white_king, first_black_rook, second_black_rook)
        game = engine.Game(figures, engine.Colour.WHITE)
        assert game.is_stalemate()
