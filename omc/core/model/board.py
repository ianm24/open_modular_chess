from __future__ import annotations

from typing import Any
from typing import Callable
from typing import cast
from typing import Collection

import numpy as np
from colorama import Fore
from colorama import Style
from numpy import ndarray

from omc.core.exception.exception import NegativePieceCoordinatesException
from omc.core.exception.exception import NegativePiecePlayerNumException
from omc.core.exception.exception import NonCurrentPiecePlayerNumException
from omc.core.exception.exception import PiecePixelHexOutOfBoundsException
from omc.core.exception.exception import PieceSubclassInvalidException


class Board:
    """
    Object representing the state of the board, its present layout, and
     dimensions.
    """
    PLAYER_COLORS = [Fore.BLUE, Fore.RED, Fore.GREEN, Fore.YELLOW]

    def __init__(
            self, board_id: int, dimensions: tuple[int, ...],
            layout: ndarray[Piece | None, Any]
    ):
        """
        Initialize an instance of Board.

        :param board_id: Id for the board
        :type board_id: int
        :param dimensions: Dimensions of the board
        :type dimensions: tuple[int, ...]
        :param layout: Layout of pieces on the board
        :type layout: ndarray[Piece | None]
        """
        self._board_id: int = board_id
        self._board_state_hash_dirty: bool = True
        self._board_state_hash: int = 0
        self._dimensions: tuple[int, ...] = dimensions
        self._layout: ndarray[Piece | None, Any] = layout
        self._players: dict[int, Player] = dict()

    @classmethod
    def empty(cls, board_id: int, dimensions: tuple[int, Any]) -> Board:
        """
        Instantiate an empty board.

        :param board_id: Id for the board
        :type board_id: int
        :param dimensions: Dimensions of board
        :type dimensions: tuple[int, ...]
        :return: Empty board instance
        :rtype: Board
        """
        return Board(
            board_id, dimensions, np.empty(tuple(dimensions), dtype=Piece)
        )

    @property
    def id(self) -> int:
        """
        Get ID of the board.

        :return: ID of the board
        :rtype: int
        """
        return self._board_id

    @property
    def dimensions(self) -> tuple[int, ...]:
        """
        Get dimensions of the board.

        :return: Dimensions of the board
        :rtype: tuple[int, ...]
        """
        return self._dimensions

    @property
    def layout(self) -> ndarray[Piece | None, Any]:
        """
        Get layout of the board.

        :return: Layout of the board
        :rtype: ndarray[Piece | None]
        """
        return self._layout

    @property
    def current_players(self) -> dict[int, Player]:
        """
        Get current players on the board.

        :return: Current players on the board
        :rtype: tuple[int, ...]
        """
        return self._players

    @property
    def board_state_hash(self) -> int:
        """
        Get the hash of the board state.

        :return: Hash of the board state
        :rtype: int
        """
        if self._board_state_hash_dirty:
            self._board_state_hash = 0
            for index, piece in np.ndenumerate(self._layout):
                piece_hash = piece.piece_state_hash if piece else None
                self._board_state_hash += hash((index, piece_hash))
            self._board_state_hash_dirty = False
        return self._board_state_hash

    def add_piece(self, piece: Piece) -> bool:
        """
        Add a piece to the board.

        :param piece: The piece to add
        :type piece: Piece
        :return: Whether piece addition was successful
        :rtype: bool
        """
        if self.query_space(piece.current_coords) is not None:
            print("There is already a piece at this location on the board.")
            return False
        index = self.coord_to_index(piece.current_coords)
        self._layout[index] = piece
        self._board_state_hash_dirty = True
        return True

    def remove_piece(self, piece: Piece) -> bool:
        """
        Remove a piece from the board.

        :param piece: The piece to remove
        :type piece: Piece
        :return: Whether piece removal was successful
        :rtype: bool
        """
        if self.query_space(piece.current_coords) != piece:
            print("The piece to remove does not belong to this board.")
            return False
        index = self.coord_to_index(piece.current_coords)
        self._layout[index] = None
        piece.remove_from_play()
        self._board_state_hash_dirty = True
        return True

    def add_player(self, player: Player) -> bool:
        """
        Add a player to the board.

        :param player: Player to add to the board
        :type player: Player
        :return: Whether player addition was successful
        :rtype: bool
        """
        if player.player_number in self._players:
            print("The player to add is already on the board.")
            return False
        self._players[player.player_number] = player
        self._board_state_hash_dirty = True
        return True

    def remove_player(self, player: Player) -> bool:
        """
        Remove a player from the board.

        :param player: Player to remove from the board
        :type player: Player
        :return: Whether player removal was successful
        :rtype: bool
        """
        if player.player_number not in self._players:
            print("The player to remove isn't on the board.")
            return False
        del self._players[player.player_number]
        self._board_state_hash_dirty = True
        return True

    def get_player(self, player_number: int) -> Player:
        """
        Get a player on the board.

        :param player_number: Number of the player on the board
        :type player_number: int
        :return: Player corresponding to the specified player number
        :rtype: Player
        """
        return self._players[player_number]

    @staticmethod
    def _highlight_piece(
            piece: Piece | None,
            select_player: Player | None,
            select_piece: Piece | None
    ) -> bool:
        if piece is None:
            return False

        if select_piece is not None:
            if select_piece == piece:
                return True

        if select_player is not None:
            if piece.player_controller == select_player.player_number:
                return True

        return False

    def get_board_chars(
            self,
            *,
            select_player: Player | None = None,
            select_piece: Piece | None = None,
            primary_color: str | None = None,
            secondary_color: str | None = None
    ) -> str:
        """
        Print the board to the command line.

        :param select_piece: TODO
        :param select_player: TODO
        :param primary_color: TODO
        :param secondary_color: TODO
        :return: String representation of the board
        :rtype: str
        """
        assert len(self._dimensions) == 2
        board_str = ''
        board_str += '+--------+\n'
        selected_piece_moves = (
            select_piece.list_moves() if select_piece else []
        )
        for yi, row in enumerate(reversed(self._layout)):
            y = self._dimensions[1] - yi - 1
            board_str += '|'
            for x, piece in enumerate(row):
                highlight_move = secondary_color is not None and (
                    (x, y) in selected_piece_moves
                )
                if highlight_move:
                    board_str += cast(str, secondary_color)
                if piece is None:
                    board_str += ' '
                    if highlight_move:
                        board_str += Style.RESET_ALL
                else:
                    highlight_piece = primary_color is not None and (
                        self._highlight_piece(
                            piece, select_player, select_piece
                        )
                    )
                    if highlight_piece:
                        board_str += cast(str, primary_color)
                    board_str += piece.piece_char
                    if highlight_piece:
                        board_str += Style.RESET_ALL
            board_str += '|\n'
        board_str += '+--------+\n'
        return board_str

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
                self.id == other.id
                and self.dimensions == other.dimensions
                and np.array_equal(self.layout, other.layout)
                and self.current_players == other.current_players
            )
        return False

    def on_board(self, space: tuple[int, ...]) -> bool:
        """
        Query whether a space is on the board

        :param space: coordinate denoting the space to be queried
        :type space: tuple[int, ...]
        :return: Whether the space is on the board
        :rtype: bool
        """
        return all(
            [
                0 <= coord < dim
                for coord, dim in zip(space, self._dimensions)
            ]
        )

    @staticmethod
    def coord_to_index(coord: tuple[int, ...]) -> tuple[int, ...]:
        """
        Converts an n-dimensional space to an n-dimensional index.

        :param coord: coord to convert
        :type coord: tuple[int, ...]
        :return: index corresponding to the space
        :rtype: tuple[int, ...]
        """
        return tuple(reversed(coord))

    @staticmethod
    def index_to_coord(index: tuple[int, ...]) -> tuple[int, ...]:
        """
        Converts an n-dimensional index to an n-dimensional space.

        :param index: index to convert
        :type index: tuple[int, ...]
        :return: coord corresponding to the index
        :rtype: tuple[int, ...]
        """
        return tuple(reversed(index))

    def query_space(self, space: tuple[int, ...]) -> Piece | None:
        """
        Query a space for what piece exists there, if any, or None otherwise.

        :param space: coordinate denoting the space to be queried
        :type space: tuple[int, ...]
        :return: Piece at the queried space in the layout
        :rtype: Piece | None
        """
        try:
            index = self.coord_to_index(space)
            return cast(Piece | None, self._layout[index])
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
            self, board: Board,
            piece_char: str | None = None,
            piece_pxl_hex: int | None = None,
            current_coords: tuple[int, ...] | None = None,
            player_controller: int | None = None
    ):
        """
        Initialize an instance of Piece.

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
            current_coords = tuple([0] * len(board.dimensions))

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

        self._piece_pxl_hex = piece_pxl_hex

        if current_coords[0] < 0 or current_coords[1] < 0:
            raise NegativePieceCoordinatesException(
                "Error: Piece coordinates for"
                f" {self.__class__.__name__} are negative. Coordinates"
                f" are {current_coords} which should be greater or equal"
                " to (0, 0)")

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

        # For caching moves between board state changes
        self._cached_moves: list[tuple[int, ...]] = []
        self._last_board_state_hash: int = 0

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
    def board_id(self) -> int:
        """
        Gets the id of the board the piece belongs to.

        :return: ID of associated board
        :rtype: int
        """
        return self._board.id

    @property
    def current_coords(self) -> tuple[int, ...]:
        """
        Gets the current coordinates of the piece

        :return: Current player coordinate
        :rtype: tuple[int, ...]
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

    @property
    def piece_state_hash(self) -> int:
        """
        Gets a hash of the current state of the piece.

        :return: Hash of the current state of the piece
        :rtype: int
        """
        return hash(self._current_coords) + hash(self._player_controller)

    def list_moves(self) -> list[tuple[int, ...]]:
        """
        Gives a list of all available moves for the piece.

        :return: List of moves currently able to be performed by
            the piece.
        :rtype: list[tuple[int, ...]]
        """
        if self._board.board_state_hash == self._last_board_state_hash:
            return self._cached_moves
        raise NotImplementedError

    def move(self, coords: tuple[int, ...]) -> bool:
        """
        Performs an action on the piece using arguments.

        :param coords: Coordinates for the space of the attempted move.
        :type coords: tuple[int, ...]
        :return: True on successful move, False otherwise.
        :rtype: bool
        """

        # Check if move is valid
        if coords not in self.list_moves():
            print("Invalid Move.")
            return False

        self._board.remove_piece(self)
        self._current_coords = coords
        capture_piece = self._board.query_space(coords)
        if capture_piece is not None:
            self._board.remove_piece(capture_piece)
        self._board.add_piece(self)
        return True

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

        self._board.current_players[self._player_controller].remove_piece(self)
        self._player_controller = new_player
        self._board.current_players[new_player].add_piece(self)
        return True

    @classmethod
    def list_actions(cls) -> list[str]:
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
                coords = tuple([
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

    def __eq__(self, other: Any):
        """
        Compare this instance to another instance for equality.

        :param other: The other instance to compare to.
        :type other: Any
        :return: True if the instances are considered equal, False otherwise.
        :rtype: bool
        """
        if isinstance(other, Piece):
            return (
                self.board_id == other.board_id
                and self.current_coords == other.current_coords
                and self.current_players == other.current_players
                and self.player_controller == other.player_controller
                and self.piece_pxl_hex == other.piece_pxl_hex
                and self.piece_char == other.piece_char
            )
        return False

    def remove_from_play(self):
        """
        Removes a piece from play by setting coordinates to None.
        """

        self._current_coords = None


''' TypeVar representing subclasses of "Piece" '''
PieceClass = Callable[..., Piece]


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
        self._pieces: list[Piece] = []
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

    def add_piece(self, piece: Piece) -> bool:
        """
        Add a piece to the collection owned by the player.

        :param piece: Piece to be added
        :type piece: Piece
        :return: Whether the piece removal was successful
        :rtype: bool
        """
        if piece.player_controller != self.player_number:
            print("The piece to add is not controlled by this player.")
            return False
        if piece in self._pieces:
            print("The piece to add is already controlled by this player.")
            return False
        self._pieces.append(piece)
        return True

    def remove_piece(self, piece: Piece) -> bool:
        """
        Add a piece to the collection owned by the player.

        :param piece: Piece to be added
        :type piece: Piece
        :return: Whether the piece removal was successful
        :rtype: bool
        """
        if piece not in self._pieces:
            print("The piece to remove is not controlled by this player.")
            return False
        self._pieces.remove(piece)
        return True

    def __eq__(self, other: Any):
        """
        Compare this instance to another instance for equality.

        :param other: The other instance to compare to.
        :type other: Any
        :return: True if the instances are considered equal, False otherwise.
        :rtype: bool
        """
        if isinstance(other, Player):
            return (
                self.player_number == other.player_number
                and self.pieces == other.pieces
            )
        return False
