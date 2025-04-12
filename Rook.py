from ChessPiece import ChessPiece

class Rook(ChessPiece):
    """
    Defines attributes and methods surrounding the Rook piece.
    """

    def __init__(self, color, position):
        """Inherits common attributes for chess pieces and initializes unique attributes to the Rook."""

        super().__init__(color, position)
        self._name = 'R'

    def get_name(self):
        """
        Returns the _name private data member initialized and tracked in this object class.
        """
        return self._name

    def get_chess_piece_moves(self, board_obj):
        """
        Calculates the legal moves for a Rook and returns those possible moves for comparison elsewhere.
        :param board_obj: The board object (list) containing sub-lists (chess board rows) whose indices contain
        the chess pieces currently at their respective positions on the board.
        :return: A list of legal moves for the Rook to make.
        """

        # Retrieves the current column and row the Rook is at
        column, row = self.get_row_and_column_from_position()
        row = int(row)

        # Creates a blank list to store the legal moves and determines the direction of movement from piece color
        moves = []

        # Down, up, right and left, respectively (row, column)
        move_positions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # Record that the Rook can move anywhere up, down, left or right in one direction until it is blocked
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

        # Returns the list of legal moves for the Rook object
        return moves