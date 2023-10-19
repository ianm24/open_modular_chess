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
    """CSV Reader failed to parse the file format"""


class InvalidBoardLayoutException(AbstractOpenModularChessException):
    """Specified set not found in the sets directory"""


class InvalidBoardDimensionException(AbstractOpenModularChessException):
    """Specified set not found in the sets directory"""


class BoardValidationFailedException(AbstractOpenModularChessException):
    """Specified set not found in the sets directory"""


class MissingPieceCharException(AbstractOpenModularChessException):
    """Piece character missing for piece"""


class PiecePixelHexOutOfBoundsException(AbstractOpenModularChessException):
    """Piece pixel-hex value out of bounds for piece"""


class NegativePiecePlayerNumException(AbstractOpenModularChessException):
    """Player controller set to negative value"""


class NegativePieceCoordinatesException(AbstractOpenModularChessException):
    """Piece coordinates set to negative value"""


class NonCurrentPiecePlayerNumException(AbstractOpenModularChessException):
    """Piece player controller set to a non-current player"""


class PieceSubclassInvalidException(AbstractOpenModularChessException):
    """Subclassing of Piece object is invalid or incomplete"""


class PieceAlreadyAtLocationException(AbstractOpenModularChessException):
    """Piece attempted to place on top of other piece without replacement"""
