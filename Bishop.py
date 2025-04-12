from ChessPiece import ChessPiece

class Bishop(ChessPiece):
    """
    Defines attributes and methods surrounding the Bishop piece.
    """

    def __init__(self, color, position):
        """Inherits common attributes for chess pieces and initializes unique attributes to the Bishop."""

        super().__init__(color, position)
        self._name = 'B'

    def get_name(self):
        """
        Returns the _name private data member initialized and tracked in this object class.
        """
        return self._name

    def get_chess_piece_moves(self, board_obj):
        """
        Calculates the legal moves for a Bishop and returns those possible moves for comparison elsewhere.
        :param board_obj: The board object (list) containing sub-lists (chess board rows) whose indices contain
        the chess pieces currently at their respective positions on the board.
        :return: A list of legal moves for the Bishop to make.
        """

        # Retrieves the current column and row the Bishop is at
        column, row = self.get_row_and_column_from_position()
        row = int(row)

        # Creates lists to store the legal moves and positions which the Bishop could move to
        moves = []
        move_positions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        # Record the Bishop's legal moves
        for direction in move_positions:
            direction_row, direction_column = direction
            r_temp, c_temp = row + direction_row, ord(column) - 97 + direction_column

            while 1 <= r_temp <= 8 and 0 <= c_temp <= 7:
                if board_obj[-r_temp][c_temp] == '.':
                    moves.append(str(chr(c_temp + 97) + str(r_temp)))
                elif board_obj[-r_temp][c_temp].get_color() != self.get_color():
                    moves.append(str(chr(c_temp + 97) + str(r_temp)))
                    break
                else:
                    break

                r_temp += direction_row
                c_temp += direction_column

        # Returns the list of legal moves for the Bishop object
        return moves