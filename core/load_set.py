# Code by Ian McDowell 2021
import csv

SETS_DIR = "../sets/"
""" File path to 'sets' directory """
SET_PIECES_DIR = "/pieces"
""" File path to 'pieces' directory inside of a set's directory """
SET_SCRIPTS_DIR = "/scripts"
""" File path to 'scripts' directory inside of a set's directory """

BOARD_FILE_NAME = "/board.csv"
""" Standard name for the board file in a set """

NUM_BOARD_VALS = 3
""" Number of values that should be in a board file """

def get_board(set_name):
    """
    Gets the board information for a set

    Inputs:
        set_name - String
            The selected set's folder name inside the 'sets' directory
    Outputs:
        board - List [int num_rows, int num_cols, num_rows x num_cols String List]
            Contains dimensions and piece placement of board
    """
    
    board = []
    filepath = SETS_DIR + set_name + BOARD_FILE_NAME
    try:
        file = open(filepath, mode = 'r')
        board = [file.read()]
    except IOError:
        print(f"Error: The file {filepath} for set {set_name} couldn't be loaded.")

    if validate_board(board,set_name):
        print(f"Successfully loaded board from set {set_name}")
        return board
    else:
        return []


def validate_board(board,set_name):
    """
    Validates that a loaded board fits specifications

    Inputs:
        board - List
            The board as read by the set's file put into a list
        set_name - String
            The selected set's folder name inside the 'sets' directory
    Outputs:
        isValid - boolean
            Whether or not the board fits specifications
    """
    #Set filepath from set name
    filepath = SETS_DIR + set_name + BOARD_FILE_NAME

    #Non-empty file check
    if board == ['']:
        print(f"Error: The file {filepath} in set {set_name} appears to be empty.")
        return False
    
    #Correct amount of board values check
    if len(board) != NUM_BOARD_VALS:
        print(f"Error: Invalid board format in set {set_name}. ",
             f"There are {len(board)} arguments when there should be {NUM_BOARD_VALS}")
        return False

    #Get values from board
    num_rows = board[0]
    num_cols = board[1]
    board_layout = board[2]

    #Valid board dimension data type check
    if not (isinstance(num_rows,int) and isinstance(num_cols,int)):
        print(f"Error: Invalid board dimension type in set {set_name}. ",
            f"The dimensions should be of type {type(int)}. This set's "
            f"dimensions are of type ({type(num_rows)},{type(num_cols)}).")
        return False

    #Valid board dimensions check
    if board[0] < 1 or board[1] < 1:
        print(f"Error: Invalid board dimensions in set {set_name}. ",
            f"The dimensions (# of rows, # of cols) must be positive. This set's ",
            f"dimensions are ({num_rows},{num_cols}).")
        return False


    #Board layout matches dimensions check
    #Check rows
    if len(board_layout) != num_rows:
        print(f"Error: Invalid board layout in set {set_name}.",
            f"The number of rows in the layout is {len(board_layout)} and does not ",
            f"match the board dimension specified {num_rows}.")
        return False
    for i in range(len(board_layout)):
        #Check columns
        if len(board_layout[i]) != num_cols:
            print(f"Error: Invalid board layout in set {set_name}.",
                f"The number of columns in row {i+1} of the layout is {len(board_layout)} ",
                f"and does not match the board dimension specified {num_cols}.")
            return False
        for j in range(len(board_layout[i])):
            #Check type
            if not isinstance(j,str):
                print(f"Error: Invalid board layout type in set {set_name}.",
                    f"The entry in row {i+1} and column {j+1} of the layout is ",
                    f"{board_layout[i][j]} and of type {type(board_layout[i][j])} but should be a string.")
                return False
            #TODO only p1, p2, blank, and pieces that are in pieces directory