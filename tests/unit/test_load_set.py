# Code by Chandler McDowell 2023
from os import remove
from os.path import exists

import numpy as np
import pytest

from omc.core import load_set
from omc.core.exception.exception import BoardNotFoundException
from omc.core.exception.exception import EmptyBoardException
from omc.core.exception.exception import InvalidBoardDimensionException
from omc.core.exception.exception import InvalidBoardFormatException
from omc.core.exception.exception import InvalidBoardLayoutException
from omc.core.exception.exception import PiecesEmptyException
from omc.core.exception.exception import PiecesNotFoundException
from omc.core.exception.exception import SetNotFoundException
from omc.core.model.board import Board

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
        load_set.get_piece_map("test_sets/test_set_missing_pieces_directory")


def test_empty_pieces_directory():
    """Ensures proper function when a set has an empty pieces directory"""

    # Remove the ensure commit file to create empty directory
    set_dir = "test_sets/test_set_empty_pieces_directory/"

    if exists("./resources/sets/" + set_dir + "pieces/" + EC):
        remove("./resources/sets/" + set_dir + "pieces/" + EC)

    # Run the test
    with pytest.raises(PiecesEmptyException):
        load_set.get_piece_map(set_dir)

    # Recreate the ensure commit file
    file = open("./resources/sets/" + set_dir + "pieces/" + EC, "x")
    file.close()


def test_get_piece_names():
    """Ensures the correct piece names are gotten for a set"""
    expected_base_set_names = {
        'bishop',
        'king',
        'knight',
        'pawn',
        'queen',
        'rook'
    }
    actual_base_set_names = set(load_set.get_piece_map("base_set").keys())
    assert actual_base_set_names == expected_base_set_names


'''GetBoard tests'''


def test_missing_board_file():
    """Ensures proper function when a set does not contain a board file"""
    with pytest.raises(BoardNotFoundException):
        base_set_piece_map = dict()
        load_set.get_board(
            "test_sets/test_set_missing_board_file", base_set_piece_map
        )


def test_board_unicode_decode_error():
    """Ensures proper function when a set contains a board that is an invalid
    csv-type file"""
    with pytest.raises(InvalidBoardLayoutException):
        base_set_piece_map = dict()
        load_set.get_board(
            "test_sets/test_set_board_unicode_decode_error", base_set_piece_map
        )


def test_empty_board_file():
    """Ensures proper function when a set has an empty board file"""
    with pytest.raises(EmptyBoardException):
        base_set_piece_map = dict()
        load_set.get_board(
            "test_sets/test_set_empty_board_file", base_set_piece_map
        )


def test_board_row_dimension_type():
    """Ensures proper function when a set has a board with non-integer row
    dimension"""
    with pytest.raises(InvalidBoardDimensionException):
        base_set_piece_map = dict()
        load_set.get_board(
            "test_sets/test_set_board_row_dimension_type",
            base_set_piece_map
        )


def test_board_column_dimension_type():
    """Ensures proper function when a set has a board with non-integer column
    dimension"""
    with pytest.raises(InvalidBoardDimensionException):
        base_set_piece_map = dict()
        load_set.get_board(
            "test_sets/test_set_board_column_dimension_type",
            base_set_piece_map
        )


def test_invalid_board_layout_value():
    """Ensures proper function when a set has a board with an invalid value
    type in board layout"""
    with pytest.raises(InvalidBoardLayoutException):
        base_set_piece_map = dict()
        load_set.get_board(
            "test_sets/test_set_invalid_board_layout_value",
            base_set_piece_map
        )


def test_extra_values_board():
    """Ensures proper function when a set has a board with extra values"""
    with pytest.raises(InvalidBoardFormatException):
        base_set_piece_map = dict()
        load_set.get_board(
            "test_sets/test_set_extra_values_board", base_set_piece_map
        )


def test_invalid_board():
    """Ensures proper function when a set has a board with non-integer column
    dimension"""
    with pytest.raises(InvalidBoardFormatException):
        base_set_piece_map = dict()
        load_set.get_board(
            "test_sets/test_set_extra_values_board", base_set_piece_map
        )


@pytest.mark.xfail(reason="Needs to be adapted to new Board structure")
def test_get_board():
    """Ensures the correct board is gotten for a set"""
    base_set_board = Board(np.array([8, 8]), np.array([
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
         'p1_bishop', 'p1_knight', 'p1_rook']]
    ), )
    base_piece_map = load_set.get_piece_map("base_set")
    result = load_set.get_board("base_set", base_piece_map)
    assert result == base_set_board
