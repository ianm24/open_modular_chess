from __future__ import annotations

from typing import Any
from typing import cast
from typing import Collection
from typing import MutableSet
from typing import Optional

import numpy as np
from numpy import ndarray

from omc.core.exception.exception import NegativePieceCoordinatesException
from omc.core.exception.exception import NegativePiecePlayerNumException
from omc.core.exception.exception import NonCurrentPiecePlayerNumException
from omc.core.exception.exception import PieceAlreadyAtLocationException
from omc.core.exception.exception import PiecePixelHexOutOfBoundsException
from omc.core.exception.exception import PieceSubclassInvalidException


class Board:
    """
    Object representing the state of the board, its present layout, and
     dimensions.
    """

    def __init__(
            self, dimensions: ndarray[int],
            layout: ndarray[Player | None]
    ):
        """
        Initialize an instance of Board.

        :param dimensions: Dimensions of the board
        :type dimensions: ndarray[int]
        :param layout: Layout of pieces on the board
        :type layout: ndarray[Optional[Piece]]
        """
        self._dimensions: ndarray[int] = dimensions
        self._layout: ndarray[Player | None] = layout
        self._players: dict[int, Player] = dict()

    @classmethod
    def empty(cls, dimensions: ndarray[int]) -> Board:
        """
        Instantiate an empty board.

        :param dimensions: Dimensions of board
        :type dimensions: ndarray[int]
        :return: Empty board instance
        :rtype: Board
        """
        return Board(dimensions, np.empty(tuple(dimensions), dtype=object))

    @property
    def dimensions(self) -> ndarray[int]:
        """
        Get dimensions of the board.

        :return: Dimensions of the board
        :rtype: ndarray[int]
        """
        return self._dimensions

    @property
    def layout(self) -> ndarray[Player | None]:
        """
        Get layout of the board.

        :return: Layout of the board
        :rtype: ndarray[Player | None]
        """
        return self._layout

    @property
    def current_players(self) -> dict[int, Player]:
        """
        Get current players on the board.

        :return: Current players on the board
        :rtype: ndarray[int]
        """
        return self._players

    def add_piece(self, piece_: Piece, replace_existing: bool = False) -> None:
        """
        Add a piece to the board.

        :param piece_: The piece to add
        :type piece_: Piece
        :param replace_existing: Whether to replace an existing piece at the
            same location
        :rtype: bool
        :return: None
        """
        current_piece = cast(
            Optional[Piece],
            self.layout[tuple(piece_.current_coords)]
        )
        if current_piece and not replace_existing:
            raise PieceAlreadyAtLocationException(
                f'Cannot add {piece_.__class__.__name__} to the board because'
                f' {current_piece.__class__.__name__} already present at the'
                f' location {current_piece.current_coords}'
            )
        self._layout[tuple(piece_.current_coords)] = piece_

    def remove_piece(self, piece_: Piece) -> None:
        """
        Remove a piece from the board.

        :param piece_: The piece to remove
        :type piece_: Piece
        :return: None
        """
        self._layout[tuple(piece_.current_coords)] = None

    def add_player(self, player_: Player) -> None:
        """
        Add a player to the board.

        :param player_: Player to add to the board
        :type player_: Player
        :return: None
        """
        self._players[player_.player_number] = player_

    def remove_player(self, player_: Player) -> None:
        """
        Remove a player from the board.

        :param player_: Player to remove from the board
        :type player_: Player
        :return: None
        """
        self._players[player_.player_number] = player_

    def get_player(self, player_number: int) -> Player:
        """
        Get a player on the board.

        :param player_number: Number of the player on the board
        :type player_number: int
        :return: Player corresponding to the specified player number
        :rtype: Player
        """
        return self._players[player_number]

    def __eq__(self, other: Any):
        """
        Compare this instance to another instance for equality.

        :param other: The other instance to compare to.
        :type other: Any
        :return: True if the instances are considered equal, False otherwise.
        :rtype: bool
        """
        if isinstance(other, Board):
            return (
                np.array_equal(self.dimensions, other.dimensions)
                and np.array_equal(self.layout, other.layout)
                and self.current_players == other.current_players
            )
        return False

    def on_board(self, space: ndarray[int]) -> bool:
        """
        Query whether a space is on the board

        :param space: coordinate denoting the space to be queried
        :type space: ndarray[int]
        :return: Whether the space is on the board
        :rtype: bool
        """
        return bool((space >= 0 or space < self._dimensions).all())

    def query_space(self, space: ndarray[int]) -> Piece | None:
        """
        Query a space for what piece exists there, if any, or None otherwise.

        :param space: coordinate denoting the space to be queried
        :type space: ndarray[int]
        :return: Piece at the queried space in the layout
        :rtype: Optional[Piece]
        """
        try:
            return cast(Optional[Piece], self._layout[tuple(space)])
        except IndexError:
            return None  # Handle out-of-bounds coordinates


class Piece:
    """
    Object representing the state of a piece in the game, its depiction,
     controlling player, and coordinates.
    """

    DEFAULT_PIECE_CHAR: str = ''
    DEFAULT_PIECE_PIXEL_HEX: int = 0

    def __init__(
            self, board_: Board,
            piece_char: str | None = None,
            piece_pxl_hex: int | None = None,
            current_coords: ndarray[int] | None = None,
            player_controller: int | None = None
    ):
        """
        Initialize an instance of Piece.

        :param board_: The board the piece belongs to.
        :type board_: Board
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

        if self.DEFAULT_PIECE_CHAR == '':
            raise PieceSubclassInvalidException(
                "Error: Default piece character for piece"
                f" {self.__class__.__name__} is missing. Please set"
                " default piece character to a 1 character string."
            )

        if (
                self.DEFAULT_PIECE_PIXEL_HEX < 1
                or self.DEFAULT_PIECE_PIXEL_HEX > (2 ** 64) - 1
        ):
            raise PieceSubclassInvalidException(
                "Error: Default piece pixel-hex for"
                f" {self.__class__.__name__} is out of bounds. Default"
                f" pixel-hex is {piece_pxl_hex} which is not between 1 and"
                " 2^64 - 1."
            )

        # Override defaults
        if piece_char is None:
            piece_char = self.DEFAULT_PIECE_CHAR

        if piece_pxl_hex is None:
            piece_pxl_hex = self.DEFAULT_PIECE_PIXEL_HEX

        if current_coords is None:
            current_coords = np.zeros(len(board_.dimensions), dtype=int)

        if player_controller is None:
            player_controller = 1

        # Set values
        self._board = board_

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

    def list_moves(self) -> list[ndarray[int] | None]:
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


class Player:
    """
    Object representing the state of a player in the game and its controlled
     pieces.
    """

    def __init__(self, player_number: int):
        """
        Initialize an instance of Piece.

        :param player_number: The board the piece belongs to.
        :ptype player_number: int
        """
        self._pieces: MutableSet[Piece] = set()
        self._player_number = player_number

    @property
    def player_number(self) -> int:
        """
        Gets the player number.

        :return: Player number
        :rtype: int
        """
        return self._player_number

    @property
    def pieces(self) -> Collection[Piece]:
        """
        Gets the pieces owned by the player.

        :return: Collection of pieces owned by the player
        :rtype: Collection[Piece]
        """
        return self._pieces

    def add_piece(self, piece_: Piece) -> None:
        """
        Add a piece to the collection owned by the player.

        :param piece_: Piece to be added
        :type piece_: Piece
        :return: None
        """
        self._pieces.add(piece_)
