import pytest

from omc.core import load_set

'''Pawn Class Tests'''


def test_list_first_moves_pawn():
    """
    Ensures proper moves available for a pawn's first move
    """

    base_piece_map = load_set.get_piece_map('base_set')
    b = load_set.get_board('base_set', base_piece_map)

    p = b.query_space((0, 1))

    expected_moves = [(0, 2), (0, 3)]

    assert p.list_moves() == expected_moves


def test_list_second_moves_pawn():
    """
    Ensures proper moves available for a pawn's second move
    """

    base_piece_map = load_set.get_piece_map('base_set')
    b = load_set.get_board('base_set', base_piece_map)

    p = b.query_space((0, 1))
    p.move((0, 2))

    expected_moves = [(0, 3)]

    assert p.list_moves() == expected_moves


def test_list_blocked_moves_pawn():
    """
    Ensures proper moves available for a blocked pawn
    """

    base_piece_map = load_set.get_piece_map('base_set')
    b = load_set.get_board('base_set', base_piece_map)

    p1 = b.query_space((0, 1))
    p1.move((0, 2))
    p1.move((0, 3))
    p1.move((0, 4))

    p2 = b.query_space((0, 6))
    p2.move((0, 5))

    expected_moves = []

    assert p1.list_moves() == expected_moves


def test_list_capture_moves_pawn():
    """
    Ensures proper moves available for a pawn with capture choices
    """
    base_piece_map = load_set.get_piece_map('base_set')
    b = load_set.get_board('base_set', base_piece_map)

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


def test_pawn_capture():
    """
    Ensures proper functionality when a pawn captures a piece
    """
    base_piece_map = load_set.get_piece_map('base_set')
    b = load_set.get_board('base_set', base_piece_map)

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


@pytest.fixture
def pawn_promotion_board():
    """
    Returns a board with a ready-to-promote pawn
    """
    base_piece_map = load_set.get_piece_map('base_set')
    b = load_set.get_board('base_set', base_piece_map)

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
