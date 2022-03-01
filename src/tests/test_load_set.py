from distutils.log import error
import unittest
import open_modular_chess_core
from open_modular_chess_core import load_set

#TODO Add tests for each error code
class TestGetPieceNames(unittest.TestCase):
    def test_missing_pieces_directory(self):
        #Ensures proper function when a set does not contain a pieces directory
        self.assertEqual(load_set.get_piece_names("test_sets/test_set_missing_pieces_directory"),[[],(1,2,1)])

    def test_empty_pieces_directory(self):
        #Ensures proper function when a set has an empty pieces directory
        self.assertEqual(load_set.get_piece_names("test_sets/test_set_empty_pieces_directory"),[[],(1,2,2)])

    def test_get_piece_names(self):
        #Ensures the correct piece names are gotten for a set
        base_set_names = ['bishop','king','knight','pawn','queen','rook']
        self.assertEqual(load_set.get_piece_names("base_set"),[base_set_names,None])

#TODO Add tests for each error code for getting
class TestGetBoard(unittest.TestCase):
    def test_missing_board_file(self):
        #Ensures proper function when a set does not contain a board file
        self.assertEqual(load_set.get_board("test_sets/test_set_missing_board_file"),[[],(1,3,1)])
    
    def test_board_unicode_decode_error(self):
        #Ensures proper function when a set contains a board that is an invalid csv-type file
        self.assertEqual(load_set.get_board("test_sets/test_set_board_unicode_decode_error"),[[],(1,3,2)])

    def test_empty_board_file(self):
        #Ensures proper function when a set has an empty board file
        self.assertEqual(load_set.get_board("test_sets/test_set_empty_board_file"),[[],(1,3,3)])

    def test_board_row_dimension_type(self):
        #Ensures proper function when a set has a board with non-integer row dimension
        self.assertEqual(load_set.get_board("test_sets/test_set_board_row_dimension_type"),[[],(1,3,4)])
    
    def test_board_column_dimension_type(self):
        #Ensures proper function when a set has a board with non-integer column dimension
        self.assertEqual(load_set.get_board("test_sets/test_set_board_column_dimension_type"),[[],(1,3,5)])
    
    def test_invalid_board(self):
        #Ensures proper function when a set has a board with non-integer column dimension
        errorcodes = load_set.get_board("test_sets/test_set_invalid_board");
        get_board_errorcode = (errorcodes[1][0],errorcodes[1][1],errorcodes[1][2])
        self.assertEqual(get_board_errorcode,(1,3,6))
    
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


#TODO Add tests for each error code for validating boards
# class TestValidateBoard(unittest.TestCase):
#     def test_validate_board(self):
#         #TODO