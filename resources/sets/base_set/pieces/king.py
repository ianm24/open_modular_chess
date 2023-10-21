from resources.sets.base_set.helper.chess_piece import ChessPiece


class King(ChessPiece):
    """Object representing a king piece."""

    DEFAULT_PIECE_CHAR: str = 'K'
    DEFAULT_PIECE_PIXEL_HEX: int = 0x183C187E7E3C3C7E
    DIRECTIONS = (
        (1, 0),
        (1, 1),
        (0, 1),
        (-1, 1),
        (-1, 0),
        (-1, -1),
        (0, -1),
        (1, -1),
    )
