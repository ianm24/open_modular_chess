# Code by Chandler McDowell 2023
import ast
import csv
import importlib
from os import listdir
from os.path import abspath
from os.path import dirname
from os.path import exists
from os.path import isdir
from os.path import isfile
from os.path import join
from typing import Callable

import numpy as np

from omc.core.exception.exception import BoardNotFoundException
from omc.core.exception.exception import EmptyBoardException
from omc.core.exception.exception import InvalidBoardDimensionException
from omc.core.exception.exception import InvalidBoardFormatException
from omc.core.exception.exception import InvalidBoardLayoutException
from omc.core.exception.exception import PiecesEmptyException
from omc.core.exception.exception import PiecesNotFoundException
from omc.core.exception.exception import SetNotFoundException
from omc.core.model.board import Board
from omc.core.model.board import Piece
from omc.core.model.board import Player

''' File path to 'sets' directory '''
SETS_DIR = dirname(abspath(__file__)) + '/../../resources/sets/'

''' File path to 'pieces' directory inside of a set's directory '''
SET_PIECES_DIR = '/pieces'

''' File path to 'scripts' directory inside of a set's directory '''
SET_SCRIPTS_DIR = '/scripts'

''' Standard name for the board file in a set '''
BOARD_FILE_NAME = '/board.csv'

''' Number of values that should be in a board file '''
NUM_BOARD_VALS = 3

''' TypeVar representing subclasses of "Piece" '''
PieceClass = Callable[..., Piece]


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
        raise SetNotFoundException(
            f'\nError: The set {set_name} is not in the sets directory.'
        )

    piece_map: dict[str, PieceClass] = get_piece_map(set_name)
    board: Board = get_board(set_name, piece_map)
    # win = get_win(set_name)
    # lose = get_lose(set_name)

    return [board]
    # return [[pieces,board,win,lose], None]


def get_piece_map(set_name: str) -> dict[str, PieceClass]:
    """
    Gets all piece objects in a set

    :param set_name: The selected set's folder name inside the 'sets' directory
    :type set_name: str
    :return: Piece objects in the set
    :rtype: list[Piece]
    """
    # Gets file_path for pieces
    file_path = SETS_DIR + set_name + SET_PIECES_DIR

    if not isdir(file_path):
        raise PiecesNotFoundException(
            f"\nError: The set {set_name} does not contain a 'pieces'"
            f" directory."
        )

    # Load the class dynamically
    pieces: dict[str, PieceClass] = {}
    for file_name in listdir(file_path):
        if (
                not isfile(join(file_path, file_name))
                or not file_name.endswith('.py')
                or file_name == '__init__.py'
        ):
            continue
        piece_name = file_name.partition('.py')[0]
        piece_class_name = piece_name.title().replace('_', '')
        loader = importlib.machinery.SourceFileLoader(
            piece_class_name, file_path + '/' + file_name
        )
        piece_class = getattr(loader.load_module(), piece_class_name)
        pieces[piece_name] = piece_class

    if not pieces:
        raise PiecesEmptyException(
            f'\nError: The pieces directory for set {set_name} appears to be'
            f' empty.'
        )

    return pieces


def get_board(set_name: str, piece_map: dict[str, PieceClass]) -> Board:
    """
    Gets the board information for a set

    :param piece_map:
    :type piece_map: dict[str, PieceClass]
    :param set_name: The selected set's folder name inside the 'sets' directory
    :type set_name: str
    :return: board - The loaded board
    :rtype: Board
    """

    # Initializes empty board and establishes file_path to set's board file
    file_path = SETS_DIR + set_name + BOARD_FILE_NAME

    print(file_path)

    if not exists(file_path):
        raise BoardNotFoundException(
            f"\nError: The set {set_name} does not contain a "
            f"'{BOARD_FILE_NAME}' file."
        )

    # Tries to load the set's board file
    raw_rows = ''
    raw_columns = ''
    raw_layout = ''
    try:
        with open(file_path) as csv_file:
            reader = csv.reader(csv_file, delimiter='|')
            for row in reader:  # Only 1 row
                if len(row) != 3:
                    raise InvalidBoardFormatException(
                        f'Error: The file {file_path} for set {set_name} has'
                        f' malformed row {row}.'
                    )
                raw_rows = row[0]
                raw_columns = row[1]
                raw_layout = row[2]
    except UnicodeDecodeError:
        raise InvalidBoardLayoutException(
            f'\nError: The file {file_path} for set {set_name} is not a'
            f' properly formatted csv file.'
        )

    if len(raw_layout) == 0:
        raise EmptyBoardException(
            f'\nError: The file {file_path} for set {set_name} appears to be'
            f' empty.'
        )

    # Tries to get integer dimension
    try:
        rows = int(raw_rows)
    except ValueError:
        raise InvalidBoardDimensionException(
            f'\nError: Unable to parse board row dimension in set'
            f' {set_name}. The dimension should be of type {int}. This'
            f' row dimension is {raw_rows}.'
        )

    # Tries to get integer dimension
    try:
        columns = int(raw_columns)
    except ValueError:
        raise InvalidBoardDimensionException(
            f'\nError: Unable to parse board column dimension in set'
            f' {set_name}. The dimension should be of type {int}. This'
            f' column dimension is {raw_columns}.'
        )

    # Converts from string to list
    try:
        # TODO fix this nasty nasty danger code
        piece_name_layout: list = ast.literal_eval(raw_layout)
    except ValueError:
        raise InvalidBoardLayoutException(
            f'\nError: Board layout in set {set_name} contains an invalid'
            f' value type. Ensure that all strings have quotes around them.'
        )

    def get_player_number_from_raw_piece_name(raw_piece_name: str) -> int:
        return int(raw_piece_name.partition('_')[0].lstrip('p'))

    player_numbers = {
        get_player_number_from_raw_piece_name(x)
        for x in np.array(piece_name_layout).flatten()
        if x
    }

    # inst empty board
    board = Board.empty(0, (columns, rows))

    # inst players
    players = {pn: Player(pn) for pn in player_numbers}

    # assign players -> board
    for player in players.values():
        board.add_player(player)

    # inst pieces
    def piece_map_func(raw_piece_name, coord):
        # converts raw piece name to the initial controlling player number
        # p2_pawn -> ('p2', '_', 'pawn') -> 'p2' -> '2' -> 2
        if raw_piece_name == '':
            return None
        player_number = get_player_number_from_raw_piece_name(raw_piece_name)
        piece_name = raw_piece_name.partition('_')[2]
        piece_class = piece_map.get(piece_name)
        if piece_class:
            return piece_class(
                board, current_coords=coord, player_controller=player_number
            )
        return None

    layout = np.empty(np.array([columns, rows]), dtype=Piece)
    for coord, piece_name in np.ndenumerate(piece_name_layout):
        layout[coord] = piece_map_func(piece_name, coord)

    # assign pieces -> players and pieces -> board
    for piece in layout.flatten():
        if piece is None:
            continue
        piece_owner = piece.player_controller
        players[piece_owner].add_piece(piece)
        board.add_piece(piece)

    print(f'\nSuccessfully loaded board from set {set_name}')
    return board
