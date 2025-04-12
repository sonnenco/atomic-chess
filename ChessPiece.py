class ChessPiece:
    """
    Defines common attributes and methods for chess pieces.
    """

    def __init__(self, color, position):
        """
        Defines common attributes for chess pieces.
        """
        self._name = ''
        self._color = color
        self._position = position
        self._chess_piece_turn_counter = 0

    def get_color(self):
        """
        Returns the _color private data member initialized and tracked in this ChessPiece object.
        """
        return self._color

    def get_chess_piece_turn_counter(self):
        """
        Returns the _chess_piece_turn_counter private data member initialized and tracked in this ChessPiece object.
        """
        return self._chess_piece_turn_counter

    def get_row_and_column_from_position(self):
        """
        Finds the row and column on the atomic chess board of the ChessPiece object (algebraic notation).
        :return: list_of_column_and_row
        """

        row = self._position[1]
        column = self._position[0]
        list_of_column_and_row = [column, row]
        return list_of_column_and_row

    def set_position(self, new_position):
        """
        Sets a new position for a ChessPiece object as it moves around the atomic chess board.
        :param new_position: Position that the ChessPiece object now is positioned in.
        """
        self._position = new_position