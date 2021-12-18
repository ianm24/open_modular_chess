import unittest
import open_modular_chess_core
from open_modular_chess_core import load_set

#TODO Add tests for each error code
class TestGetPieceNames(unittest.TestCase):
    def test_names(self):
        #Test it gets names properly
        base_set_names = ['bishop','king','knight','pawn','queen','rook']
        self.assertEqual(load_set.get_piece_names("base_set"),[base_set_names,None])

#TODO Add tests for each error code for getting and validating boards
# class TestGetBoard(unittest.TestCase):
#     def test_board(self):
#         #TODO
    
#     def test_validate_board(self):
#         #TODO