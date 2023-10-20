from resources.sets.base_set.helper.chess_piece import ChessPiece


class Bishop(ChessPiece):
    """Object representing a bishop piece."""

    DEFAULT_PIECE_CHAR: str = 'B'
    DEFAULT_PIECE_PIXEL_HEX: int = 0x103434183C183C7E
    DIRECTIONS = (
        (1, 1),
        (-1, 1),
        (-1, -1),
        (1, -1),
    )
    MULTI_STEP = True
