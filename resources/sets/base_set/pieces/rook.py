from typing import Optional

import numpy as np
from numpy import ndarray

from src.core.model.piece import Piece


class Rook(Piece):
    """Object representing a rook piece."""

    __slots__ = ('_piece_char', '_piece_pxl_hex', '_board',
                 '_current_coords', '_player_controller', '_direction')

    _default_piece_char: str = 'R'
    _default_piece_pxl_hex: int = 0x005A5A3C3C3C3C7E  # TODO change
    _directions = {
        np.array([1, 0]),
        np.array([-1, 0]),
        np.array([0, -1]),
        np.array([0, 1]),
    }

    def list_moves(self) -> list[Optional[ndarray[int]]]:
        """
        Gives a list of all available moves for the piece.

        :return: List of moves currently able to be performed by
            the piece.
        :rtype: list[Optional[ndarray[int]]]
        """

        moves = []

        # Consider all 4 directions
        for direction in self._directions:
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
