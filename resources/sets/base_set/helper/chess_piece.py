from typing import Iterable
from typing import Optional

from numpy import ndarray

from omc.core.model.board import Piece


class ChessPiece(Piece):
    """Object representing a chess piece."""

    # Whether or not a piece can move more than one unit in a given direction
    MULTI_STEP: bool = False

    # Each direction to consider for valid moves
    DIRECTIONS: Iterable[ndarray] = tuple()

    def list_moves(self) -> list[Optional[ndarray[int]]]:
        """
        Gives a list of all available moves for the piece.

        :return: List of moves currently able to be performed by
            the piece.
        :rtype: list[Optional[ndarray[int]]]
        """

        moves = []

        # Consider all valid directions
        for direction in self.DIRECTIONS:
            try_move = self._current_coords + direction
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

    def move(self, coords: ndarray[int]) -> bool:
        """
        Performs an action on the piece using arguments

        :param coords: Coordinates of the attempted move
        :type coords: ndarray[int]
        :return: True on successful move, False otherwise.
        :rtype: bool
        """

        # Check if move is valid
        if coords not in self.list_moves():
            print("Invalid Move.")
            return False

        other_piece = self._board.query_space(coords)

        # Check for capture
        if (
                other_piece is not None
                and other_piece.player_controller != self._player_controller
        ):
            other_piece.capture(self._player_controller)

        self._current_coords = coords
        return True
