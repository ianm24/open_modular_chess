from omc.core.model.board import Board
from omc.core.model.board import Player
from omc.core.model.condition import Condition


class Win(Condition):
    @staticmethod
    def test_condition(board: Board, player: Player) -> bool:
        return (
            len(board.current_players) == 1
            and player.player_number in board.current_players
            and board.current_players[player.player_number] == player
        )
