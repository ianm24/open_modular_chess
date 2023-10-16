from typing import Optional

import pytest

from src.core.exception.exception import MissingPieceCharException
from src.core.exception.exception import NegativePieceCoordinatesException
from src.core.exception.exception import NegativePiecePlayerNumException
from src.core.exception.exception import NonCurrentPiecePlayerNumException
from src.core.exception.exception import PiecePixelHexOutOfBoundsException
from src.core.model.board import Board
from src.core.model.piece import Piece

'''___init___ tests'''


def test_missing_piece_char():
    """Ensures proper function when a piece has an empty piece character"""
    expected_message = ("Error: Piece character for piece Piece is missing."
                        " Please set piece character to a 1 character string.")
    with pytest.raises(MissingPieceCharException, match=expected_message):
        Piece("", 1, Board.empty(), (1, 1), 1)


def test_long_piece_char():
    """Ensures proper function when a piece has a piece character length > 1"""
    p = Piece("Test", 1, Board.empty())
    assert p.piece_char == 'T'


def test_piece_char_immutability():
    """Ensures proper function when a piece has a piece character length > 1"""
    p = Piece('t', 1, Board.empty())
    with pytest.raises(AttributeError):
        p.piece_char = 'q'


def test_piece_char():
    """Ensures proper function when a piece has a valid piece character"""
    p = Piece('t', 1, Board.empty())
    assert p.piece_char == 't'


def test_negative_piece_pxl_hex():
    """Ensures proper function when a piece has a negative pixel-hex"""
    with pytest.raises(PiecePixelHexOutOfBoundsException):
        Piece('t', -1, Board.empty())


def test_large_piece_pxl_hex():
    """Ensures proper function when a piece has a pixel-hex > 64-bits"""
    with pytest.raises(PiecePixelHexOutOfBoundsException):
        Piece('t', 2**64, Board.empty())


def test_piece_pxl_hex_immutability():
    """Ensures proper function when a piece has a piece character length > 1"""
    p = Piece('t', 1, Board.empty())
    with pytest.raises(AttributeError):
        p.piece_pxl_hex = 2


def test_piece_pxl_hex():
    """Ensures proper function when a piece has a valid piece pixel-hex"""
    p = Piece('t', 1, Board.empty())
    assert p.piece_pxl_hex == 1


def test_empty_current_coords():
    """Ensures proper function when a piece has empty current_coords"""
    p = Piece("Test", 1, Board.empty())
    assert p.current_coords == (0, 0)


def test_negative_x_coord():
    """Ensures proper function when a piece has a negative x coordinate"""
    with pytest.raises(NegativePieceCoordinatesException):
        Piece('t', 1, Board.empty(), (-1, 0))


def test_negative_y_coord():
    """Ensures proper function when a piece has a negative y coordinate"""
    with pytest.raises(NegativePieceCoordinatesException):
        Piece('t', 1, Board.empty(), (0, -1))


def test_current_coords_immutability():
    """Ensures proper function when a piece has a piece character length > 1"""
    p = Piece('t', 1, Board.empty())
    with pytest.raises(AttributeError):
        p.current_coords = (1, 1)


def test_current_coords():
    """Ensures proper function when a piece has valid current coordinates"""
    p = Piece('t', 1, Board.empty(), (1, 1))
    assert p.current_coords == (1, 1)


def test_negative_player_controller():
    """Ensures proper function when a piece has a negative player controller"""
    with pytest.raises(NegativePiecePlayerNumException):
        Piece('t', 1, Board.empty(), player_controller=-1)


@pytest.mark.skip(reason="Board not finished")
def test_non_current_player_controller():
    """Ensures proper function when a piece has a non-current
    player controller"""
    with pytest.raises(NonCurrentPiecePlayerNumException):
        Piece('t', 1, Board(1, 1, [""],
                            current_players=[0, 1, 2]), player_controller=3)


@pytest.mark.skip(reason="Board not finished")
def test_player_controller():
    """Ensures proper function when a piece has valid player controller"""
    p = Piece('t', 1, Board(1, 1, [""],
                            current_players=[0, 1, 2]), player_controller=3)
    assert p.player_controller == 2


'''Move Tests'''


class SimplePiece(Piece):
    """Used to test move method"""

    def __init__(
            self, piece_char: str, piece_pxl_hex: int, board: Board,
            current_coords: Optional[tuple[int, int]] = None,
            player_controller: Optional[int] = None
    ):
        '''
        Calls parent constructor for test class
        '''
        super().__init__(piece_char, piece_pxl_hex,
                         board, current_coords,
                         player_controller)

    def list_moves(self) -> list[Optional[tuple[int, int]],]:
        '''
        Implements list_moves for testing
        '''
        return [(0, 1)]


def test_invalid_move():
    '''Ensures proper function of move with invalid input'''
    p = SimplePiece('t', 1, Board.empty())
    assert p.move((2, 2)) is False
    assert p.current_coords == (0, 0)


def test_move():
    '''Ensures proper function of move with valid input'''
    p = SimplePiece('t', 1, Board.empty())
    assert p.move((0, 1)) is True
    assert p.current_coords == (0, 1)


'''SetPlayerControl Tests'''


def test_set_negative_player_control():
    '''Ensures proper function of set_player_control with negative input'''
    p = Piece('t', 1, Board.empty())
    assert p.set_player_control(-1) is False
    assert p.player_controller == 1


def test_set_noncurrent_player_control():
    '''Ensures proper function of set_player_control with noncurrent player'''
    p = Piece('t', 1, Board.empty())
    assert p.set_player_control(3) is False
    assert p.player_controller == 1


def test_set_player_control():
    '''Ensures proper function of set_player_control with valid input'''
    p = Piece('t', 1, Board.empty())
    assert p.set_player_control(0) is True
    assert p.player_controller == 0


'''PerformAction Tests'''


def test_perform_invalid_action():
    '''Ensures proper function of perform_action with valid input'''
    p = Piece('t', 1, Board.empty())
    assert p.perform_action("test", []) is False


def test_perform_invalid_move_args_action():
    '''Ensures proper function of perform_action with invalid move args'''
    p = Piece('t', 1, Board.empty())
    assert p.perform_action("move", ["t", "1"]) is False
    assert p.perform_action("move", ["1", "t"]) is False
    assert p.current_coords == (0, 0)


def test_perform_valid_move_action():
    '''Ensures proper function of perform_action with valid move args'''
    p = SimplePiece('t', 1, Board.empty())
    assert p.perform_action("move", ["0", "1"]) is True
    assert p.current_coords == (0, 1)


def test_perform_invalid_control_arg_action():
    '''Ensures proper function of perform_action with invalid control arg'''
    p = Piece('t', 1, Board.empty())
    assert p.perform_action("control", ["t"]) is False
    assert p.player_controller == 1


def test_perform_valid_control_arg_action():
    '''Ensures proper function of perform_action with valid move arg'''
    p = Piece('t', 1, Board.empty())
    assert p.perform_action("control", ["0"]) is True
    assert p.player_controller == 0
