# Code by Chandler McDowell 2023
import ast
import csv
import re
from os import listdir
from os.path import isdir, isfile, join, exists, dirname, abspath
from typing import Any

from core.exception.exception import SetNotFoundException, PiecesNotFoundException, PiecesEmptyException, \
    BoardNotFoundException, EmptyBoardException, InvalidBoardDimensionException, \
    InvalidBoardLayoutException, BoardValidationFailedException, InvalidBoardFormatException
from core.model.board import Board

""" File path to 'sets' directory """
SETS_DIR = dirname(abspath(__file__)) + '/../../resources/sets/'

""" File path to 'pieces' directory inside of a set's directory """
SET_PIECES_DIR = '/pieces'

""" File path to 'scripts' directory inside of a set's directory """
SET_SCRIPTS_DIR = '/scripts'

""" Standard name for the board file in a set """
BOARD_FILE_NAME = '/board.csv'

""" Number of values that should be in a board file """
NUM_BOARD_VALS = 3


def load_set(set_name: str) -> list:
    """
    Loads a set

    :param set_name: The selected set's folder name inside the 'sets' directory
    :type set_name: str
    :return: All parts of the loaded set
    :rtype: list
    """

    # Sets the error code for the current method
    file_path = SETS_DIR + set_name

    if not isdir(file_path):
        raise SetNotFoundException(f'\nError: The set {set_name} is not in the sets directory.')

    return []  # TODO remove

    # pieces = get_pieces(set_name)
    # board = get_board(set_name)
    # win = get_win(set_name)
    # lose = get_lose(set_name)

    # return [[pieces,board,win,lose], None]


def get_piece_names(set_name: str) -> list[str, Any]:
    """
    Gets the name of all pieces in a set

    :param set_name: The selected set's folder name inside the 'sets' directory
    :type set_name: str
    :return: Names of every piece in the set
    :rtype: list
    """

    # Gets file_path for pieces
    file_path = SETS_DIR + set_name + SET_PIECES_DIR

    if not isdir(file_path):
        raise PiecesNotFoundException(f"\nError: The set {set_name} does not contain a 'pieces' directory.")

    pieces = [file.replace('.csv', '') for file in listdir(file_path) if isfile(join(file_path, file))]

    if not pieces:
        raise PiecesEmptyException(f'\nError: The pieces directory for set {set_name} appears to be empty.')

    # Sort in alphabetical order
    pieces.sort()

    return pieces


def get_board(set_name: str) -> Board:
    """
    Gets the board information for a set

    :param set_name: The selected set's folder name inside the 'sets' directory
    :type set_name: str
    :return: board - List [int num_rows, int num_cols, num_rows x num_cols String List]
            Contains dimensions and piece placement of board
    :rtype: list
    """

    # Initializes empty board and establishes file_path to set's board file
    board = Board.empty()
    file_path = SETS_DIR + set_name + BOARD_FILE_NAME

    print(file_path)

    if not exists(file_path):
        raise BoardNotFoundException(f"\nError: The set {set_name} does not contain a '{BOARD_FILE_NAME}' file.")

    # Tries to load the set's board file
    rows, columns, layout = 0, 0, []
    try:
        with open(file_path) as csv_file:
            reader = csv.reader(csv_file, delimiter='|')
            for row in reader:  # Only 1 row
                if len(row) != 3:
                    raise InvalidBoardFormatException(
                        f'Error: The file {file_path} for set {set_name} has malformatted row {row}.'
                    )
                rows, columns, layout = row
    except UnicodeDecodeError:
        raise InvalidBoardLayoutException(
            f'\nError: The file {file_path} for set {set_name} is not a properly formatted csv file.'
        )

    if len(layout) == 0:
        raise EmptyBoardException(f'\nError: The file {file_path} for set {set_name} appears to be empty.')

    # Tries to get integer dimension
    try:
        rows = int(rows)
    except ValueError:
        raise InvalidBoardDimensionException(
            f'\nError: Invalid board dimension type in set {set_name}. '
            f"The dimensions should be of type {int}. This set's "
            f'row dimension is of type {type(board.rows)}.'
        )

    # Tries to get integer dimension
    try:
        columns = int(columns)
    except ValueError:
        raise InvalidBoardDimensionException(
            f'\nError: Invalid board dimension type in set {set_name}. '
            f"The dimensions should be of type {int}. This set's "
            f'column dimension is of type {type(board.columns)}.'
        )

    # Converts from string to list
    try:
        layout = ast.literal_eval(layout)  # TODO fix this nasty nasty danger code
    except ValueError:
        raise InvalidBoardLayoutException(
            f'\nError: Board layout in set {set_name} contains an invalid value type. '
            f'Ensure that all strings have quotes around them.'
        )

    board = Board(rows, columns, layout)

    # Tries to validate board and returns it if successful
    valid = validate_board(board, set_name)
    if valid:
        print(f'\nSuccessfully loaded board from set {set_name}')
        return board
    else:
        raise BoardValidationFailedException(f'\nError: Board from set {set_name} failed to validate.')


def validate_board(board: Board, set_name: str) -> bool:
    """
    Validates that a loaded board fits specifications

    :param board: The board
    :type board: Board
    :param set_name: The selected set's folder name inside the 'sets' directory
    :type set_name: str
    :return: Whether or not the board fits specifications
    :rtype: bool
    """

    board_layout = board.layout
    num_rows = board.rows
    num_cols = board.columns

    # Valid board dimensions check
    if num_rows < 1 or num_cols < 1:
        raise BoardValidationFailedException(
            f'\nError: Invalid board dimensions in set {set_name}. '
            f"The dimensions (# of rows, # of cols) must be positive. This set's "
            f'dimensions are ({num_rows}, {num_cols}).'
        )

    # Board layout matches dimensions check
    # Check rows
    if len(board_layout) != num_rows:
        raise BoardValidationFailedException(
            f'\nError: Invalid board layout in set {set_name}. '
            f'The number of rows in the layout is {len(board_layout)} and does not '
            f'match the board dimension specified {num_rows}.'
        )

    for i in range(len(board_layout)):
        curr_row = board_layout[i]
        # Check columns
        if len(curr_row) != num_cols:
            raise BoardValidationFailedException(
                f'\nError: Invalid board layout in set {set_name}. '
                f'The number of columns in row {i + 1} of the layout is {len(curr_row)} '
                f'and does not match the board dimension specified {num_cols}.'
            )

        for j in range(len(curr_row)):
            curr_cell = curr_row[j]
            if not isinstance(curr_cell, str):
                raise BoardValidationFailedException(
                    f'\nError: Invalid type for piece on board in set {set_name}. '
                    f'The entry in row {i + 1} and column {j + 1} of the layout is '
                    f'{curr_cell} and of type {type(curr_cell)} but should be a string.'
                )

            # Check it is a valid piece
            if curr_cell != '':
                # Check for player prefix
                player_prefix = re.search('p[0-9]+_', curr_cell)
                if not player_prefix:
                    raise BoardValidationFailedException(
                        f'\nError: Invalid player prefix for piece on board in set {set_name}. '
                        f'The non-blank entry in row {i + 1} and column {j + 1} of the layout is '
                        f'{curr_cell} and does not have a player prefix. '
                        f'Non-player pieces should have the prefix \'p0\''
                    )

                # Check for valid piece suffix
                piece_names = get_piece_names(set_name)
                has_piece_suffix = False
                for name in piece_names:
                    piece = re.search(name, curr_cell)
                    if piece:
                        # Check the name isn't a substring of the actual piece
                        if len(curr_cell.replace(player_prefix[0], '')) != len(name):
                            continue
                        else:
                            has_piece_suffix = True

                if not has_piece_suffix:
                    raise BoardValidationFailedException(
                        f'\nError: Invalid name for piece on board in set {set_name}. '
                        f'The non-blank entry in row {i + 1} and column {j + 1} of the layout is '
                        f'{curr_cell} and does not have a piece name specified for the set. '
                        f'The piece should be one of {piece_names}'
                    )
    return True
