# Code by Chandler McDowell 2023
from typing import Optional

import numpy as np
from numpy import ndarray

from src.core.exception.exception import NegativePieceCoordinatesException
from src.core.exception.exception import NegativePiecePlayerNumException
from src.core.exception.exception import NonCurrentPiecePlayerNumException
from src.core.exception.exception import PiecePixelHexOutOfBoundsException
from src.core.exception.exception import PieceSubclassInvalidException
from src.core.model.board import Board


class Piece:
    """
    Object representing the state of a piece in the game, its depiction,
     controlling player, and coordinates.
    """

    __slots__ = ('_piece_char', '_piece_pxl_hex', '_board',
                 '_current_coords', '_starting_coords', '_player_controller')

    _default_piece_char: str = ''
    _default_piece_pxl_hex: int = 0

    def __init__(
            self, board: Board,
            piece_char: Optional[str] = None,
            piece_pxl_hex: Optional[int] = None,
            current_coords: Optional[ndarray[int]] = None,
            player_controller: Optional[int] = None
    ):
        """
        Initialize an instance of Piece.

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
        # Assertions to validate subclassing
        if self.__class__.__name__ == 'Piece':
            raise NotImplementedError(
                'Attempted to instantiate base Piece class directly'
            )

        if self._default_piece_char == '':
            raise PieceSubclassInvalidException(
                "Error: Default piece character for piece"
                f" {self.__class__.__name__} is missing. Please set"
                " default piece character to a 1 character string."
            )

        if (
                self._default_piece_pxl_hex < 1
                or self._default_piece_pxl_hex > (2 ** 64) - 1
        ):
            raise PieceSubclassInvalidException(
                "Error: Default piece pixel-hex for"
                f" {self.__class__.__name__} is out of bounds. Default"
                f" pixel-hex is {piece_pxl_hex} which is not between 1 and"
                " 2^64 - 1."
            )

        # Override defaults
        if piece_char is None:
            piece_char = self._default_piece_char

        if piece_pxl_hex is None:
            piece_pxl_hex = self._default_piece_pxl_hex

        if current_coords is None:
            current_coords = np.zeros(tuple(board.dimensions))

        if player_controller is None:
            player_controller = 1

        # Set values
        self._board = board

        if len(piece_char) > 1:
            print(
                "Warning: Piece character for piece"
                f" {self.__class__.__name__} is too long. Length of piece"
                f" character is {len(piece_char)} which is longer than 1."
                " Piece character has been set to the first character,"
                f" {piece_char[0]}."
            )
            piece_char = piece_char[0]

        self._piece_char = piece_char

        # Ensure piece pixel-hex is valid
        if piece_pxl_hex < 1 or piece_pxl_hex > (2 ** 64) - 1:
            raise PiecePixelHexOutOfBoundsException(
                "Error: Piece pixel-hex for"
                f" {self.__class__.__name__} is out of bounds. Pixel-hex"
                f" is {piece_pxl_hex} which is not between 1 and 2^64 - 1."
            )

        if piece_pxl_hex < 1 or piece_pxl_hex > (2 ** 64) - 1:
            raise PiecePixelHexOutOfBoundsException(
                "Error: Piece pixel-hex for"
                f" {self.__class__.__name__} is out of bounds. Pixel-hex"
                f" is {piece_pxl_hex} which is not between 1 and 2^64 - 1."
            )

        self._piece_pxl_hex = piece_pxl_hex

        if current_coords[0] < 0 or current_coords[1] < 0:
            raise NegativePieceCoordinatesException(
                "Error: Piece coordinates for"
                f" {self.__class__.__name__} are negative. Coordinates"
                f" are {current_coords} which should be greater or equal"
                " to (0,0)")

        self._current_coords = current_coords
        self._starting_coords = current_coords

        if player_controller < 0:
            raise NegativePiecePlayerNumException(
                "Error: Player controller for piece"
                f" {self.__class__.__name__} is negative. Player controller"
                f" is {player_controller} which is less than 0.")

        if player_controller not in self._board.current_players:
            raise NonCurrentPiecePlayerNumException(
                "Error: Player controller for piece"
                f" {self.__class__.__name__} is non-current. Player"
                f" controller is {player_controller} which is not a current"
                f" player: {self._board.current_players}.")

        self._player_controller = player_controller

    @property
    def piece_char(self) -> str:
        """
        Gets the character representation for the piece.

        :return: 1-character string that represent the piece in the command
            line display
        :rtype: str
        """
        return self._piece_char

    @property
    def piece_pxl_hex(self) -> int:
        """
        Gets the pixel-hex representation for the piece.

        :return: Hex value of 64-bit number representing an 8x8 pixel grid to
            display the piece in a GUI.
        :rtype: int
        """

        return self._piece_pxl_hex

    @property
    def current_players(self) -> list[int]:
        """
        Gets the list of current players from board.

        :return: List of the current player numbers
        :rtype: list[int]
        """

        return list(self._board.current_players.keys())

    @property
    def current_coords(self) -> ndarray[int]:
        """
        Gets the current coordinates of the piece

        :return: Current player coordinate
        :rtype: ndarray[int]
        """
        return self._current_coords

    @property
    def player_controller(self) -> int:
        """
        Gets the current player controller.

        :return: Number associated with player currently controlling the piece.
        :rtype: int
        """
        return self._player_controller

    def list_moves(self) -> list[Optional[ndarray[int]]]:
        """
        Gives a list of all available moves for the piece.

        :return: List of moves currently able to be performed by
            the piece.
        :rtype: list[Optional[ndarray[int]]]
        """

        raise NotImplementedError

    def move(self, coords: ndarray[int]) -> bool:
        """
        Performs an action on the piece using arguments.

        :param coords: Coordinates for the space of the attempted move.
        :type coords: ndarray[int]
        :return: True on successful move, False otherwise.
        :rtype: bool
        """

        # Check if move is valid
        if coords not in self.list_moves():
            print("Invalid Move.")
            return False

        self._current_coords = coords
        return True

    def capture(self, new_player: int) -> bool:
        """
        Attempt to capture this piece, removing it from the board and giving
        possession of the piece to `new_player`.

        :param new_player: Player number for the player capturing this piece
        :type new_player: int
        :return: True on successful capture, False otherwise.
        :rtype: bool
        """
        if self.set_player_control(new_player):
            self._current_coords = None
            self._board.remove_piece(self)
            return True
        return False

    def set_player_control(self, new_player: int) -> bool:
        """
        Changes the player in control of this piece.

        :param new_player: Player number taking control of the piece.
        :type new_player: int
        :return: True on successful action, False otherwise.
        :rtype: bool
        """

        if new_player < 0:
            print("Invalid Player Number (Negative).")
            return False

        valid_players = self.current_players

        if new_player not in valid_players:
            print(f"Invalid Player Number. (Valid Numbers: {valid_players})")
            return False

        self._player_controller = new_player
        return True

    def list_actions(self) -> list[str]:
        """
        Gives a list of all available actions for the piece.

        :return: List of actions currently able to be performed by
            the piece.
        :rtype: list[str]
        """

        return ["move", "control"]

    def perform_action(self, action: str, args: list[str]) -> bool:
        """
        Performs an action on the piece using arguments.

        :param action: Action to attempt to perform
        :type action: str
        :param args: list of arguments to the action
        :type args: list[str]
        :return: True on successful action, False otherwise.
        :rtype: bool
        """

        # Check if action is valid
        if action not in self.list_actions():
            print(f"Invalid Action. Valid Actions: {self.list_actions()}")
            return False

        if action == "move":
            num_dimensions = len(self._board.dimensions)
            try:
                coords = np.array([
                    int(args[i]) for i in range(num_dimensions)
                ])
            except IndexError:
                print(f"Invalid arguments for action {action}. Arguments must"
                      f" be {num_dimensions} integers for"
                      f" {num_dimensions}-dimensional board.")
                return False
            except ValueError:
                print(f"Invalid arguments for action {action}. Arguments must"
                      f" be {num_dimensions} integers for"
                      f" {num_dimensions}-dimensional board.")
                return False

            return self.move(coords)
        elif action == "control":
            try:
                player_controller = int(args[0])
            except ValueError:
                print(f"Invalid arguments for action {action}. Argument must"
                      " be one integer.")
                return False

            return self.set_player_control(player_controller)

        return False
