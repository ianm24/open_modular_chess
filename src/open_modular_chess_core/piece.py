# Code by Chandler McDowell 2023
from typing import Optional


class Piece:
    """Defines the base class for a piece."""
    __slots__ = ('_piece_char', '_piece_pxl_hex', 'current_coords')

    def __init__(
            self, piece_char: str, piece_pxl_hex: int,
            current_coords: Optional(tuple[int, int]) = None
    ):
        """
        Constructor for a piece.

        Parameters:
            :param piece_char: 1 character string that represent the piece in
                the command line display
            :param piece_pxl_hex: Hex value of 64-bit number representing an
                8x8 pixel grid to display the piece in a GUI.
            :param current_coords: Represents the current placement of the
                piece on the board.
        """

        # Ensure piece character is valid
        if piece_char == "":
            print("Error: Piece character for piece"
                  f" {self.__class__.__name__} is missing. Please set"
                  f" piece character to a 1 character string.")
            # TODO: Add MissingPieceCharException

        if len(piece_char) > 1:
            print("Warning: Piece character for piece"
                  f" {self.__class__.__name__} is too long. Length of piece"
                  f" character is {len(piece_char)} which is longer than 1. "
                  "Piece character has been set to the first character,"
                  f"{piece_char[0]}.")
            self._piece_char = piece_char[0]

        # Ensure piece pixel-hex is valid
        if piece_pxl_hex < 1 or piece_pxl_hex > (2**64)-1:
            print("Error: Piece pixel-hex for"
                  f" {self.__class__.__name__} is out of bounds. Pixel-hex"
                  f" is {piece_pxl_hex} which is not between 1 and 2^64 - 1.")
            # TODO: Add PiecePxlHexOutOfBoundsException

        self._piece_pxl_hex = piece_pxl_hex

        if current_coords is None:
            current_coords = (0, 0)

        self.current_coords = current_coords

    def list_moves(self) -> list[tuple(int, int),]:
        '''
        Gives a list of all available moves for the piece.

        :return moves_list: List of moves currently able to be performed by
            the piece.
        '''

        return [None]

    def move(self, coords: tuple(int, int)) -> bool:
        '''
        Performs an action on the piece using arguments

        :return success: True on successful move, False otherwise.
        '''

        # Check if move is valid
        if coords not in self.list_moves():
            print("Invalid Move.")
            return False

        self.current_coords = coords
        return True

    def list_actions(self) -> list[str,]:
        '''
        Gives a list of all available actions for the piece.

        :return action_list: List of actions currently able to be performed by
            the piece.
        '''

        return ["move"]

    def perform_action(self, action: str, args: list[str,]) -> bool:
        '''
        Performs an action on the piece using arguments

        :return success: True on successful action, False otherwise.
        '''

        # Check if action is valid
        if action not in self.list_actions():
            print("Invalid Action.")

        if action == "move":
            try:
                x_coord = int(args[0])
                y_coord = int(args[1])
                return self.move((x_coord, y_coord))
            except ValueError:
                print(f"Invalid arguments for action {action}")
                return False
