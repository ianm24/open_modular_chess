import numpy as np

from resources.sets.base_set.helper.chess_piece import ChessPiece


class Queen(ChessPiece):
    """Object representing a pawn piece."""

    DEFAULT_PIECE_CHAR: str = 'Q'
    DEFAULT_PIECE_PIXEL_HEX: int = 0x5A24183C183C3C7E
    DIRECTIONS = (
        np.array([1, 0]),
        np.array([1, 1]),
        np.array([0, 1]),
        np.array([-1, 1]),
        np.array([-1, 0]),
        np.array([-1, -1]),
        np.array([0, -1]),
        np.array([1, -1]),
    )
    MULTI_STEP: bool = True
