class AbstractOpenModularChessException(Exception):
    """Base class for all Open Module Chess Exceptions"""


class SetNotFoundException(AbstractOpenModularChessException):
    """Specified set not found in the sets directory"""


class PiecesNotFoundException(AbstractOpenModularChessException):
    """Specified set not found in the sets directory"""


class PiecesEmptyException(AbstractOpenModularChessException):
    """Specified set not found in the sets directory"""


class BoardNotFoundException(AbstractOpenModularChessException):
    """Specified set not found in the sets directory"""


class EmptyBoardException(AbstractOpenModularChessException):
    """Specified set not found in the sets directory"""


class InvalidBoardFormatException(AbstractOpenModularChessException):
    """"""


class InvalidBoardLayoutException(AbstractOpenModularChessException):
    """Specified set not found in the sets directory"""


class InvalidBoardDimensionException(AbstractOpenModularChessException):
    """Specified set not found in the sets directory"""


class BoardValidationFailedException(AbstractOpenModularChessException):
    """Specified set not found in the sets directory"""
