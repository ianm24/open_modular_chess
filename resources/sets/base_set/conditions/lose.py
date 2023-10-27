from omc.core.model.board import Board, Player
from omc.core.model.condition import Condition
from resources.sets.base_set.pieces.king import King


class Lose(Condition):
    @staticmethod
    def test_condition(board: Board, player: Player) -> bool:
        return not any(
            issubclass(type(piece), King) for piece in player.pieces
        )
