from ChessPiece import ChessPiece

class King(ChessPiece):
    """
    Defines attributes and methods surrounding the King piece.
    """

    def __init__(self, color, position):
        """Inherits common attributes for chess pieces and initializes unique attributes to the King."""

        super().__init__(color, position)
        self._name = 'K'

    def get_name(self):
        """
        Returns the _name private data member initialized and tracked in this object class.
        """
        return self._name

    def get_chess_piece_moves(self, board_obj):
        """
        Calculates the legal moves for a King and returns those possible moves for comparison elsewhere.
        :param board_obj: The board object (list) containing sub-lists (chess board rows) whose indices contain
        the chess pieces currently at their respective positions on the board.
        :return: A list of legal moves for the King to make.
        """

        # Retrieves the current column and row the King is at
        column, row = self.get_row_and_column_from_position()
        row = int(row)

        # Creates lists to store the legal moves and positions which the King could move to
        moves = []
        move_positions = [
            (1, 0), (1, 1), (0, 1), (-1, 1),
            (-1, 0), (-1, -1), (0, -1), (1, -1)
        ]

        # Record the King's legal moves
        for direction_row, direction_column in move_positions:
            r_temp, c_temp = row + direction_row, ord(column) - 97 + direction_column
            if 1 <= r_temp <= 8 and 0 <= c_temp <= 7:
                if board_obj[-r_temp][c_temp] == '.' or board_obj[-r_temp][c_temp].get_color() != self.get_color():
                    moves.append(str(chr(c_temp + 97) + str(r_temp)))

        # Returns the list of legal moves for the King object
        return moves