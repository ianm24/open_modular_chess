import numpy as np

from resources.sets.base_set.helper.chess_piece import ChessPiece


class Rook(ChessPiece):
    """Object representing a rook piece."""

    DEFAULT_PIECE_CHAR: str = 'R'
    DEFAULT_PIECE_PIXEL_HEX: int = 0x005A5A3C3C3C3C7E
    DIRECTIONS = (
        np.array([1, 0]),
        np.array([-1, 0]),
        np.array([0, -1]),
        np.array([0, 1]),
    )
    MULTI_STEP = True
