from resources.sets.base_set.helper.chess_piece import ChessPiece


class Knight(ChessPiece):
    """Object representing a knight piece."""

    DEFAULT_PIECE_CHAR: str = 'N'
    DEFAULT_PIECE_PIXEL_HEX: int = 0x1C3E70783C3C3C7E
    DIRECTIONS = (
        (2, 1),
        (1, 2),
        (-1, 2),
        (-2, 1),
        (-2, -1),
        (-1, -2),
        (1, -2),
        (2, -1),
    )
