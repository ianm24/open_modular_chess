# Code by Chandler McDowell 2023
from typing import Optional

from core.exception.exception import MissingPieceCharException
from core.exception.exception import NegativePieceCoordinatesException
from core.exception.exception import NegativePiecePlayerNumException
from core.exception.exception import PiecePxlHexOutOfBoundsException
from core.model.board import Board
# TODO uncomment this once board updated with current_players
# from core.exception.exception import NonCurrentPiecePlayerNumException


class Piece:
    """Defines the base class for a piece."""
    __slots__ = ('_piece_char', '_piece_pxl_hex', '_board',
                 '_current_coords', '_player_controller')

    def __init__(
            self, piece_char: str, piece_pxl_hex: int, board: Board,
            current_coords: Optional[tuple[int, int]] = None,
            player_controller: Optional[int] = None
    ):
        """
        Constructor for a piece.

        Parameters:
            :param piece_char: 1-character string that represent the piece in
                the command line display
            :param piece_pxl_hex: Hex value of 64-bit number representing an
                8x8 pixel grid to display the piece in a GUI.
            :param board: The board the piece belongs to.
            :param current_coords: Represents the current placement of the
                piece on the board. Default is (0,0)
            :param player_controller: The player controlling this piece.
                Default is 1.
        """

        # Ensure piece character is valid
        if piece_char == "":
            raise MissingPieceCharException(
                "Error: Piece character for piece"
                f" {self.__class__.__name__} is missing. Please set"
                " piece character to a 1 character string.")

        if len(piece_char) > 1:
            print("Warning: Piece character for piece"
                  f" {self.__class__.__name__} is too long. Length of piece"
                  f" character is {len(piece_char)} which is longer than 1. "
                  "Piece character has been set to the first character,"
                  f"{piece_char[0]}.")
            piece_char = piece_char[0]

        self._piece_char = piece_char[0]

        # Ensure piece pixel-hex is valid
        if piece_pxl_hex < 1 or piece_pxl_hex > (2**64)-1:
            raise PiecePxlHexOutOfBoundsException(
                "Error: Piece pixel-hex for"
                f" {self.__class__.__name__} is out of bounds. Pixel-hex"
                f" is {piece_pxl_hex} which is not between 1 and 2^64 - 1.")

        self._piece_pxl_hex = piece_pxl_hex

        self._board = board

        if current_coords is None:
            current_coords = (0, 0)

        if current_coords[0] < 0 or current_coords[1] < 0:
            raise NegativePieceCoordinatesException(
                "Error: Piece coordinates for"
                f" {self.__class__.__name__} are negative. Coordinates"
                f" are {current_coords} which should be greater or equal"
                " to (0,0)")

        self._current_coords = current_coords

        if player_controller is None:
            player_controller = 1

        if player_controller < 0:
            raise NegativePiecePlayerNumException(
                "Error: Player controller for piece"
                f" {self.__class__.__name__} is negative. Player controller"
                f" is {player_controller} which is less than 0.")

        # TODO uncomment this once board updated with current_players
        # if player_controller not in self._board.current_players:
        #     raise NonCurrentPiecePlayerNumException(
        #         "Error: Player controller for piece"
        #         f" {self.__class__.__name__} is non-current. Player"
        #         f" controller is {player_controller} which is not a current"
        #         f" player: {self._board.current_players}.")

        self._player_controller = player_controller

    @property
    def piece_char(self) -> str:
        '''
        Gets the character representation for the piece.

        :return piece_char: 1-character string that represent the piece in
            the command line display
        '''
        return self._piece_char

    @property
    def piece_pxl_hex(self) -> int:
        '''
        Gets the pixel-hex representation for the piece.

        :return piece_pxl_hex: Hex value of 64-bit number representing an
            8x8 pixel grid to display the piece in a GUI.
        '''

        return self._piece_pxl_hex

    @property
    def current_players(self) -> list[int,]:
        '''
        Gets the list of current players from board.
        '''

        # return self._board.current_players
        return [0]  # TODO replace with commented line once board updated

    @property
    def current_coords(self) -> tuple[int, int]:
        '''
        Gets the current coordinates of the piece
        '''
        return self._current_coords

    @property
    def player_controller(self) -> int:
        '''
        Gets the current player controller.

        :return player_controller: Number associated with player currently"
        " controlling the piece.
        '''
        return self._player_controller

    def list_moves(self) -> list[Optional[tuple[int, int]],]:
        '''
        Gives a list of all available moves for the piece.

        :return moves_list: List of moves currently able to be performed by
            the piece.
        '''

        return [(0, 1)]

    def move(self, coords: tuple[int, int]) -> bool:
        '''
        Performs an action on the piece using arguments

        :return success: True on successful move, False otherwise.
        '''

        # Check if move is valid
        if coords not in self.list_moves():
            print("Invalid Move.")
            return False

        self._current_coords = coords
        return True

    def set_player_control(self, new_player: int) -> bool:
        '''
        Changes the player in control of this piece.

        :param new_player: Player number taking control of the piece.
        :return success: True on successful action, False otherwise.
        '''

        if new_player < 0:
            print("Invalid Player Number (Negative).")
            return False

        valid_players = self.current_players

        if new_player not in valid_players:
            print(f"Invalid Player Number. (Valid Numbers: {valid_players})")
            return False

        self._player_controller = new_player
        return True

    def list_actions(self) -> list[str,]:
        '''
        Gives a list of all available actions for the piece.

        :return action_list: List of actions currently able to be performed by
            the piece.
        '''

        return ["move", "control"]

    def perform_action(self, action: str, args: list[str,]) -> bool:
        '''
        Performs an action on the piece using arguments

        :return success: True on successful action, False otherwise.
        '''

        # Check if action is valid
        if action not in self.list_actions():
            print(f"Invalid Action. Valid Actions: {self.list_actions()}")
            return False

        if action == "move":
            try:
                x_coord = int(args[0])
                y_coord = int(args[1])
            except ValueError:
                print(f"Invalid arguments for action {action}. Arguments must"
                      " be two integers.")
                return False

            return self.move((x_coord, y_coord))
        elif action == "control":
            try:
                player_controller = int(args[0])
            except ValueError:
                print(f"Invalid arguments for action {action}. Argument must"
                      " be one integer.")
                return False

            return self.set_player_control(player_controller)
