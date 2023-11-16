import pytest

from omc.core import load_set

'''Pawn Class Tests'''


@pytest.fixture
def base_board():
    """
    Returns a Board with the base set
    """
    base_piece_map = load_set.get_piece_map('base_set')
    b = load_set.get_board('base_set', base_piece_map)
    p1 = b.get_player(1)
    p2 = b.get_player(2)
    p1.update_threatened_spaces()
    p2.update_threatened_spaces()
    return b


def test_pawn_moves(base_board):
    """
    Ensures proper moves available for a pawn
    """

    b = base_board

    p = b.query_space((0, 1))

    expected_first_moves = [(0, 2), (0, 3)]
    actual_first_moves = p.list_moves()

    p.move((0, 2))

    expected_second_moves = [(0, 3)]
    actual_second_moves = p.list_moves()

    p.move((0, 3))
    p.move((0, 4))

    # Move enemy pawn to block
    b.query_space((0, 6)).move((0, 5))

    expected_blocked_moves = []
    actual_blocked_moves = p.list_moves()

    # Block a first-move pawn
    p2 = b.query_space((1, 6))
    p2.move((1, 5))
    p2.move((1, 4))
    p2.move((1, 3))
    p2.move((1, 2))

    expected_first_blocked_moves = []
    actual_first_blocked_moves = b.query_space((1, 1)).list_moves()

    assert actual_first_moves == expected_first_moves
    assert actual_second_moves == expected_second_moves
    assert actual_blocked_moves == expected_blocked_moves
    assert actual_first_blocked_moves == expected_first_blocked_moves


def test_pawn_capture_moves(base_board):
    """
    Ensures proper moves available for a pawn with capture choices
    """

    b = base_board

    p1 = b.query_space((1, 1))
    p1.move((1, 2))
    p1.move((1, 3))
    p1.move((1, 4))

    p2 = b.query_space((2, 6))
    p2.move((2, 5))

    p3 = b.query_space((0, 6))
    p3.move((0, 5))

    expected_moves = [(1, 5), (2, 5), (0, 5)]

    assert p1.list_moves() == expected_moves


def test_pawn_capture(base_board):
    """
    Ensures proper functionality when a pawn captures a piece
    """

    b = base_board

    p1 = b.query_space((1, 1))
    p1.move((1, 2))
    p1.move((1, 3))

    p2 = b.query_space((2, 6))
    p2.move((2, 5))
    p2.move((2, 4))

    expected_coords = (2, 4)

    p1.move((2, 4))

    assert p1.current_coords == expected_coords
    assert b.query_space(expected_coords) == p1
    assert p2.current_coords is None


@pytest.mark.xfail(reason="En passant not implemented yet")
def test_pawn_en_passant(base_board):
    """
    Ensures proper functionality when a pawn can en passant
    """
    # TODO

    b = base_board

    p1 = b.query_space((1, 1))
    p1.move((1, 2))
    p1.move((1, 3))
    p1.move((1, 4))

    p2 = b.query_space((2, 6))
    p2.move((2, 4))

    expected_coords = (2, 3)

    move_success = p1.move((2, 3))

    assert move_success is True
    assert p1.current_coords == expected_coords
    assert b.query_space(expected_coords) == p1
    assert p2.current_coords is None


@pytest.fixture
def pawn_promotion_board(base_board):
    """
    Returns a board with a ready-to-promote pawn
    """
    b = base_board

    p1 = b.query_space((1, 1))
    p1.move((1, 2))
    p1.move((1, 3))

    p2 = b.query_space((2, 6))
    p2.move((2, 5))
    p2.move((2, 4))

    p1.move((2, 4))
    p1.move((2, 5))
    p1.move((2, 6))

    return [b, p1]


@pytest.mark.xfail(reason="User-chosen promotion not implemented")
def test_pawn_promote_queen(pawn_promotion_board):
    """
    Ensures proper functionality when pawn promotes
    """
    b, p1 = pawn_promotion_board
    p1.move((1, 7))
    # User input to select promotion

    expected_coords = None
    expected_piece_char = "Q"
    actual_piece = b.query_space((1, 7))

    assert p1.current_coords == expected_coords
    assert actual_piece != p1
    assert actual_piece.piece_char == expected_piece_char


@pytest.mark.xfail(reason="User-chosen promotion not implemented")
def test_pawn_promote_knight(pawn_promotion_board):
    """
    Ensures proper functionality when pawn promotes
    """
    b, p1 = pawn_promotion_board
    p1.move((1, 7))
    # TODO User input to select promotion

    expected_coords = None
    expected_piece_char = "K"
    actual_piece = b.query_space((1, 7))

    assert p1.current_coords == expected_coords
    assert actual_piece != p1
    assert actual_piece.piece_char == expected_piece_char


@pytest.mark.xfail(reason="User-chosen promotion not implemented")
def test_pawn_promote_bishop(pawn_promotion_board):
    """
    Ensures proper functionality when pawn promotes
    """
    b, p1 = pawn_promotion_board
    p1.move((1, 7))
    # TODO User input to select promotion

    expected_coords = None
    expected_piece_char = "B"
    actual_piece = b.query_space((1, 7))

    assert p1.current_coords == expected_coords
    assert actual_piece != p1
    assert actual_piece.piece_char == expected_piece_char


@pytest.mark.xfail(reason="User-chosen promotion not implemented")
def test_pawn_promote_rook(pawn_promotion_board):
    """
    Ensures proper functionality when pawn promotes
    """
    b, p1 = pawn_promotion_board
    p1.move((1, 7))
    # TODO User input to select promotion

    expected_coords = None
    expected_piece_char = "R"
    actual_piece = b.query_space((1, 7))

    assert p1.current_coords == expected_coords
    assert actual_piece != p1
    assert actual_piece.piece_char == expected_piece_char


'''Knight Class Tests'''


def test_knight_moves(base_board):
    """
    Ensures proper moves available for a knight
    """

    b = base_board

    n = b.query_space((1, 0))

    expected_first_moves = [(2, 2), (0, 2)]
    actual_first_moves = n.list_moves()

    n.move((2, 2))

    expected_second_moves = [(4, 3), (3, 4), (1, 4), (0, 3), (1, 0)]
    actual_second_moves = n.list_moves()

    n.move((3, 4))

    expected_moves = [(5, 5), (4, 6), (2, 6), (1, 5), (1, 3), (2, 2), (4, 2),
                      (5, 3)]
    actual_moves = n.list_moves()

    assert actual_first_moves == expected_first_moves
    assert actual_second_moves == expected_second_moves
    assert actual_moves == expected_moves


def test_knight_capture(base_board):
    """
    Ensures proper function when a knight captures a piece
    """

    b = base_board

    n = b.query_space((1, 0))
    n.move((2, 2))
    n.move((3, 4))
    n.move((4, 6))

    expected_coords = (4, 6)

    assert n.current_coords == expected_coords
    assert b.query_space(expected_coords) == n


'''Bishop Class Tests'''


def test_bishop_moves(base_board):
    """
    Ensures proper moves available for a bishop
    """

    b = base_board

    bishop = b.query_space((2, 0))

    # Move pawn out of bishop's way
    b.query_space((3, 1)).move((3, 3))

    expected_first_moves = [(3, 1), (4, 2), (5, 3), (6, 4), (7, 5)]
    actual_first_moves = bishop.list_moves()

    bishop.move((5, 3))

    expected_moves = [(6, 4), (7, 5), (4, 4), (3, 5),
                      (2, 6), (4, 2), (3, 1), (2, 0), (6, 2)]
    actual_moves = bishop.list_moves()

    assert expected_first_moves == actual_first_moves
    assert expected_moves == actual_moves


def test_bishop_capture(base_board):
    """
    Ensures proper function when a bishop captures a piece
    """

    b = base_board

    # Move pawn out of bishop's way
    b.query_space((3, 1)).move((3, 3))

    bishop = b.query_space((2, 0))
    bishop.move((5, 3))
    bishop.move((2, 6))

    expected_coords = (2, 6)

    assert bishop.current_coords == expected_coords
    assert b.query_space(expected_coords) == bishop


'''Rook Class Tests'''


def test_rook_moves(base_board):
    """
    Ensures proper moves available for a rook
    """

    b = base_board

    r = b.query_space((0, 0))

    # Move pawn out of rook's way
    b.query_space((0, 1)).move((0, 3))

    expected_first_moves = [(0, 1), (0, 2)]
    actual_first_moves = r.list_moves()

    r.move((0, 2))

    expected_second_moves = [(1, 2), (2, 2), (3, 2),
                             (4, 2), (5, 2), (6, 2), (7, 2), (0, 1), (0, 0)]
    actual_second_moves = r.list_moves()

    r.move((4, 2))
    r.move((4, 4))

    expected_moves = [(5, 4), (6, 4), (7, 4), (3, 4), (2, 4),
                      (1, 4), (0, 4), (4, 3), (4, 2), (4, 5), (4, 6)]
    actual_moves = r.list_moves()

    assert expected_first_moves == actual_first_moves
    assert expected_second_moves == actual_second_moves
    assert expected_moves == actual_moves


def test_rook_capture(base_board):
    """
    Ensures proper function when a rook captures a piece
    """

    b = base_board

    r = b.query_space((0, 0))

    # Move pawn out of rook's way
    b.query_space((0, 1)).move((0, 3))

    r.move((0, 2))
    r.move((4, 2))
    r.move((4, 4))
    r.move((4, 6))

    expected_coords = (4, 6)

    assert r.current_coords == expected_coords
    assert b.query_space(expected_coords) == r


'''Queen Class Tests'''


def test_queen_moves(base_board):
    """
    Ensures proper moves available for a queen
    """

    b = base_board

    q = b.query_space((4, 0))

    # Move pawn out of queen's way
    p = b.query_space((4, 1))
    p.move((4, 3))
    p.move((4, 4))
    p.move((4, 5))
    p.move((3, 6))

    expected_first_moves = [(4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6)]
    actual_first_moves = q.list_moves()

    q.move((4, 4))

    expected_moves = [(5, 4), (6, 4), (7, 4), (5, 5), (6, 6), (4, 5), (4, 6),
                      (3, 5), (2, 6), (3, 4), (2, 4), (1, 4), (0, 4), (3, 3),
                      (2, 2), (4, 3), (4, 2), (4, 1), (4, 0), (5, 3), (6, 2)]
    actual_moves = q.list_moves()

    assert expected_first_moves == actual_first_moves
    assert expected_moves == actual_moves


def test_queen_capture(base_board):
    """
    Ensures proper function when a queen captures a piece
    """

    b = base_board

    q = b.query_space((4, 0))

    # Move pawn out of queen's way
    p = b.query_space((4, 1))
    p.move((4, 3))
    p.move((4, 4))
    p.move((4, 5))
    p.move((3, 6))

    q.move((4, 6))

    expected_coords = (4, 6)

    assert q.current_coords == expected_coords
    assert b.query_space(expected_coords) == q


'''King Class Tests'''


def test_king_moves(base_board):
    """
    Ensures proper moves available for a king
    """

    b = base_board

    k = b.query_space((3, 0))

    # Move pawn out of king's way
    p = b.query_space((3, 1))
    p.move((3, 3))
    p.move((3, 4))
    p.move((3, 5))
    p.move((4, 6))

    expected_first_moves = [(3, 1)]
    actual_first_moves = k.list_moves()

    k.move((3, 1))
    k.move((3, 2))
    k.move((3, 3))
    k.move((3, 4))

    expected_moves = [(4, 4), (2, 4), (2, 3), (3, 3), (4, 3)]
    actual_moves = k.list_moves()

    assert expected_first_moves == actual_first_moves
    assert expected_moves == actual_moves


def test_king_capture(base_board):
    """
    Ensures proper function when a king captures a piece
    """

    b = base_board

    k = b.query_space((3, 0))

    # Move pawn out of king's way
    p1 = b.query_space((3, 1))
    p1.move((3, 3))
    p1.move((3, 4))
    p1.move((3, 5))
    p1.move((4, 6))

    # Move enemy pawn for king capture
    p2 = b.query_space((3, 6))
    p2.move((3, 4))

    k.move((3, 1))
    k.move((3, 2))
    k.move((3, 3))
    k.move((3, 4))

    expected_coords = (3, 4)

    assert k.current_coords == expected_coords
    assert b.query_space(expected_coords) == k


@pytest.fixture
def castling_board(base_board):
    """
    Returns a board where a king can castle
    """

    b = base_board

    # Move Knights
    b.query_space((1, 0)).move((2, 2))
    b.query_space((6, 0)).move((5, 2))

    # Move Pawns
    b.query_space((3, 1)).move((3, 3))
    b.query_space((4, 1)).move((4, 3))

    # Move Bishops
    b.query_space((2, 0)).move((5, 3))
    b.query_space((5, 0)).move((2, 3))

    # Move Queen
    b.query_space((4, 0)).move((4, 1))

    return b


@pytest.mark.xfail(reason="Castling not implemented yet")
def test_king_castle_king_side(castling_board):
    """
    Ensures proper function when king castles to the king side rook
    """

    b = castling_board

    k = b.query_space((3, 0))
    r = b.query_space((0, 0))

    expected_moves = [(4, 0), (3, 1), (2, 0), (1, 0)]
    actual_moves = k.list_moves()

    success = k.move((1, 0))

    expected_king_coord = (1, 0)
    expected_rook_coord = (2, 0)

    assert expected_moves == actual_moves
    assert success is True
    assert k.current_coord == expected_king_coord
    assert r.current_coord == expected_rook_coord
    assert b.query_space(expected_king_coord) == k
    assert b.query_space(expected_rook_coord) == r


@pytest.mark.xfail(reason="Castling not implemented yet")
def test_king_castle_queen_side(castling_board):
    """
    Ensures proper function when king castles to the queen side rook
    """

    b = castling_board

    k = b.query_space((3, 0))
    r = b.query_space((7, 0))

    expected_moves = [(4, 0), (3, 1), (2, 0), (5, 0)]
    actual_moves = k.list_moves()

    success = k.move((5, 0))

    expected_king_coord = (5, 0)
    expected_rook_coord = (4, 0)

    assert expected_moves == actual_moves
    assert success is True
    assert k.current_coord == expected_king_coord
    assert r.current_coord == expected_rook_coord
    assert b.query_space(expected_king_coord) == k
    assert b.query_space(expected_rook_coord) == r


'''ChessPlayer Tests'''


def test_chess_player_set_check(base_board):
    """
    Ensures proper function when chess player's check status is set
    """

    b = base_board
    p = b.get_player(1)

    p.set_check(True)

    assert p.in_check is True


def test_chess_player_update_threatened_spaces(base_board):
    """
    Ensures proper function when chess player updates threatened spaces
    """

    b = base_board
    p = b.get_player(1)

    expected_starting_area = [
        (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2)]
    actual_starting_area = p.threatened_spaces

    # Move pawn
    b.query_space((1, 1)).move((1, 2))
    p.update_threatened_spaces()

    expected_area = [(0, 2), (0, 3), (1, 1), (1, 2), (2, 2),
                     (2, 3), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2)]
    actual_area = p.threatened_spaces

    assert sorted(actual_starting_area) == expected_starting_area
    assert sorted(actual_area) == expected_area


@pytest.fixture
def check_board(base_board):
    """
    Returns a board where player 1 is in check
    """
    b = base_board

    k = b.query_space((3, 0))

    # Move pawn out of king's way
    p1 = b.query_space((3, 1))
    p1.move((3, 3))
    p1.move((3, 4))
    p1.move((3, 5))
    p1.move((4, 6))

    # Move enemy pawn for king capture
    p2 = b.query_space((3, 6))
    p2.move((3, 4))

    k.move((3, 1))
    k.move((2, 2))
    k.move((2, 3))

    p2.move((3, 2))

    return b


def test_chess_player_update_threatened_spaces_sets_check(check_board):
    """
    Ensures proper function when chess player updates threatened spaces after
    putting other player in check
    """
    b = check_board
    b.get_player(2).update_threatened_spaces()

    assert b.get_player(1).in_check is True


@pytest.mark.xfail(reason="Move limiting for check not implemented yet")
def test_moves_in_check(check_board):
    """
    Ensures proper function when a player is in check
    """

    b = check_board

    k = b.query_space((3, 0))

    # Move pawn out of king's way
    p = b.query_space((3, 1))
    p.move((3, 3))
    p.move((3, 4))
    p.move((3, 5))
    p.move((4, 6))

    k.move((3, 1))
    k.move((3, 2))
    k.move((3, 3))
    k.move((2, 4))

    # Move Knight and Queen for check
    b.query_space((1, 7)).move((0, 5))
    q = b.query_space((4, 7))
    q.move((4, 6))
    q.move((4, 5))

    expected_first_moves = [(1, 4), (1, 3), (3, 3)]
    actual_first_moves = k.list_moves()

    assert actual_first_moves == expected_first_moves


@pytest.mark.xfail(reason="Test not implemented")
def test_chess_player_lose_condition():
    """
    Ensures proper function when chess player checks lose condition
    """

    assert False is True


@pytest.mark.xfail(reason="Test not implemented")
def test_chess_player_win_condition():
    """
    Ensures proper function when chess player checks win condition
    """

    assert False is True
