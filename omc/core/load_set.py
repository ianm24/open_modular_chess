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
from typing import cast

import numpy as np

from omc.core.exception.exception import BoardNotFoundException
from omc.core.exception.exception import ConditionNotFoundException
from omc.core.exception.exception import EmptyBoardException
from omc.core.exception.exception import InvalidBoardDimensionException
from omc.core.exception.exception import InvalidBoardFormatException
from omc.core.exception.exception import InvalidBoardLayoutException
from omc.core.exception.exception import PiecesEmptyException
from omc.core.exception.exception import PiecesNotFoundException
from omc.core.exception.exception import PlayerClassInvalidException
from omc.core.exception.exception import PlayerNotFoundException
from omc.core.exception.exception import SetNotFoundException
from omc.core.model.board import Board
from omc.core.model.board import Piece
from omc.core.model.board import PieceClass
from omc.core.model.condition import Condition

''' File path to 'sets' directory '''
SETS_DIR = dirname(abspath(__file__)) + '/../../resources/sets/'

''' File path to 'pieces' directory inside of a set's directory '''
SET_PIECES_DIR = '/pieces'

''' File path to 'scripts' directory inside of a set's directory '''
SET_SCRIPTS_DIR = '/scripts'

''' File path to 'conditions' directory inside of a set's directory '''
SET_CONDITIONS_DIR = '/conditions'

''' Standard name for the board file in a set '''
BOARD_FILE_NAME = '/board.csv'

'''Standard ending for the player file in a set'''
PLAYER_FILE_ENDING = '_player.py'

''' Standard name for the win condition file in a set '''
WIN_FILE_NAME = 'win.py'

''' Standard name for the lose condition file in a set '''
LOSE_FILE_NAME = 'lose.py'

''' Number of values that should be in a board file '''
NUM_BOARD_VALS = 3


def load_set(
        set_name: str
) -> tuple[dict[str, PieceClass], Board, Condition, Condition]:
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
    win: Condition = get_win_condition(set_name)
    lose: Condition = get_lose_condition(set_name)

    return piece_map, board, win, lose


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

    :param piece_map: Map of piece names to classes
    :type piece_map: dict[str, PieceClass]
    :param set_name: The selected set's folder name inside the 'sets' directory
    :type set_name: str
    :return: The loaded board
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
    # Load the set's player class dynamically
    set_path = SETS_DIR + set_name
    player_class = None
    try:
        for file_name in listdir(set_path):
            if (file_name.endswith('_player.py')):
                player_name = file_name.partition('.py')[0]
                player_class_name = player_name.title().replace('_', '')
                loader = importlib.machinery.SourceFileLoader(
                    player_class_name, set_path + '/' + file_name
                )
                player_class = getattr(loader.load_module(), player_class_name)
    except AttributeError:
        raise PlayerClassInvalidException(
            f"\nError: The set {set_name} has a player class"
            f"with an invalid name convention. Player file '{file_name}'"
            f" should have class name '{player_class_name}'."
        )

    if player_class is None:
        raise PlayerNotFoundException(
            f"\nError: The set {set_name} does not contain a "
            f"file ending in '{PLAYER_FILE_ENDING}'."
        )

    players = {pn: player_class(pn) for pn in player_numbers}

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
    for index, piece_name in np.ndenumerate(piece_name_layout):
        coord = Board.index_to_coord(index)
        layout[index] = piece_map_func(piece_name, coord)

    # assign pieces -> players and pieces -> board
    for piece in layout.flatten():
        if piece is None:
            continue
        piece_owner = piece.player_controller
        players[piece_owner].add_piece(piece)
        board.add_piece(piece)

    print(f'\nSuccessfully loaded board from set {set_name}')
    return board


def load_condition(set_name: str, file_name: str) -> Condition:
    """
    Loads a condition for a set

    :param set_name: The selected set's folder name inside the 'sets' directory
    :type set_name: str
    :param file_name: The condition's file name inside the set folder
    :type file_name: str
    :return: The loaded condition
    :rtype: Condition
    """
    # Gets file_path for pieces
    dir_path = SETS_DIR + set_name + SET_CONDITIONS_DIR

    if not isdir(dir_path):
        raise ConditionNotFoundException(
            f"\nError: The set {set_name} does not contain a 'conditions'"
            f" directory."
        )
    condition_name = file_name.partition('.py')[0]
    condition_class_name = condition_name.title().replace('_', '')
    loader = importlib.machinery.SourceFileLoader(
        condition_class_name, dir_path + '/' + file_name
    )
    condition_class = getattr(loader.load_module(), condition_class_name)
    return cast(Condition, condition_class())


def get_win_condition(set_name: str) -> Condition:
    """
    Loads a win condition for a set

    :param set_name: The selected set's folder name inside the 'sets' directory
    :type set_name: str
    :return: The loaded win condition
    :rtype: Condition
    """
    return load_condition(set_name, WIN_FILE_NAME)


def get_lose_condition(set_name: str) -> Condition:
    """
    Loads a lose condition for a set

    :param set_name: The selected set's folder name inside the 'sets' directory
    :type set_name: str
    :return: The loaded lose condition
    :rtype: Condition
    """
    return load_condition(set_name, LOSE_FILE_NAME)
