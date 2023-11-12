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

    def list_moves(self) -> list[tuple[int, ...]]:
        """
        Gives a list of all available moves for the piece.

        :return: List of moves currently able to be performed by
            the piece.
        :rtype: list[tuple[int, ...]]
        """
        moves = super().list_moves()

        opposing_player_controller = (self.player_controller % 2) + 1

        illegal_moves = self._board.get_player(
            opposing_player_controller).threatened_spaces

        valid_moves = []
        for move in moves:
            if move not in illegal_moves:
                valid_moves.append(move)

        return valid_moves
