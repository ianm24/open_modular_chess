import os
import platform
import time
from typing import cast

from colorama import Back
from colorama import Fore
from colorama import Style

import omc.core.load_set as load_set
from omc.core.model.board import Board
from omc.core.model.board import Piece
from omc.core.model.board import Player


class Game:
    def __init__(self):
        self.main_menu()

    def main_menu(self):
        os.system('cls' if platform.system() == 'Windows' else 'clear')
        print("Main Menu")
        print("1. Start Game")
        print("2. Settings")
        print("3. Quit Game")

        choice = input("Enter your choice: ")
        if choice == '1':
            self.play_game()
        elif choice == '2':
            self.settings()
        elif choice == '3':
            self.quit_game()

    @staticmethod
    def _show_board_for_player(board: Board, player: Player) -> None:
        print(
            board.get_board_chars(
                select_player=player,
                primary_color=Back.GREEN + Fore.BLACK + Style.BRIGHT
            )
        )

    @staticmethod
    def _show_board_for_piece(board: Board, piece: Piece) -> None:
        print(
            board.get_board_chars(
                select_piece=piece,
                primary_color=Back.GREEN + Fore.BLACK + Style.BRIGHT,
                secondary_color=Back.BLUE + Fore.BLACK + Style.BRIGHT,
            )
        )

    @staticmethod
    def _ask_for_piece(player: Player) -> Piece:
        coord_map = {piece.current_coords: piece for piece in player.pieces}
        coords = None
        while coords not in coord_map:
            print('What piece will you select? ("l" for list)')
            piece_select_args = input().split()
            if len(piece_select_args) == 1 and piece_select_args[0] == 'l':
                for piece in player.pieces:
                    print(
                        f'{piece.current_coords[0]} {piece.current_coords[1]}.'
                        f' {piece.piece_char}'
                    )
                print('\n')
                continue
            try:
                coords = tuple(int(arg) for arg in piece_select_args)
            except ValueError:
                print(
                    'Invalid piece. What piece will you select? ("l" for list)'
                )
                continue
        return coord_map[coords]

    @staticmethod
    def _ask_for_move(board: Board, piece: Piece) -> tuple[int, ...]:
        valid_moves = piece.list_moves()
        coords = None
        while coords not in valid_moves:
            print('What move will you make? ("l" for list)')
            piece_select_args = input().split()
            if len(piece_select_args) == 1 and piece_select_args[0] == 'l':
                for move in valid_moves:
                    to_piece = board.query_space(move)
                    to_char = (
                        to_piece.piece_char
                        if to_piece is not None else 'empty'
                    )
                    print(f'{move[0]} {move[1]}. {to_char}')
                print('\n')
                continue
            try:
                coords = tuple(int(x) for x in piece_select_args)
            except ValueError:
                print('Invalid move. What move will you make? ("l" for list)')
                continue
        return cast(tuple[int, ...], coords)

    def play_game(self):
        os.system('cls' if platform.system() == 'Windows' else 'clear')
        piece_map, board, win_con, lose_con = load_set.load_set("base_set")
        game_over = False
        while not game_over:
            for player_num, player in board.current_players.items():
                self._show_board_for_player(board, player)
                selected_piece = self._ask_for_piece(player)
                self._show_board_for_piece(board, selected_piece)
                selected_piece.move(self._ask_for_move(board, selected_piece))
                # if lose_con.test_condition(board, player):
                #     print(f'Player {player_num} loses!')
                #     game_over = True
                #     break
                # if win_con.test_condition(board, player):
                #     print(f'Player {player_num} wins!')
                #     game_over = True
                #     break
        self.main_menu()

    def settings(self):
        os.system('cls' if platform.system() == 'Windows' else 'clear')
        print("Settings")
        print("ASCII gear")
        time.sleep(5)
        self.main_menu()

    def quit_game(self):
        os.system('cls' if platform.system() == 'Windows' else 'clear')
        print("Goodbye!")
        time.sleep(2)

    def clear_screen(self):
        os.system('cls' if platform.system() == 'Windows' else 'clear')


game = Game()
