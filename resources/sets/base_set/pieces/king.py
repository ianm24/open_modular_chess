import numpy as np

from resources.sets.base_set.helper.chess_piece import ChessPiece


class King(ChessPiece):
    """Object representing a king piece."""

    DEFAULT_PIECE_CHAR: str = 'K'
    DEFAULT_PIECE_PIXEL_HEX: int = 0x183C187E7E3C3C7E
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
