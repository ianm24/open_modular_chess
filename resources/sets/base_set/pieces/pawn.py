from typing import cast

from omc.core.model.board import Board
from resources.sets.base_set.helper.chess_piece import ChessPiece
from resources.sets.base_set.pieces.queen import Queen


class Pawn(ChessPiece):
    """Object representing a pawn piece."""

    DEFAULT_PIECE_CHAR: str = 'P'
    DEFAULT_PIECE_PIXEL_HEX: int = 0x183C3C1818183C7E

    def __init__(
            self, board: Board,
            piece_char: str | None = None,
            piece_pxl_hex: int | None = None,
            current_coords: tuple[int, ...] | None = None,
            player_controller: int | None = None
    ):
        """
        Initialize an instance of Pawn. Calls the superclass constructor, but
            also instantiates the direction in which the Pawn is allowed to
            advance.

        :param board: The board the piece belongs to.
        :type board: Board
        :param piece_char: 1-character string that represent the piece in
            the command line display. Default is set by subclass.
        :type piece_char: str | None
        :param piece_pxl_hex: Hex value of 64-bit number representing an
            8x8 pixel grid to display the piece in a GUI. Default is set
            by subclass.
        :type piece_pxl_hex: int | None
        :param current_coords: Represents the current placement of the
            piece on the board. Default is (0, 0).
        :type current_coords: tuple[int, ...] | None
        :param player_controller: The player controlling this piece.
            Default is 1.
        :type player_controller: int | None
        """
        super().__init__(
            board, piece_char, piece_pxl_hex, current_coords, player_controller
        )
        self.DIRECTIONS = ((0, 1),) if self._moving_down() else ((0, -1),)

    def _moving_down(self) -> bool:
        """
        Indicate whether the pawn is moving in the negative y direction.

        :return: Whether the pawn is moving in the negative y direction
        :rtype: bool
        """
        return self._player_controller % 2 == 1

    def list_moves(self) -> list[tuple[int, ...]]:
        """
        Gives a list of all available moves for the piece.

        :return: List of moves currently able to be performed by
            the piece.
        :rtype: list[tuple[int, ...]]
        """
        moves: list[tuple[int, ...]] = []

        if self.current_coords is None:
            print("This piece is not in play.")
            return moves

        for direction in self.DIRECTIONS:
            # Consider open spaces
            # Check space 1 in front
            move_f = (
                self._current_coords[0] + direction[0],
                self._current_coords[1] + direction[1]
            )
            if self._board.query_space(move_f) is None:
                moves.append(move_f)

            # Check space 2 in front (if in starting spot)
            move_ff = (
                self._current_coords[0] + 2 * direction[0],
                self._current_coords[1] + 2 * direction[1]
            )
            if (
                    self._current_coords == self._starting_coords
                    and self._board.query_space(move_ff) is None
            ):
                moves.append(move_ff)

            # Consider captures
            move_fl = (
                self._current_coords[0] + direction[0] + 1,
                self._current_coords[1] + direction[1]
            )
            player_fl = self._board.query_space(move_fl)
            if (
                    player_fl is not None
                    and player_fl.player_controller != self._player_controller
            ):
                moves.append(move_fl)

            move_fr = (
                self._current_coords[0] + direction[0] - 1,
                self._current_coords[1] + direction[1]
            )
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

    def move(self, coords: tuple[int, ...]) -> bool:
        """
        Performs an action on the piece using arguments.

        :param coords: Coordinates of the attempted move
        :type coords: tuple[int, ...]
        :return: True on successful move, False otherwise.
        :rtype: bool
        """
        moved = super().move(coords)

        if not moved:
            return False

        # Check for promote
        if coords[1] == self._get_promotion_zone():
            # TODO request promotion input from user
            self._board.add_piece(Queen(
                self._board,
                self._piece_char,
                self._piece_pxl_hex,
                self._current_coords,
                self._player_controller
            ))

        return True
