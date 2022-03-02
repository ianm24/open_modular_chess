# Code by Ian McDowell 2021
import ast, csv, re
from os import listdir
from os.path import isdir, isfile, join, exists

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

SCRIPT_ERROR_CODE = 1
"""Number to indicate which script the error is from """

def load_set(set_name):
    """
    Loads a set

    Inputs:
        set_name - String
            The selected set's folder name inside the 'sets' directory
    Outputs:
        loaded_set - list [???]
            Contains all parts of the loaded set
        errorcodes - Tuple (int script_error_code, int method_error_code, int check_error_code, Tuple prev_errors)
            The error codes is there were any
    """
    #Sets the error code for the current method
    METHOD_ERROR_CODE = 1

    filepath = SETS_DIR + set_name

    if not isdir(filepath):
        print(f"\nError: The set {set_name} is not in the sets directory.")
        return [[],(SCRIPT_ERROR_CODE,METHOD_ERROR_CODE,1)]

    #pieces = get_pieces(set_name)
    #board = get_board(set_name)
    #win = get_win(set_name)
    #lose = get_lose(set_name)

    #return [pieces,board,win,lose]


def get_piece_names(set_name):
    """
    Gets the name of all pieces in a set

    Inputs:
        set_name - String
            The selected set's folder name inside the 'sets' directory
    Outputs:
        piece_names - list [string,*]
            Contains the names of every piece in the set
        errorcodes - Tuple (int script_error_code, int method_error_code, int check_error_code, Tuple prev_errors)
            The error codes is there were any
    """
    #Sets the error code for the current method
    METHOD_ERROR_CODE = 2

    #Gets filepath for pieces
    filepath = SETS_DIR + set_name + SET_PIECES_DIR

    if not isdir(filepath):
        print(f"\nError: The set {set_name} does not contain a 'pieces' directory.")
        return [[],(SCRIPT_ERROR_CODE,METHOD_ERROR_CODE,1)]

    pieces = [file.replace(".csv","") for file in listdir(filepath) if isfile(join(filepath,file))]
    
    if pieces == []:
        print(f"\nError: The pieces directory for set {set_name} appears to be empty.")
        return [[],(SCRIPT_ERROR_CODE,METHOD_ERROR_CODE,2)]

    #Sort in alphabetical order
    pieces.sort()

    return [pieces,None]

def get_board(set_name): #TODO add tests for each error code
    """
    Gets the board information for a set

    Inputs:
        set_name - String
            The selected set's folder name inside the 'sets' directory
    Outputs:
        board - List [int num_rows, int num_cols, num_rows x num_cols String List]
            Contains dimensions and piece placement of board
        errorcodes - Tuple (int script_error_code, int method_error_code, int check_error_code, Tuple prev_errors)
            The error codes is there were any 
    """
    #Sets the error code for the current method
    METHOD_ERROR_CODE = 3
    
    #Initializes empty board and establishes filepath to set's board file
    board = []
    filepath = SETS_DIR + set_name + BOARD_FILE_NAME
    
    if not exists(filepath):
        print(f"\nError: The set {set_name} does not contain a '{BOARD_FILE_NAME}' file.")
        return [[],(SCRIPT_ERROR_CODE,METHOD_ERROR_CODE,1)]

    #Tries to load the set's board file
    try:
        with open(filepath) as csvfile:
            reader = csv.reader(csvfile,delimiter="|")
            for row in reader: #Only 1 row
                board = row
    except UnicodeDecodeError:
        print(f"\nError: The file {filepath} for set {set_name} is not a properly formatted csv file.")
        return [[],(SCRIPT_ERROR_CODE,METHOD_ERROR_CODE,2)]
    
    if len(board) == 0:
        print(f"\nError: The file {filepath} for set {set_name} appears to be empty.")
        return [[],(SCRIPT_ERROR_CODE,METHOD_ERROR_CODE,3)]


    #Tries to get integer dimension
    try:
        board[0] = int(board[0])
    except ValueError:
        print(f"\nError: Invalid board dimension type in set {set_name}. ",
            f"The dimensions should be of type {int}. This set's "
            f"row dimension is of type {type(board[0])}.")
        return [[],(SCRIPT_ERROR_CODE,METHOD_ERROR_CODE,4)]
    
    #Tries to get integer dimension
    try:
        board[1] = int(board[1])
    except ValueError:
        print(f"\nError: Invalid board dimension type in set {set_name}. ",
            f"The dimensions should be of type {int}. This set's "
            f"column dimension is of type {type(board[1])}.")
        return [[],(SCRIPT_ERROR_CODE,METHOD_ERROR_CODE,5)]
    
    #Converts from string to list
    try:
        board[2] = ast.literal_eval(board[2])
    except ValueError:
        print(f"\nError: Board layout in set {set_name} contains an invalid value type",
            f"Ensure that all strings have quotes around them.")
        return [[],(SCRIPT_ERROR_CODE,METHOD_ERROR_CODE,6)]

    #Tries to validate board and returns it if successful
    [valid,errorcodes] = validate_board(board,set_name)
    if valid:
        print(f"\nSuccessfully loaded board from set {set_name}")
        return board
    else:
        print(f"\nError: Board from set {set_name} failed to validate.")
        return [[],(SCRIPT_ERROR_CODE,METHOD_ERROR_CODE,7,errorcodes)]


def validate_board(board,set_name): #TODO add tests for each error code
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
        errorcodes - Tuple (int script_error_code, int method_error_code, int check_error_code, Tuple prev_errors)
            The error codes is there were any
    """
    #Sets the error code for the current method
    METHOD_ERROR_CODE = 4

    #Set filepath from set name
    filepath = SETS_DIR + set_name + BOARD_FILE_NAME
    
    #Correct amount of board values check
    if len(board) != NUM_BOARD_VALS:
        print(f"\nError: Invalid board format in set {set_name}. ",
             f"There are {len(board)} arguments when there should be {NUM_BOARD_VALS}")
        return [False,(SCRIPT_ERROR_CODE,METHOD_ERROR_CODE,1)]

    #Get values from board
    num_rows = board[0]
    num_cols = board[1]
    board_layout = board[2]

    #Valid board dimensions check
    if board[0] < 1 or board[1] < 1:
        print(f"\nError: Invalid board dimensions in set {set_name}. ",
            f"The dimensions (# of rows, # of cols) must be positive. This set's ",
            f"dimensions are ({num_rows},{num_cols}).")
        return [False,(SCRIPT_ERROR_CODE,METHOD_ERROR_CODE,2)]


    #Board layout matches dimensions check
    #Check rows
    if len(board_layout) != num_rows:
        print(f"\nError: Invalid board layout in set {set_name}. ",
            f"The number of rows in the layout is {len(board_layout)} and does not ",
            f"match the board dimension specified {num_rows}.")
        return [False,(SCRIPT_ERROR_CODE,METHOD_ERROR_CODE,3)]

    for i in range(len(board_layout)):
        curr_row = board_layout[i]
        #Check columns
        if len(curr_row) != num_cols:
            print(f"\nError: Invalid board layout in set {set_name}. ",
                f"The number of columns in row {i+1} of the layout is {len(curr_row)} ",
                f"and does not match the board dimension specified {num_cols}.")
            return [False,(SCRIPT_ERROR_CODE,METHOD_ERROR_CODE,4)]

        for j in range(len(curr_row)):
            curr_cell = curr_row[j]
            #Check type
            if not isinstance(curr_cell,str):
                print(f"\nError: Invalid type for piece on board in set {set_name}. ",
                    f"The entry in row {i+1} and column {j+1} of the layout is ",
                    f"{curr_cell} and of type {type(curr_cell)} but should be a string.")
                return [False,(SCRIPT_ERROR_CODE,METHOD_ERROR_CODE,5)]
            
            #Check it is a valid piece
            if curr_cell != "":
                #Check for player prefix
                player_prefix = re.search("p[0-9]+",curr_cell)
                if not player_prefix:
                    print(f"\nError: Invalid player prefix for piece on board in set {set_name}. ",
                        f"The non-blank entry in row {i+1} and column {j+1} of the layout is ",
                        f"{curr_cell} and does not have a player prefix. ",
                        f"Non-player pieces should have the prefix \'p0\'")
                    return [False,(SCRIPT_ERROR_CODE,METHOD_ERROR_CODE,6)]

                #Check for valid piece suffix
                piece_names = get_piece_names(set_name)[0]
                has_piece_suffix = False
                for name in piece_names:
                    piece = re.search(name,curr_cell)
                    if piece:
                        if len(curr_cell.replace(player_prefix[0]+"_","")) != len(name): #Check the name isn't a substring of the actual piece
                            continue
                        else:
                            has_piece_suffix = True
                
                if not has_piece_suffix:
                    print(f"\nError: Invalid name for piece on board in set {set_name}. ",
                        f"The non-blank entry in row {i+1} and column {j+1} of the layout is ",
                        f"{curr_cell} and does not have a piece name specified for the set. ",
                        f"The piece should be one of {piece_names}")
                    return [False,(SCRIPT_ERROR_CODE,METHOD_ERROR_CODE,7)]
    return [True,None]