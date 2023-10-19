from src.core.model.piece import Piece


class Player:
    """
    Object representing the state of a player in the game and its controlled
     pieces.
    """

    __slots__ = ('_pieces', '_player_number')

    def __init__(self, player_number: int):
        """
        Initialize an instance of Piece.

        :param player_number: The board the piece belongs to.
        """
        self._player_number = player_number

    @property
    def player_number(self):
        return self._player_number

    @property
    def pieces(self):
        return self._pieces

    def add_piece(self, piece: Piece):
        self._pieces.add(piece)
