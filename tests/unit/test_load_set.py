# Code by Chandler McDowell 2023
from os import remove
from os.path import exists

import pytest
from core import load_set
from core.exception.exception import BoardNotFoundException
from core.exception.exception import BoardValidationFailedException
from core.exception.exception import EmptyBoardException
from core.exception.exception import InvalidBoardDimensionException
from core.exception.exception import InvalidBoardFormatException
from core.exception.exception import InvalidBoardLayoutException
from core.exception.exception import PiecesEmptyException
from core.exception.exception import PiecesNotFoundException
from core.exception.exception import SetNotFoundException
from core.model.board import Board

# Load ensure commit file title
EC = "ensure_commit.txt"

'''LoadSet tests'''


def test_incorrect_set_name():
    """Ensures proper function when a set name is incorrect"""
    with pytest.raises(SetNotFoundException):
        load_set.load_set("test_sets/test_set_incorrect_set_name")


'''GetPieceNames tests'''


def test_missing_pieces_directory():
    """Ensures proper function when a set does not contain a pieces
    directory"""
    with pytest.raises(PiecesNotFoundException):
        load_set.get_piece_names("test_sets/test_set_missing_pieces_directory")


def test_empty_pieces_directory():
    """Ensures proper function when a set has an empty pieces directory"""

    # Remove the ensure commit file to create empty directory
    set_dir = "test_sets/test_set_empty_pieces_directory/"

    if exists("../resources/sets/" + set_dir + "pieces/" + EC):
        remove("../resources/sets/" + set_dir + "pieces/" + EC)

    # Run the test
    with pytest.raises(PiecesEmptyException):
        load_set.get_piece_names(set_dir, test_flag=True)

    # Recreate the ensure commit file
    file = open("../resources/sets/" + set_dir + "pieces/" + EC, "x")
    file.close()


def test_get_piece_names():
    """Ensures the correct piece names are gotten for a set"""
    base_set_names = ['bishop', 'king', 'knight', 'pawn', 'queen', 'rook']
    assert load_set.get_piece_names("base_set") == base_set_names


'''GetBoard tests'''


def test_missing_board_file():
    """Ensures proper function when a set does not contain a board file"""
    with pytest.raises(BoardNotFoundException):
        load_set.get_board("test_sets/test_set_missing_board_file")


def test_board_unicode_decode_error():
    """Ensures proper function when a set contains a board that is an invalid
    csv-type file"""
    with pytest.raises(InvalidBoardLayoutException):
        load_set.get_board("test_sets/test_set_board_unicode_decode_error")


def test_empty_board_file():
    """Ensures proper function when a set has an empty board file"""
    with pytest.raises(EmptyBoardException):
        load_set.get_board("test_sets/test_set_empty_board_file")


def test_board_row_dimension_type():
    """Ensures proper function when a set has a board with non-integer row
    dimension"""
    with pytest.raises(InvalidBoardDimensionException):
        load_set.get_board("test_sets/test_set_board_row_dimension_type")


def test_board_column_dimension_type():
    """Ensures proper function when a set has a board with non-integer column
    dimension"""
    with pytest.raises(InvalidBoardDimensionException):
        load_set.get_board("test_sets/test_set_board_column_dimension_type")


def test_invalid_board_layout_value():
    """Ensures proper function when a set has a board with an invalid value
    type in board layout"""
    with pytest.raises(InvalidBoardLayoutException):
        load_set.get_board("test_sets/test_set_invalid_board_layout_value")


def test_extra_values_board():
    """Ensures proper function when a set has a board with extra values"""
    with pytest.raises(InvalidBoardFormatException):
        load_set.get_board("test_sets/test_set_extra_values_board")


def test_invalid_board():
    """Ensures proper function when a set has a board with non-integer column
    dimension"""
    with pytest.raises(InvalidBoardFormatException):
        load_set.get_board("test_sets/test_set_extra_values_board")


def test_get_board():
    """Ensures the correct board is gotten for a set"""
    base_set_board = Board(8, 8, [
        ['p2_rook', 'p2_knight', 'p2_bishop', 'p2_king',
         'p2_queen', 'p2_bishop', 'p2_knight', 'p2_rook'],
        ['p2_pawn', 'p2_pawn', 'p2_pawn', 'p2_pawn',
         'p2_pawn', 'p2_pawn', 'p2_pawn', 'p2_pawn'],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['p1_pawn', 'p1_pawn', 'p1_pawn', 'p1_pawn',
         'p1_pawn', 'p1_pawn', 'p1_pawn', 'p1_pawn'],
        ['p1_rook', 'p1_knight', 'p1_bishop', 'p1_king', 'p1_queen',
         'p1_bishop', 'p1_knight', 'p1_rook']])

    result = load_set.get_board("base_set")
    assert result == base_set_board


'''ValidateBoard tests'''


def test_nonpos_board_dimension():
    """Ensures proper function when a set has a board with non-positive
    dimensions"""
    with pytest.raises(BoardValidationFailedException):
        load_set.get_board("test_sets/test_set_nonpos_board_dimension_1")
    with pytest.raises(BoardValidationFailedException):
        load_set.get_board("test_sets/test_set_nonpos_board_dimension_2")


def test_board_layout_num_rows():
    """Ensures proper function when a set has a board with a number of rows
    different that what is stated
    previously in the board file"""
    with pytest.raises(BoardValidationFailedException):
        load_set.get_board("test_sets/test_set_board_layout_num_rows")


def test_board_layout_num_cols():
    """Ensures proper function when a set has a board with a number of cols
    different that what is stated
    previously in the board file"""
    with pytest.raises(BoardValidationFailedException):
        load_set.get_board("test_sets/test_set_board_layout_num_cols")


def test_nonstring_board_piece():
    """Ensures proper function when a set has a board has a non-string value
    in the board layout"""
    with pytest.raises(BoardValidationFailedException):
        load_set.get_board("test_sets/test_set_nonstring_board_piece")


def test_invalid_player_prefix_board_piece():
    """Ensures proper function when a set has a board has an invalid player
    prefix for a board piece"""
    with pytest.raises(BoardValidationFailedException):
        load_set.get_board(
            "test_sets/test_set_invalid_player_prefix_board_piece")


def test_invalid_player_suffix_board_piece():
    """Ensures proper function when a set has a board has an invalid player
    suffix for a board piece"""
    with pytest.raises(BoardValidationFailedException):
        load_set.get_board(
            "test_sets/test_set_invalid_player_suffix_board_piece")


def test_validate_board():
    """Ensures a valid board is validated"""
    base_set_board = Board(8, 8, [
        ['p2_rook', 'p2_knight', 'p2_bishop', 'p2_king',
         'p2_queen', 'p2_bishop', 'p2_knight', 'p2_rook'],
        ['p2_pawn', 'p2_pawn', 'p2_pawn', 'p2_pawn',
         'p2_pawn', 'p2_pawn', 'p2_pawn', 'p2_pawn'],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['p1_pawn', 'p1_pawn', 'p1_pawn', 'p1_pawn',
         'p1_pawn', 'p1_pawn', 'p1_pawn', 'p1_pawn'],
        ['p1_rook', 'p1_knight', 'p1_bishop', 'p1_king',
            'p1_queen', 'p1_bishop', 'p1_knight', 'p1_rook']
    ])
    assert load_set.validate_board(base_set_board, "base_set") is True
