from typing import Optional

import numpy as np
import pytest

from omc.core.exception.exception import NegativePieceCoordinatesException
from omc.core.exception.exception import NegativePiecePlayerNumException
from omc.core.exception.exception import NonCurrentPiecePlayerNumException
from omc.core.exception.exception import PiecePixelHexOutOfBoundsException
from omc.core.exception.exception import PieceSubclassInvalidException
from omc.core.exception.exception import PlayerNotControllingPieceException
from omc.core.model.board import Board
from omc.core.model.board import Piece
from omc.core.model.board import Player

'''Board Class Tests'''

'''Piece Class Tests'''


class SimplePiece(Piece):
    """
    Subclass used to test piece class
    """

    DEFAULT_PIECE_CHAR: str = 't'
    DEFAULT_PIECE_PIXEL_HEX: int = 0xFF18181818181818

    def list_moves(self) -> list[Optional[tuple[int, int]],]:
        """
        Implements list_moves for testing
        """
        return [np.asarray([0, 1])]


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
            Board.empty(np.array([8, 8])), "", 1,
        )


def test_empty_default_piece_char():
    """
    Ensures proper function when a piece is has no default piece character.
    """
    with pytest.raises(PieceSubclassInvalidException):
        SimplePieceNoDefPieceChar(
            Board.empty(np.array([8, 8])), "", 1,
        )


def test_empty_default_pxl_hex():
    """
    Ensures proper function when a piece has no default pixel hex.
    """
    with pytest.raises(PieceSubclassInvalidException):
        SimplePieceNoDefPxlHex(
            Board.empty(np.array([8, 8])), "t", 1,
        )


def test_long_piece_char():
    """
    Ensures proper function when a piece has a piece character length > 1
    """
    expected_piece_char = 'T'

    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board, "Test", 1)

    assert p.piece_char == expected_piece_char


def test_piece_char_immutability():
    """
    Ensures proper function when a piece has an attempted piece_char edit
    """
    expected_piece_char = 't'

    test_board = Board.empty(np.array([8, 8]))
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

    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board)

    assert p.piece_char == expected_piece_char


def test_piece_char():
    """
    Ensures proper function when a piece has a valid piece character
    """
    expected_piece_char = 's'

    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board, 's', 1)

    assert p.piece_char == expected_piece_char


def test_negative_piece_pxl_hex():
    """
    Ensures proper function when a piece has a negative pixel-hex
    """
    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(1))

    with pytest.raises(PiecePixelHexOutOfBoundsException):
        SimplePiece(test_board, 't', 0)


def test_large_piece_pxl_hex():
    """
    Ensures proper function when a piece has a pixel-hex > 64-bits
    """
    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(1))

    with pytest.raises(PiecePixelHexOutOfBoundsException):
        SimplePiece(Board.empty(np.array([8, 8])), 't', 2 ** 64)


def test_piece_pxl_hex_immutability():
    """
    Ensures proper function when a piece has an attempted piece_pxl_hex edit
    """
    expected_piece_pxl_hex = 1

    test_board = Board.empty(np.array([8, 8]))
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

    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board, 't')

    assert p.piece_pxl_hex == expected_pxl_hex


def test_piece_pxl_hex():
    """
    Ensures proper function when a piece has a valid piece pixel-hex
    """
    expected_piece_pxl_hex = 1

    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board, 't', expected_piece_pxl_hex)

    assert p.piece_pxl_hex == 1


def test_negative_x_coord():
    """
    Ensures proper function when a piece has a negative x coordinate
    """
    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(1))
    with pytest.raises(NegativePieceCoordinatesException):
        SimplePiece(test_board, 't', 1, np.asarray([-1, 0]))


def test_negative_y_coord():
    """
    Ensures proper function when a piece has a negative y coordinate
    """
    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(1))
    with pytest.raises(NegativePieceCoordinatesException):
        SimplePiece(test_board, 't', 1, np.asarray([0, -1]))


def test_current_coords_immutability():
    """
    Ensures proper function when a piece has an attempted current_coords edit
    """
    expected_current_coords = np.asarray([0, 0])

    test_board = Board.empty(np.array([8, 8]))
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
    expected_current_coords = np.asarray([0, 0])

    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board, 't', 1)

    assert np.array_equal(p.current_coords, expected_current_coords)


def test_current_coords():
    """
    Ensures proper function when a piece has valid current coordinates
    """
    expected_current_coords = np.asarray([0, 1])

    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board, 't', 1, expected_current_coords)

    assert np.array_equal(p.current_coords, expected_current_coords)


def test_negative_player_controller():
    """
    Ensures proper function when a piece has a negative player controller
    """

    with pytest.raises(NegativePiecePlayerNumException):
        SimplePiece(Board.empty(np.array([8, 8])), player_controller=-1)


def test_non_current_player_controller():
    """
    Ensures proper function when a piece has a non-current player controller
    """
    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(1))

    with pytest.raises(NonCurrentPiecePlayerNumException):
        SimplePiece(test_board, player_controller=2)


def test_player_controller_default():
    """
    Ensures proper function when a piece is instantiated with default
    piece char.
    """
    expected_player_controller = 1

    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board)

    assert p.player_controller == expected_player_controller


def test_player_controller():
    """
    Ensures proper function when a piece has valid player controller
    """
    expected_player_controller = 2

    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(1))
    test_board.add_player(Player(2))
    p = SimplePiece(test_board, player_controller=expected_player_controller)

    assert p.player_controller == expected_player_controller


'''Move Tests'''


@pytest.mark.xfail(reason="Move should support ndarrays when checking valid"
                   " moves.")
def test_invalid_move():
    """
    Ensures proper function of move with invalid input
    """
    expected_current_coords = np.asarray([0, 0])

    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board)

    assert p.move(np.asarray([2, 2])) is False
    assert np.array_equal(p.current_coords, expected_current_coords)


@pytest.mark.xfail(reason="Move should support ndarrays when checking valid"
                   " moves. Piece should update board on move")
def test_move():
    """
    Ensures proper function of move with valid input
    """
    expected_current_coords = np.asarray([0, 1])

    test_board = Board.empty(np.array([8, 8]))
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

    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(expected_player_controller))
    p = SimplePiece(test_board)

    assert p.set_player_control(-1) is False
    assert p.player_controller == expected_player_controller


def test_set_noncurrent_player_control():
    """
    Ensures proper function of set_player_control with noncurrent player
    """
    expected_player_controller = 1

    test_board = Board.empty(np.array([8, 8]))
    player = Player(expected_player_controller)
    test_board.add_player(player)
    piece = SimplePiece(test_board)
    player.add_piece(piece)

    assert piece.set_player_control(2) is False
    assert piece.player_controller == expected_player_controller
    assert piece in player.pieces


@pytest.mark.xfail(reason="Player pieces not updated on set player controller")
def test_set_player_control():
    """
    Ensures proper function of set_player_control with valid input
    """
    expected_player_controller = 2

    test_board = Board.empty(np.array([8, 8]))
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


'''Capture Tests'''


@pytest.mark.xfail(reason="Piece should update board prior to setting "
                   "coordinates to None")
def test_invalid_player_capture():
    """
    Ensures proper function of capture with invalid player
    """
    expected_player_controller = 1

    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(expected_player_controller))
    test_board.add_player(Player(2))
    p = SimplePiece(test_board)

    assert p.capture(3) is False
    assert p.player_controller == expected_player_controller


@pytest.mark.xfail(reason="Piece should update board prior to setting "
                   "coordinates to None")
def test_capture():
    """
    Ensures proper function of capture with valid player
    """
    expected_player_controller = 2
    piece_coords = np.asarray([0, 0])

    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(1))
    test_board.add_player(Player(expected_player_controller))
    p = SimplePiece(test_board)
    test_board.add_piece(p)

    assert p.capture(expected_player_controller) is True
    assert p.player_controller == expected_player_controller
    assert test_board.query_space(piece_coords) is None


'''PerformAction Tests'''


def test_perform_invalid_action():
    """
    Ensures proper function of perform_action with valid input
    """
    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board)

    assert p.perform_action("test", []) is False


def test_perform_invalid_move_args_action():
    """
    Ensures proper function of perform_action with invalid move args
    """
    expected_current_coords = np.asarray([0, 0])

    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board)

    assert p.perform_action("move", ["t", "1"]) is False
    assert p.perform_action("move", ["1", "t"]) is False
    assert np.array_equal(p.current_coords, expected_current_coords)


@pytest.mark.xfail(reason="Piece should update board prior to setting "
                   "coordinates to None")
def test_perform_valid_move_action():
    """
    Ensures proper function of perform_action with valid move args
    """
    expected_current_coords = np.asarray([0, 1])

    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board)

    assert p.perform_action("move", ["0", "1"]) is True
    assert np.array_equal(p.current_coords, expected_current_coords)


def test_perform_invalid_control_arg_action():
    """
    Ensures proper function of perform_action with invalid control arg
    """
    expected_player_controller = 1

    test_board = Board.empty(np.array([8, 8]))
    test_board.add_player(Player(1))
    p = SimplePiece(test_board)

    assert p.perform_action("control", ["t"]) is False
    assert p.player_controller == expected_player_controller


def test_perform_valid_control_arg_action():
    """
    Ensures proper function of perform_action with valid move arg
    """
    expected_player_controller = 0

    test_board = Board.empty(np.array([8, 8]))
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


@pytest.mark.xfail(reason="Add piece does not yet check player controller")
def test_add_piece_not_controlled():
    """
    Ensures proper functionality when a player adds a piece it doesn't control
    """
    test_board = Board.empty(np.array([8, 8]))
    player2 = Player(2)
    test_board.add_player(Player(1))
    test_board.add_player(player2)
    piece = SimplePiece(test_board)

    with pytest.raises(PlayerNotControllingPieceException):
        player2.add_piece(piece)
    assert piece not in player2.pieces


@pytest.mark.xfail(reason="Add piece does not return a success boolean")
def test_add_piece():
    """
    Ensures proper functionality when a player adds a valid piece
    """
    test_board = Board.empty(np.array([8, 8]))
    player = Player(1)
    test_board.add_player(player)
    piece = SimplePiece(test_board)

    assert player.add_piece(piece) is True
