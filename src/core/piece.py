# Code by Chandler McDowell 2023

class Piece:
    """Defines the base class for a piece."""

    def __init__(self, piece_char: str, piece_pxl_hex: str, current_coords: tuple):
        """
        Constructor for a piece.

        Parameters:
            piece_char - String
                1 character string that represent the piece in the command line display
            piece_pxl_hex - String
        """
