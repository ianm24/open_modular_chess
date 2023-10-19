from typing import cast
from typing import Optional

import numpy as np
from numpy import ndarray
from queen import Queen

from src.core.model.board import Board
from src.core.model.piece import Piece


class Pawn(Piece):
    """Object representing a pawn piece."""

    __slots__ = ('_piece_char', '_piece_pxl_hex', '_board',
                 '_current_coords', '_player_controller', '_direction')

    _default_piece_char: str = 'P'
    _default_piece_pxl_hex: int = 0x183C3C1818183C7E

    def __init__(
            self, board: Board,
            piece_char: Optional[str] = None,
            piece_pxl_hex: Optional[int] = None,
            current_coords: Optional[tuple[int, int]] = None,
            player_controller: Optional[int] = None
    ):
        """
        Initialize an instance of Pawn. Calls the superclass constructor, but
            also instantiates the direction in which the Pawn is allowed to
            advance.

        :param board: The board the piece belongs to.
        :type board: Board
        :param piece_char: 1-character string that represent the piece in
            the command line display. Default is set by subclass.
        :type piece_char: Optional[str]
        :param piece_pxl_hex: Hex value of 64-bit number representing an
            8x8 pixel grid to display the piece in a GUI. Default is set
            by subclass.
        :type piece_pxl_hex: Optional[int]
        :param current_coords: Represents the current placement of the
            piece on the board. Default is (0,0).
        :type current_coords: Optional[ndarray[int]]
        :param player_controller: The player controlling this piece.
            Default is 1.
        :type player_controller: Optional[int]
        """
        super().__init__(
            board, piece_char, piece_pxl_hex, current_coords, player_controller
        )
        self._direction = np.array(
            [0, 1] if self._moving_down() else [0, -1]
        )

    def _moving_down(self) -> bool:
        """
        Indicate whether the pawn is moving in the negative y direction.

        :return: Whether the pawn is moving in the negative y direction
        :rtype: bool
        """
        return self._player_controller % 2 == 1

    def list_moves(self) -> list[Optional[ndarray[int]]]:
        """
        Gives a list of all available moves for the piece.

        :return: List of moves currently able to be performed by
            the piece.
        :rtype: list[Optional[ndarray[int]]]
        """
        moves = []

        # Consider open spaces
        # Check space in front
        move_f = self._current_coords + self._direction
        if self._board.query_space(move_f) is None:
            moves.append(move_f)

        # Check space 2 in front (if in starting spot)
        move_ff = self._current_coords + (2 * self._direction)
        if (
                self._current_coords == self._starting_coords
                and self._board.query_space(move_ff) is None
        ):
            moves.append(move_ff)

        # Consider captures
        move_fl = self._current_coords + self._direction + np.array([1, 0])
        player_fl = self._board.query_space(move_fl)
        if (
                player_fl is not None
                and player_fl.player_controller != self._player_controller
        ):
            moves.append(move_fl)

        move_fr = self._current_coords + self._direction + np.array([-1, 0])
        player_fr = self._board.query_space(move_fr)
        if (
                player_fr is not None
                and player_fr.player_controller != self._player_controller
        ):
            moves.append(move_fr)

        return moves

    def _get_promotion_zone(self) -> int:
        """
        Get the y-value associated with the pawn "promotion zone" in the pawn's
            forward direction.

        :return: y-value at which the pawn will promote
        :rtype: int
        """
        if self._moving_down():
            return 0
        else:
            return cast(int, self._board.dimensions[1]) - 1

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

        # Check for promote
        promotion_zone = self._get_promotion_zone()
        if coords[1] == promotion_zone:
            # TODO request promotion input from user
            self._board.add_piece(
                Queen(
                    self._board,
                    self._piece_char,
                    self._piece_pxl_hex,
                    self._current_coords,
                    self._player_controller
                )
            )

        self._current_coords = coords
        return True
