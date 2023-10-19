from typing import Optional

import numpy as np
import pytest
from numpy import ndarray

from omc.core.exception.exception import PlayerNotControllingPieceException
from omc.core.model.board import Board
from omc.core.model.board import Piece
from omc.core.model.board import Player


class SimplePiece(Piece):
    """
    Subclass used to test piece class
    """

    DEFAULT_PIECE_CHAR: str = 't'
    DEFAULT_PIECE_PIXEL_HEX: int = 0xFF18181818181818

    def list_moves(self) -> list[Optional[tuple[int, int]],]:
        """
        Implements list_moves for testing
        """
        return [np.asarray([0, 1])]


'''__init__ tests'''


def test_player_number_immutable():
    """
    Ensures proper function when a player has an attempted player_number edit
    """
    expected_player_number = 1

    p = Player(1)

    with pytest.raises(AttributeError):
        p.player_number = 2
    assert p.player_number == expected_player_number


'''AddPiece Tests'''


@pytest.mark.xfail(reason="Add piece does not yet check player controller")
def test_add_piece_not_controlled():
    """
    Ensures proper functionality when a player adds a piece it doesn't control
    """
    test_board = Board.empty(np.array([8, 8]))
    player2 = Player(2)
    test_board.add_player(Player(1))
    test_board.add_player(player2)
    piece = SimplePiece(test_board)

    with pytest.raises(PlayerNotControllingPieceException):
        player2.add_piece(piece)
    assert piece not in player2.pieces


@pytest.mark.xfail(reason="Add piece does not return a success boolean")
def test_add_piece():
    """
    Ensures proper functionality when a player adds a valid piece
    """
    test_board = Board.empty(np.array([8, 8]))
    player = Player(1)
    test_board.add_player(player)
    piece = SimplePiece(test_board)

    assert player.add_piece(piece) is True
