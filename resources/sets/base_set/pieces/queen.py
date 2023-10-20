from resources.sets.base_set.helper.chess_piece import ChessPiece


class Queen(ChessPiece):
    """Object representing a pawn piece."""

    DEFAULT_PIECE_CHAR: str = 'Q'
    DEFAULT_PIECE_PIXEL_HEX: int = 0x5A24183C183C3C7E
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
    MULTI_STEP: bool = True
