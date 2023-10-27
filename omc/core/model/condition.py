from omc.core.model.board import Board
from omc.core.model.board import Player


class Condition:
    @staticmethod
    def test_condition(board: Board, player: Player) -> bool:
        raise NotImplementedError
