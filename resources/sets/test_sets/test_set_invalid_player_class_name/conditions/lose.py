from omc.core.model.board import Board
from omc.core.model.board import Player
from omc.core.model.condition import Condition


class Lose(Condition):
    @staticmethod
    def test_condition(board: Board, player: Player) -> bool:
        # TODO add checkmate
        return not any(
            piece.__class__.__name__ == 'King' for piece in player.pieces
        )
