import pytest
from core.exception.exception import MissingPieceCharException
from core.exception.exception import NegativePieceCoordinatesException
from core.exception.exception import NegativePiecePlayerNumException
from core.exception.exception import PiecePxlHexOutOfBoundsException
from core.model.board import Board
from core.model.piece import Piece
# TODO uncomment this once board updated with current_players
# from core.exception.exception import NonCurrentPiecePlayerNumException

'''___init___ tests'''


def test_missing_piece_char():
    """Ensures proper function when a piece has an empty piece character"""
    with pytest.raises(MissingPieceCharException):
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
    with pytest.raises(PiecePxlHexOutOfBoundsException):
        Piece('t', -1, Board.empty())


def test_large_piece_pxl_hex():
    """Ensures proper function when a piece has a pixel-hex > 64-bits"""
    with pytest.raises(PiecePxlHexOutOfBoundsException):
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


# TODO uncomment this once board updated with current_players
# def test_non_current_player_controller():
#     """Ensures proper function when a piece has a non-current
#     player controller"""
#     with pytest.raises(NonCurrentPiecePlayerNumException):
#         Piece('t', 1, Board(1, 1, [""],
#                             current_players=[0, 1, 2]), player_controller=3)


def test_player_controller():
    """Ensures proper function when a piece has valid player controller"""
#         Piece('t', 1, Board(1, 1, [""],
#                             current_players=[0, 1, 2]), player_controller=3)
    p = Piece('t', 1, Board.empty(), player_controller=2)
    # TODO replace with commented line once board updated
    assert p.player_controller == 2


'''Move Tests'''


def test_invalid_move():
    '''Ensures proper function of move with invalid input'''
    p = Piece('t', 1, Board.empty())
    assert p.move((2, 2)) is False and p.current_coords == (0, 0)


def test_move():
    '''Ensures proper function of move with valid input'''
    p = Piece('t', 1, Board.empty())
    assert p.move((0, 1)) is True and p.current_coords == (0, 1)


'''SetPlayerControl Tests'''


def test_set_negative_player_control():
    '''Ensures proper function of set_player_control with negative input'''
    p = Piece('t', 1, Board.empty())
    assert p.set_player_control(-1) is False and p.player_controller == 1


def test_set_noncurrent_player_control():
    '''Ensures proper function of set_player_control with noncurrent player'''
    p = Piece('t', 1, Board.empty())
    assert p.set_player_control(3) is False and p.player_controller == 1


def test_set_player_control():
    '''Ensures proper function of set_player_control with valid input'''
    p = Piece('t', 1, Board.empty())
    assert p.set_player_control(0) is True and p.player_controller == 0


'''PerformAction Tests'''


def test_perform_invalid_action():
    '''Ensures proper function of perform_action with valid input'''
    p = Piece('t', 1, Board.empty())
    assert p.perform_action("test", []) is False


def test_perform_invalid_move_args_action():
    '''Ensures proper function of perform_action with invalid move args'''
    p = Piece('t', 1, Board.empty())
    assert p.perform_action("move", ["t", "1"]) is False and p.perform_action(
        "move", ["1", "t"]) is False and p.current_coords == (0, 0)


def test_perform_valid_move_action():
    '''Ensures proper function of perform_action with valid move args'''
    p = Piece('t', 1, Board.empty())
    assert p.perform_action(
        "move", ["0", "1"]) is True and p.current_coords == (0, 1)


def test_perform_invalid_control_arg_action():
    '''Ensures proper function of perform_action with invalid control arg'''
    p = Piece('t', 1, Board.empty())
    assert p.perform_action(
        "control", ["t"]) is False and p.player_controller == 1


def test_perform_valid_control_arg_action():
    '''Ensures proper function of perform_action with valid move arg'''
    p = Piece('t', 1, Board.empty())
    assert p.perform_action(
        "control", ["0"]) is True and p.player_controller == 0
