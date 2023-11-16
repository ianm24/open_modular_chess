from omc.core.model.board import Player


class ChessPlayer(Player):
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
        super().__init__(player_number)
        self._in_check: bool = False

    @property
    def in_check(self) -> bool:
        """
        Gets the check status of the player.

        :return: Boolean whether or not the player is in check
        :rtype: bool
        """
        return self._in_check

    def set_check(self, status: bool):
        """
        Sets this player's check status

        :param status: The check status to set this player as
        :ptype status: bool
        """

        self._in_check = status

    def update_threatened_spaces(self):
        """
        Recalculates threatened spaces for a player
        """
        updated_threatened_spaces = []
        causing_check = False

        board = self._pieces[0]._board

        for piece in self._pieces:
            # Pawns have different capture criteria
            if piece.piece_char == 'P' and len(piece.list_moves()) > 0:
                base_move = piece.list_moves()[0]
                left_capture = (base_move[0]-1, base_move[1])
                right_capture = (base_move[0]+1, base_move[1])

                if piece._board.on_board(left_capture):
                    updated_threatened_spaces.append(left_capture)

                    # If opposing king is threatened, it causes check
                    th_piece = board.query_space(left_capture)
                    if (
                        th_piece is not None
                        and th_piece.piece_char == "K"
                        and th_piece.player_controller != self.player_number
                    ):
                        causing_check = True
                if piece._board.on_board(right_capture):
                    updated_threatened_spaces.append(right_capture)

                    # If opposing king is threatened, it causes check
                    th_piece = board.query_space(right_capture)
                    if (
                        th_piece is not None
                        and th_piece.piece_char == "K"
                        and th_piece.player_controller != self.player_number
                    ):
                        causing_check = True
            else:
                for move in piece.list_moves():
                    updated_threatened_spaces.append(move)

                    # If opposing king is threatened, it causes check
                    th_piece = board.query_space(move)
                    if (
                        th_piece is not None
                        and th_piece.piece_char == "K"
                        and th_piece.player_controller != self.player_number
                    ):
                        causing_check = True

        if causing_check:
            opposing_player_controller = (self.player_number % 2) + 1
            board.get_player(opposing_player_controller).set_check(True)

        self._threatened_spaces = updated_threatened_spaces

    def check_lose_condition(self) -> bool:
        """
        Checks if this player has lost

        :return: True if player has lost, False otherwise
        :rtype: bool
        """

        if self.in_check:
            # Check for moveable pieces, pieces that cant stop check cant move
            moveable_pieces = []
            for piece in self.pieces:
                if len(piece.list_moves()) == 0:
                    continue
                moveable_pieces.append(piece)
            if moveable_pieces == []:
                return True

        return False

    def check_win_condition(self) -> bool:
        """
        Checks if this player has won

        :return: True if player has won, False otherwise
        :rtype: bool
        """
        opposing_player_controller = (self.player_number % 2) + 1
        board = self._pieces[0]._board
        if board.get_player(opposing_player_controller).check_lose_condition():
            return True

        return False
