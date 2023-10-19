from __future__ import annotations

from typing import Any
from typing import cast
from typing import Optional

import numpy as np
from numpy import ndarray

from src.core.exception.exception import PieceAlreadyAtLocationException
from src.core.model.piece import Piece
from src.core.model.player import Player


class Board:
    """
    Object representing the state of the board, its present layout, and
     dimensions.
    """

    __slots__ = ('_dimensions', '_layout', '_players')

    def __init__(
            self, dimensions: ndarray[int], layout: ndarray[Piece | None]
    ):
        """
        Initialize an instance of Board.

        :param dimensions: Dimensions of the board
        :type dimensions: ndarray[int]
        :param layout: Layout of pieces on the board
        :type layout: ndarray[Optional[Piece]]
        """
        self._dimensions: ndarray[int] = dimensions
        self._layout: ndarray[Piece | None] = layout
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
        return Board(dimensions, np.empty(tuple(dimensions), dtype=Piece))

    @property
    def dimensions(self) -> ndarray[int]:
        """
        Get dimensions of the board.

        :return: Dimensions of the board
        :rtype: ndarray[int]
        """
        return self._dimensions

    @property
    def layout(self) -> ndarray[Piece | None]:
        """
        Get dimensions of the board.

        :return: Dimensions of the board
        :rtype: ndarray[int]
        """
        return self._layout

    @property
    def current_players(self) -> dict[int, Player]:
        """
        Get dimensions of the board.

        :return: Dimensions of the board
        :rtype: ndarray[int]
        """
        return self._players

    def add_piece(self, piece: Piece, replace_existing: bool = False) -> None:
        """
        Add a piece to the board.

        :param piece: The piece to add
        :type piece: Piece
        :param replace_existing: Whether to replace an existing piece at the
            same location
        :rtype: bool
        :return: None
        """
        current_piece = cast(
            Optional[Piece],
            self.layout[tuple(piece.current_coords)]
        )
        if current_piece and not replace_existing:
            raise PieceAlreadyAtLocationException(
                f'Cannot add {piece.__class__.__name__} to the board because'
                f' {current_piece.__class__.__name__} already present at the'
                f' location {current_piece.current_coords}'
            )
        self._layout[tuple(piece.current_coords)] = piece

    def remove_piece(self, piece: Piece) -> None:
        """
        Remove a piece from the board.

        :param piece: The piece to remove
        :type piece: Piece
        :return: None
        """
        self._layout[tuple(piece.current_coords)] = None

    def add_player(self, player: Player) -> None:
        """
        Add a player to the board.

        :param player: Player to add to the board
        :type player: Player
        :return: None
        """
        self._players[player.player_number] = player

    def remove_player(self, player: Player) -> None:
        """
        Remove a player from the board.

        :param player: Player to remove from the board
        :type player: Player
        :return: None
        """
        self._players[player.player_number] = player

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
                self.dimensions == other.dimensions
                and self.layout == other.layout
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
