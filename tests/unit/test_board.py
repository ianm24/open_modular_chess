import numpy as np
import pytest

from omc.core.exception.exception import NegativePieceCoordinatesException
from omc.core.exception.exception import NegativePiecePlayerNumException
from omc.core.exception.exception import NonCurrentPiecePlayerNumException
from omc.core.exception.exception import PiecePixelHexOutOfBoundsException
from omc.core.exception.exception import PieceSubclassInvalidException
from omc.core.model.board import Board
from omc.core.model.board import Piece
from omc.core.model.board import Player

'''Board Class Tests'''


class SimplePiece(Piece):
    """
    Subclass used to test piece class
    """

    DEFAULT_PIECE_CHAR: str = 't'
    DEFAULT_PIECE_PIXEL_HEX: int = 0xFF18181818181818

    def list_moves(self) -> list[tuple[int, ...]]:
        """
        Implements list_moves for testing
        """
        return [(0, 1)]


'''AddPiece Tests'''


def test_board_add_piece():
    """
    Ensures proper function when adding a replacing piece
    """
    b = Board.empty(1, (8, 8))
    b.add_player(Player(1))
    p = SimplePiece(b)
    b.add_piece(p)

    assert b.query_space((0, 0)) == p


'''RemovePiece Tests'''


def test_remove_piece_different_board():
    """
    Ensures proper function when a piece is removed from a board it isn't on
    """
    expected_success = False

    b1 = Board.empty(1, (8, 8))
    b1.add_player(Player(1))
    p1 = SimplePiece(b1)
    b1.add_piece(p1)

    b2 = Board.empty(2, (8, 8))
    b2.add_player(Player(1))
    p2 = SimplePiece(b2)
    b2.add_piece(p2)

    actual_success = b1.remove_piece(p2)

    assert expected_success == actual_success
    assert b1.query_space(p1.current_coords) == p1


def test_remove_piece():
    """
    Ensures proper function when a piece is removed from a board
    """
    b = Board.empty(1, (8, 8))
    b.add_player(Player(1))
    p = SimplePiece(b)
    b.add_piece(p)
    b.remove_piece(p)

    assert b.query_space((0, 0)) is None
    assert p.current_coords is None


'''AddPlayer Tests'''


def test_add_player():
    """
    Ensures proper function when a player is added to a board
    """

    b = Board.empty(1, (8, 8))
    p = Player(1)
    b.add_player(p)

    expected_players = {1: p}

    assert np.array_equal(b.current_players, expected_players)


'''RemovePlayer Tests'''


def test_remove_player():
    """
    Ensures proper function when a player is removed from a board
    """

    b = Board.empty(1, (8, 8))
    p1 = Player(1)
    b.add_player(p1)
    p2 = Player(2)
    b.add_player(p2)

    b.remove_player(p2)

    expected_players = {1: p1}

    assert np.array_equal(b.current_players, expected_players)


'''GetPlayer Tests'''


def test_get_player():
    """
    Ensures proper function when a player is added to a board
    """

    b = Board.empty(1, (8, 8))
    p = Player(1)
    b.add_player(p)

    expected_player = p

    assert np.array_equal(b.get_player(1), expected_player)


'''__eq__ Tests'''


def test_board_not_equals():
    """
    Ensures proper function checking equality of 2 different boards
    """
    base_dimensions = (2, 2)
    base_board = Board.empty(1, base_dimensions)
    player = Player(1)
    base_board.add_player(player)

    diff_id_board = Board.empty(2, base_dimensions)
    diff_id_board.add_player(player)

    diff_dimension_board = Board.empty(1, (2, 1))
    diff_dimension_board.add_player(player)

    diff_layout_board = Board.empty(1, base_dimensions)
    diff_layout_board.add_player(player)
    p = SimplePiece(diff_layout_board)
    diff_layout_board.add_piece(p)

    diff_players_board = Board.empty(1, base_dimensions)
    diff_players_board.add_player(player)
    diff_players_board.add_player(Player(2))

    assert base_board != diff_id_board
    assert base_board != diff_dimension_board
    assert base_board != diff_layout_board
    assert base_board != diff_players_board


def test_board_equals():
    """
    Ensures proper function checking equality of 2 equivalent boards
    """
    b1 = Board.empty(1, (8, 8))
    b2 = Board.empty(1, (8, 8))

    assert b1 == b2


'''OnBoard Tests'''


def test_not_on_board():
    '''Ensures proper function when checking if a space out of bounds is on
    the board'''
    b = Board.empty(1, (8, 8))

    assert not b.on_board((-1, 0))
    assert not b.on_board((0, -1))
    assert not b.on_board((8, 0))
    assert not b.on_board((0, 8))


def test_on_board():
    '''Ensures proper function when checking if a space in bounds is on
    the board'''
    b = Board.empty(1, (8, 8))

    assert b.on_board((0, 0))


'''QuerySpace Tests'''


def test_query_out_of_bounds_space():
    '''Ensures proper function when querying an out of bounds space'''
    b = Board.empty(1, (8, 8))

    assert b.query_space((-1, 0)) is None
    assert b.query_space((0, -1)) is None
    assert b.query_space((8, 0)) is None
    assert b.query_space((0, 8)) is None


def test_query_space():
    '''Ensures proper function when querying a space'''
    b = Board.empty(1, (8, 8))
    b.add_player(Player(1))
    p = SimplePiece(b)
    b.add_piece(p)

    assert b.query_space((0, 0)) is p
    assert b.query_space((1, 0)) is None


'''Piece Class Tests'''


'''___init___ tests'''


class SimplePieceNoDefPieceChar(SimplePiece):
    """
    Subclass used to test default piece char
    """
    DEFAULT_PIECE_CHAR: str = ''


class SimplePieceNoDefPxlHex(SimplePiece):
    """
    Subclass used to test default pixel-hex
    """
    DEFAULT_PIECE_PIXEL_HEX: int = 0


def test_instantiate_base_piece():
    """
    Ensures proper function when a piece is instantiated by the base class.
    """
    with pytest.raises(NotImplementedError):
        Piece(
            Board.empty(1, (8, 8)), "", 1,
        )


def test_empty_default_piece_char():
    """
    Ensures proper function when a piece is has no default piece character.
    """
    with pytest.raises(PieceSubclassInvalidException):
        SimplePieceNoDefPieceChar(
            Board.empty(1, (8, 8)), "", 1,
        )


def test_empty_default_pxl_hex():
    """
    Ensures proper function when a piece has no default pixel hex.
    """
    with pytest.raises(PieceSubclassInvalidException):
        SimplePieceNoDefPxlHex(
            Board.empty(1, (8, 8)), "t", 1,
        )


def test_long_piece_char():
    """
    Ensures proper function when a piece has a piece character length > 1
    """
    expected_piece_char = 'T'

    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board, "Test", 1)

    assert p.piece_char == expected_piece_char


def test_piece_char_immutability():
    """
    Ensures proper function when a piece has an attempted piece_char edit
    """
    expected_piece_char = 't'

    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board, expected_piece_char, 1)

    with pytest.raises(AttributeError):
        p.piece_char = 'q'
    assert p.piece_char == expected_piece_char


def test_piece_char_default():
    """
    Ensures proper function when a piece is instantiated with default
    piece char
    """
    expected_piece_char = 't'

    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board)

    assert p.piece_char == expected_piece_char


def test_piece_char():
    """
    Ensures proper function when a piece has a valid piece character
    """
    expected_piece_char = 's'

    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board, expected_piece_char, 1)

    assert p.piece_char == expected_piece_char


def test_negative_piece_pxl_hex():
    """
    Ensures proper function when a piece has a negative pixel-hex
    """
    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))

    with pytest.raises(PiecePixelHexOutOfBoundsException):
        SimplePiece(test_board, 't', 0)


def test_large_piece_pxl_hex():
    """
    Ensures proper function when a piece has a pixel-hex > 64-bits
    """
    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))

    with pytest.raises(PiecePixelHexOutOfBoundsException):
        SimplePiece(Board.empty(1, (8, 8)), 't', 2 ** 64)


def test_piece_pxl_hex_immutability():
    """
    Ensures proper function when a piece has an attempted piece_pxl_hex edit
    """
    expected_piece_pxl_hex = 1

    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board, 't', expected_piece_pxl_hex)

    with pytest.raises(AttributeError):
        p.piece_pxl_hex = 2
    assert p.piece_pxl_hex == expected_piece_pxl_hex


def test_piece_pxl_hex_default():
    """
    Ensures proper function when a piece is instantiated with default pixel hex
    """
    expected_pxl_hex = 0xFF18181818181818

    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board, 't')

    assert p.piece_pxl_hex == expected_pxl_hex


def test_piece_pxl_hex():
    """
    Ensures proper function when a piece has a valid piece pixel-hex
    """
    expected_piece_pxl_hex = 1

    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board, 't', expected_piece_pxl_hex)

    assert p.piece_pxl_hex == 1


def test_negative_x_coord():
    """
    Ensures proper function when a piece has a negative x coordinate
    """
    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))
    with pytest.raises(NegativePieceCoordinatesException):
        SimplePiece(test_board, 't', 1, (-1, 0))


def test_negative_y_coord():
    """
    Ensures proper function when a piece has a negative y coordinate
    """
    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))
    with pytest.raises(NegativePieceCoordinatesException):
        SimplePiece(test_board, 't', 1, (0, -1))


def test_current_coords_immutability():
    """
    Ensures proper function when a piece has an attempted current_coords edit
    """
    expected_current_coords = (0, 0)

    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board, 't', 1, expected_current_coords)

    with pytest.raises(AttributeError):
        p.current_coords = (1, 1)
    assert np.array_equal(p.current_coords, expected_current_coords)


def test_current_coords_default():
    """
    Ensures proper function when a piece is instantiated with default
    piece char.
    """
    expected_current_coords = (0, 0)

    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board, 't', 1)

    assert np.array_equal(p.current_coords, expected_current_coords)


def test_current_coords():
    """
    Ensures proper function when a piece has valid current coordinates
    """
    expected_current_coords = (0, 1)

    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board, 't', 1, expected_current_coords)

    assert np.array_equal(p.current_coords, expected_current_coords)


def test_negative_player_controller():
    """
    Ensures proper function when a piece has a negative player controller
    """

    with pytest.raises(NegativePiecePlayerNumException):
        SimplePiece(Board.empty(1, (8, 8)), player_controller=-1)


def test_non_current_player_controller():
    """
    Ensures proper function when a piece has a non-current player controller
    """
    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))

    with pytest.raises(NonCurrentPiecePlayerNumException):
        SimplePiece(test_board, player_controller=2)


def test_player_controller_default():
    """
    Ensures proper function when a piece is instantiated with default
    piece char.
    """
    expected_player_controller = 1

    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board)

    assert p.player_controller == expected_player_controller


def test_player_controller():
    """
    Ensures proper function when a piece has valid player controller
    """
    expected_player_controller = 2

    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))
    test_board.add_player(Player(2))
    p = SimplePiece(test_board, player_controller=expected_player_controller)

    assert p.player_controller == expected_player_controller


'''Move Tests'''


def test_invalid_move():
    """
    Ensures proper function of move with invalid input
    """
    expected_current_coords = (0, 0)

    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board)

    assert p.move((2, 2)) is False
    assert np.array_equal(p.current_coords, expected_current_coords)


def test_move():
    """
    Ensures proper function of move with valid input
    """
    expected_current_coords = (0, 1)

    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board)
    test_board.add_piece(p)

    assert p.move(expected_current_coords) is True
    assert np.array_equal(p.current_coords, expected_current_coords)
    assert test_board.query_space(expected_current_coords) == p


'''SetPlayerControl Tests'''


def test_set_negative_player_control():
    """
    Ensures proper function of set_player_control with negative input
    """
    expected_player_controller = 1

    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(expected_player_controller))
    p = SimplePiece(test_board)

    assert p.set_player_control(-1) is False
    assert p.player_controller == expected_player_controller


def test_set_noncurrent_player_control():
    """
    Ensures proper function of set_player_control with noncurrent player
    """
    expected_player_controller = 1

    test_board = Board.empty(1, (8, 8))
    player = Player(expected_player_controller)
    test_board.add_player(player)
    piece = SimplePiece(test_board)
    player.add_piece(piece)

    assert piece.set_player_control(2) is False
    assert piece.player_controller == expected_player_controller
    assert piece in player.pieces


def test_set_player_control():
    """
    Ensures proper function of set_player_control with valid input
    """
    expected_player_controller = 2

    test_board = Board.empty(1, (8, 8))
    player1 = Player(1)
    player2 = Player(expected_player_controller)
    test_board.add_player(player1)
    test_board.add_player(player2)
    piece = SimplePiece(test_board)
    player1.add_piece(piece)

    assert piece.set_player_control(expected_player_controller) is True
    assert piece.player_controller == expected_player_controller
    assert piece not in test_board.get_player(1).pieces
    assert piece in player2.pieces


'''PerformAction Tests'''


def test_perform_invalid_action():
    """
    Ensures proper function of perform_action with valid input
    """
    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board)

    assert p.perform_action("test", []) is False


def test_perform_invalid_move_args_action():
    """
    Ensures proper function of perform_action with invalid move args
    """
    expected_current_coords = (0, 0)

    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board)

    assert p.perform_action("move", ["t", "1"]) is False
    assert p.perform_action("move", ["1", "t"]) is False
    assert np.array_equal(p.current_coords, expected_current_coords)


def test_perform_valid_move_action():
    """
    Ensures proper function of perform_action with valid move args
    """
    expected_current_coords = (0, 1)

    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board)

    assert p.perform_action("move", ["0", "1"]) is True
    assert np.array_equal(p.current_coords, expected_current_coords)


def test_perform_invalid_control_arg_action():
    """
    Ensures proper function of perform_action with invalid control arg
    """
    expected_player_controller = 1

    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board)

    assert p.perform_action("control", ["t"]) is False
    assert p.player_controller == expected_player_controller


def test_perform_valid_control_arg_action():
    """
    Ensures proper function of perform_action with valid move arg
    """
    expected_player_controller = 0

    test_board = Board.empty(1, (8, 8))
    test_board.add_player(Player(expected_player_controller))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board)

    assert p.perform_action("control", ["0"]) is True
    assert p.player_controller == expected_player_controller


'''Player Class Tests'''

'''__init__ tests'''


def test_player_number_immutable():
    """
    Ensures proper function when a player has an attempted player_number edit
    """
    expected_player_number = 1

    p = Player(1)

    with pytest.raises(AttributeError):
        p.player_number = 2
    assert p.player_number == expected_player_number


'''AddPiece Tests'''


def test_player_add_piece_not_controlled():
    """
    Ensures proper function when a player adds a piece it doesn't control
    """
    expected_success = False

    test_board = Board.empty(1, (8, 8))
    player2 = Player(2)
    test_board.add_player(Player(1))
    test_board.add_player(player2)
    piece = SimplePiece(test_board)

    actual_success = player2.add_piece(piece)

    assert expected_success == actual_success
    assert piece not in player2.pieces


def test_player_add_piece():
    """
    Ensures proper function when a player adds a valid piece
    """
    test_board = Board.empty(1, (8, 8))
    player = Player(1)
    test_board.add_player(player)
    piece = SimplePiece(test_board)

    assert player.add_piece(piece) is True


def test_player_add_piece_already_added():
    """
    Ensures proper function when a player adds a piece it already controlls
    """
    test_board = Board.empty(1, (8, 8))
    player = Player(1)
    test_board.add_player(player)
    piece = SimplePiece(test_board)
    player.add_piece(piece)

    assert player.add_piece(piece) is False


def test_player_threatened_spaces():
    """
    Ensures proper function when player checks threatened spaces
    """

    b = Board.empty(1, (8, 8))
    p = Player(1)
    b.add_player(p)
    piece = SimplePiece(b)
    b.add_piece(piece)

    expected_area = []
    actual_area = p.threatened_spaces

    assert actual_area == expected_area


def test_player_update_threatened_spaces():
    """
    Ensures proper function when player updates threatened spaces
    """

    b = Board.empty(1, (8, 8))
    p = Player(1)
    b.add_player(p)
    piece = SimplePiece(b)
    b.add_piece(piece)
    p.add_piece(piece)

    expected_area = [(0, 1)]
    actual_area = p.threatened_spaces

    assert actual_area == expected_area


def test_player_lose_condition_not_implemented():
    """
    Ensures proper function when player lose condition isnt implemented
    """

    with pytest.raises(NotImplementedError):
        Player(1).check_lose_condition()


def test_player_draw_condition_not_implemented():
    """
    Ensures proper function when player draw condition isnt implemented
    """

    with pytest.raises(NotImplementedError):
        Player(1).check_draw_condition()


def test_player_win_condition_not_implemented():
    """
    Ensures proper function when player win condition isnt implemented
    """

    with pytest.raises(NotImplementedError):
        Player(1).check_win_condition()
