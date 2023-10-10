from distutils.log import error
from os import remove
from os.path import exists
import unittest

import open_modular_chess_core
from open_modular_chess_core import load_set

#Load script and method error codes
SEC = load_set.SCRIPT_ERROR_CODE
lsMEC = 1 #LoadSet
gpnMEC = 2 #GetPieceNames
gbMEC = 3 #GetBoard
vbMEC = 4 #ValidateBoard

#Load ensure commit file title
EC = "ensure_commit.txt"

class TestLoadSet(unittest.TestCase):
    def test_incorrect_set_name(self):
        #Ensures proper function when a set name is incorrect
        self.assertEqual(load_set.load_set("test_sets/test_set_incorrect_set_name"),[[],(SEC,lsMEC,1)])

class TestGetPieceNames(unittest.TestCase):
    def test_missing_pieces_directory(self):
        #Ensures proper function when a set does not contain a pieces directory
        self.assertEqual(load_set.get_piece_names("test_sets/test_set_missing_pieces_directory"),[[],(SEC,gpnMEC,1)])

    def test_empty_pieces_directory(self):
        #Ensures proper function when a set has an empty pieces directory

        #Remove the ensure commit file to create empty directory
        set_dir = "test_sets/test_set_empty_pieces_directory/"
        
        if exists("../sets/"+set_dir+"pieces/"+EC):
            remove("../sets/"+set_dir+"pieces/"+EC)
            self.assertEqual(1,1)
        
        #Get result for the test
        result = load_set.get_piece_names(set_dir)

        #Recreate the ensure commit file
        file = open("../sets/"+set_dir+"pieces/"+EC,"x")
        file.close()

        #Run the test
        self.assertEqual(result,[[],(SEC,gpnMEC,2)])

    def test_get_piece_names(self):
        #Ensures the correct piece names are gotten for a set
        base_set_names = ['bishop','king','knight','pawn','queen','rook']
        self.assertEqual(load_set.get_piece_names("base_set"),[base_set_names,None])

class TestGetBoard(unittest.TestCase):
    def test_missing_board_file(self):
        #Ensures proper function when a set does not contain a board file
        self.assertEqual(load_set.get_board("test_sets/test_set_missing_board_file"),[[],(SEC,gbMEC,1)])
    
    def test_board_unicode_decode_error(self):
        #Ensures proper function when a set contains a board that is an invalid csv-type file
        self.assertEqual(load_set.get_board("test_sets/test_set_board_unicode_decode_error"),[[],(SEC,gbMEC,2)])

    def test_empty_board_file(self):
        #Ensures proper function when a set has an empty board file
        self.assertEqual(load_set.get_board("test_sets/test_set_empty_board_file"),[[],(SEC,gbMEC,3)])

    def test_board_row_dimension_type(self):
        #Ensures proper function when a set has a board with non-integer row dimension
        self.assertEqual(load_set.get_board("test_sets/test_set_board_row_dimension_type"),[[],(SEC,gbMEC,4)])
    
    def test_board_column_dimension_type(self):
        #Ensures proper function when a set has a board with non-integer column dimension
        self.assertEqual(load_set.get_board("test_sets/test_set_board_column_dimension_type"),[[],(SEC,gbMEC,5)])

    def test_invalid_board_layout_value(self):
        #Ensures proper function when a set has a board with an invalid value type in board layout
        self.assertEqual(load_set.get_board("test_sets/test_set_invalid_board_layout_value"),[[],(SEC,gbMEC,6)])
    
    def test_invalid_board(self):
        #Ensures proper function when a set has a board with non-integer column dimension
        errorcodes = load_set.get_board("test_sets/test_set_extra_values_board")
        get_board_errorcode = (errorcodes[1][0],errorcodes[1][1],errorcodes[1][2])
        self.assertEqual(get_board_errorcode,(SEC,gbMEC,7))
    
    def test_get_board(self):
        #Ensures the correct board is gotten for a set
        base_set_board = [8, 8, [
                ['p2_rook', 'p2_knight', 'p2_bishop', 'p2_king', 'p2_queen', 'p2_bishop', 'p2_knight', 'p2_rook'],
                ['p2_pawn', 'p2_pawn', 'p2_pawn', 'p2_pawn', 'p2_pawn', 'p2_pawn', 'p2_pawn', 'p2_pawn'],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '','', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['p1_pawn', 'p1_pawn', 'p1_pawn', 'p1_pawn','p1_pawn', 'p1_pawn', 'p1_pawn', 'p1_pawn'],
                ['p1_rook', 'p1_knight', 'p1_bishop', 'p1_king', 'p1_queen', 'p1_bishop', 'p1_knight', 'p1_rook']]]
        self.assertEqual(load_set.get_board("base_set"),base_set_board)

class TestValidateBoard(unittest.TestCase):
    def test_extra_values_board(self):
        #Ensures proper function when a set has a board with extra values
        self.assertEqual(load_set.get_board("test_sets/test_set_extra_values_board"),[[],(SEC,gbMEC,7,(SEC,vbMEC,1))])
    
    def test_nonpos_board_dimension(self):
        #Ensures proper function when a set has a board with non-positive dimensions
        self.assertEqual(load_set.get_board("test_sets/test_set_nonpos_board_dimension_1"),[[],(SEC,gbMEC,7,(SEC,vbMEC,2))])
        self.assertEqual(load_set.get_board("test_sets/test_set_nonpos_board_dimension_2"),[[],(SEC,gbMEC,7,(SEC,vbMEC,2))])
    
    def test_board_layout_num_rows(self):
        #Ensures proper function when a set has a board with a number of rows different that what is stated previously in the board file
        self.assertEqual(load_set.get_board("test_sets/test_set_board_layout_num_rows"),[[],(SEC,gbMEC,7,(SEC,vbMEC,3))])

    def test_board_layout_num_cols(self):
        #Ensures proper function when a set has a board with a number of cols different that what is stated previously in the board file
        self.assertEqual(load_set.get_board("test_sets/test_set_board_layout_num_cols"),[[],(SEC,gbMEC,7,(SEC,vbMEC,4))])
    
    def test_nonstring_board_piece(self):
        #Ensures proper function when a set has a board has a non-string value in the board layout
        self.assertEqual(load_set.get_board("test_sets/test_set_nonstring_board_piece"),[[],(SEC,gbMEC,7,(SEC,vbMEC,5))])

    def test_invalid_player_prefix_board_piece(self):
        #Ensures proper function when a set has a board has an invalid player prefix for a board piece
        self.assertEqual(load_set.get_board("test_sets/test_set_invalid_player_prefix_board_piece"),[[],(SEC,gbMEC,7,(SEC,vbMEC,6))])

    def test_invalid_player_suffix_board_piece(self):
        #Ensures proper function when a set has a board has an invalid player suffix for a board piece
        self.assertEqual(load_set.get_board("test_sets/test_set_invalid_player_suffix_board_piece"),[[],(SEC,gbMEC,7,(SEC,vbMEC,7))])
    
    def test_validate_board(self):
        #Ensures a valid board is validated
        base_set_board = [8, 8, [
                ['p2_rook', 'p2_knight', 'p2_bishop', 'p2_king', 'p2_queen', 'p2_bishop', 'p2_knight', 'p2_rook'],
                ['p2_pawn', 'p2_pawn', 'p2_pawn', 'p2_pawn', 'p2_pawn', 'p2_pawn', 'p2_pawn', 'p2_pawn'],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '','', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['p1_pawn', 'p1_pawn', 'p1_pawn', 'p1_pawn','p1_pawn', 'p1_pawn', 'p1_pawn', 'p1_pawn'],
                ['p1_rook', 'p1_knight', 'p1_bishop', 'p1_king', 'p1_queen', 'p1_bishop', 'p1_knight', 'p1_rook']]]
        self.assertEqual(load_set.validate_board(base_set_board,"base_set"),[True,None])