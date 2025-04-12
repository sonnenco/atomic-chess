from ChessPiece import ChessPiece
from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Queen import Queen
from King import King

class Pawn(ChessPiece):
    """
    Defines attributes and methods surrounding the Pawn piece.
    """

    def __init__(self, color, position):
        """Inherits common attributes for chess pieces and initializes unique attributes to the Pawn."""

        super().__init__(color, position)
        self._name = 'P'

    def get_name(self):
        """
        Returns the _name private data member initialized and tracked in this object class.
        """
        return self._name

    def get_chess_piece_moves(self, board_obj):
        """
        Calculates the legal moves for a Pawn and returns those possible moves for comparison elsewhere.
        :param board_obj: The board object (list) containing sub-lists (chess board rows) whose indices contain
        the chess pieces currently at their respective positions on the board.
        :return: A list of legal moves for the Pawn to make.
        """

        # Retrieves the current column and row the Pawn is at
        column, row = self.get_row_and_column_from_position()
        row = int(row)

        # Creates a blank list to store the legal moves and determines the direction of movement from piece color
        moves = []
        direction = 1 if self._color == 'white' else -1

        # Standard move is one square forward for a Pawn
        if 1 <= row + direction <= 8 and board_obj[-(row + direction)][ord(column) - 97] == '.':
            moves.append(column + str(row + direction))

            # Pawn can move two squares forward on it's first move (if that is requested)
            if ((self.get_color() == 'white' and row == 2) or (self.get_color() == 'black' and row == 7)
                    and self.get_chess_piece_turn_counter() == 0):
                if board_obj[-(row + 2 * direction)][ord(column) - 97] == '.':
                    moves.append(column + str(row + 2 * direction))

        # Returns the list of legal moves for the Pawn object
        return moves

    def get_chess_piece_captures(self, board_obj):
        """
        Because the Pawn is the only chess piece which moves and captures separately, this additional method
        is built for the Pawn class to denote positions which can be captured on the board (diagonally forward
        left and right by one space).
        :param board_obj: Object containing the contents of the atomic chess board.
        :return: A list of legal captures for the Pawn to make.
        """
        # Retrieves the current column and row the Pawn is at
        column, row = self.get_row_and_column_from_position()
        row = int(row)

        # Creates a blank list to store the legal captures and determines the direction of movement from piece color
        captures = []
        direction = 1 if self._color == 'white' else -1

        # Finds the board locations which the Pawn can capture (diagonally forward left and right one square)
        if direction == 1:
            if 0 <= ord(column) - 98 <= 7 and isinstance(board_obj[-(row + direction)][ord(column) - 98],
                                                         (ChessPiece, Pawn, Rook, Knight, Bishop, Queen, King)):
                diagonal_forward_left = chr(ord(column) - 1) + str(row + 1)
                captures.append(diagonal_forward_left)

            if 0 <= ord(column) - 96 <= 7 and isinstance(board_obj[-(row + direction)][ord(column) - 96],
                                                         (ChessPiece, Pawn, Rook, Knight, Bishop, Queen, King)):
                diagonal_forward_right = chr(ord(column) + 1) + str(row + 1)
                captures.append(diagonal_forward_right)

        else:
            if isinstance(board_obj[-(row + direction)][ord(column) - 96],
                          (ChessPiece, Pawn, Rook, Knight, Bishop, Queen, King)):
                diagonal_forward_left = chr(ord(column) + 1) + str(row - 1)
                captures.append(diagonal_forward_left)

            if isinstance(board_obj[-(row + direction)][ord(column) - 98],
                          (ChessPiece, Pawn, Rook, Knight, Bishop, Queen, King)):
                diagonal_forward_right = chr(ord(column) - 1) + str(row - 1)
                captures.append(diagonal_forward_right)

        # Returns the list of legal captures for the Pawn object
        return captures