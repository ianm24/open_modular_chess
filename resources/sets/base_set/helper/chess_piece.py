from typing import Iterable

from omc.core.model.board import Piece


class ChessPiece(Piece):
    """Object representing a chess piece."""

    # Whether or not a piece can move more than one unit in a given direction
    MULTI_STEP: bool = False

    # Each direction to consider for valid moves
    DIRECTIONS: Iterable[tuple[int, ...]] = tuple()

    def list_moves(self) -> list[tuple[int, ...]]:
        """
        Gives a list of all available moves for the piece.

        :return: List of moves currently able to be performed by
            the piece.
        :rtype: list[tuple[int, ...]]
        """

        moves = []

        # Consider all valid directions
        for direction in self.DIRECTIONS:
            try_move = (
                self._current_coords[0] + direction[0],
                self._current_coords[1] + direction[1]
            )
            while self._board.on_board(try_move):
                try_query = self._board.query_space(try_move)
                # Consider open spaces
                if try_query is None:
                    moves.append(try_move)
                # Consider captures
                elif try_query.player_controller != self.player_controller:
                    moves.append(try_move)
                    break

                # Consider multiple steps in same direction if able
                if not self.MULTI_STEP:
                    break

                try_move += direction

        return moves
