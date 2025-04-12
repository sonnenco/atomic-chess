# Author: Colin Sonnenberg
# GitHub username: sonnenco

from ChessPiece import ChessPiece
from Pawn import Pawn
from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Queen import Queen
from King import King

from termcolor import colored, cprint

class AtomicChess:
    """An abstract board game that is a variant of chess called 'atomic chess.'
    See README.md for long-description of the game's requirements."""

    def __init__(self):
        """
        Initialization method for the match of atomic chess.
        """
        self._board = []
        self._game_state = 'UNFINISHED'
        self._list_of_columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self._list_of_rows = [1, 2, 3, 4, 5, 6, 7, 8]
        self._player_turn = 'white'

        # Create blank lists which will be filled with the starting front and back rows for each side.
        initial_black_back, initial_black_front, initial_white_back, initial_white_front = ([] for _ in range(4))

        # Dictionary which stores the order of the front + back rows of pieces for white and black
        map_of_pieces = {
            1: Rook,
            2: Knight,
            3: Bishop,
            4: Queen,
            5: King,
            6: Bishop,
            7: Knight,
            8: Rook
        }

        # Generates the front and back rows using map_of_pieces
        colors = ['black', 'white']
        for color in colors:
            for index in range(8):
                column = index + 1
                if color == 'black':
                    initial_black_front.append(Pawn(color, self._list_of_columns[index] + '7'))
                    type_of_piece = map_of_pieces[column]
                    initial_black_back.append(type_of_piece(color, self._list_of_columns[index] + '8'))
                if color == 'white':
                    initial_white_front.append(Pawn(color, self._list_of_columns[index] + '2'))
                    type_of_piece = map_of_pieces[column]
                    initial_white_back.append(type_of_piece(color, self._list_of_columns[index] + '1'))

        # Fills out the starting board using the respective variables filled above
        self._board = [
            initial_black_back,
            initial_black_front,
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            initial_white_front,
            initial_white_back
        ]

    def get_game_state(self):
        """
        Returns the game_state private data member initialized and tracked in this AtomicChess object.
        """
        return self._game_state

    def get_player_turn(self):
        """
        Returns the player_turn private data member initialized and tracked in this AtomicChess object.
        """
        return self._player_turn

    def make_move(self, current_position, requested_position):
        """
        Allows the player to make permissible moves on the atomic chess board.
        Unlike standard chess, there is no check or checkmate, no castling, en passant, or pawn promotion.
        :param current_position: Algebraic notation of a piece which the player would like to move.
        :param requested_position: Algebraic notation of a location the player would like to move the piece to.
        :return: True or False, depending on if this is a legal move based on the assignment requirements.
        """

        def find_piece_at_position(position):
            """
            Convert the position into a recognizable index in the self._board private data member.
            Returns the chess piece object found at the index (if applicable).  Otherwise, exceptions are raised.
            :param position: Algebraic position of a location on the atomic chess board.
            :return: ChessPiece-related object found at the requested position (if applicable).
            """

            # The position must adhere to the length of all chess positions (one letter + one number).
            if len(position) == 2:
                # Take both of the characters in the position argument and typecast for comparisons.
                current_row, current_column = int(position[1]), position[0].lower()

                # If the first character in the current_position argument is in the list of rows.
                # If the second character in the current_position argument is in the list of columns.
                if current_row in self._list_of_rows and current_column in self._list_of_columns:
                    # Find the row of the object being moved, then the specific object being moved.
                    row_of_obj = self._board[-current_row]
                    obj_being_moved = row_of_obj[ord(current_column) - 97]

                    # If the object is a from a user-defined ChessPiece or related class.
                    if isinstance(obj_being_moved, (ChessPiece, Pawn, Rook, Knight, Bishop, Queen, King)):
                        # Return the ChessPiece-related object being moved.
                        return obj_being_moved

        def find_pieces_impacted_by_explosion():
            """
            Finds the pieces which would be affected by an explosion in the 8 squares immediately surrounding
            the piece about to be captured in all directions.  This explosion will ultimately kill all pieces in
            its range except for Pawns.  Pawns can only be removed from the board when directly involved in a capture.
            :return: list_of_exploding_pieces
            """
            # Creates blank list of indices which would be impacted by a capturing explosion.
            list_of_exploding_indices = []

            # Determines the columns and rows immediately above and below the explosion's epicenter.
            requested_column, requested_row = requested_position[0], int(requested_position[1])
            left_col = chr(ord(requested_column) - 1)
            right_col = chr(ord(requested_column) + 1)
            row_up = str(requested_row + 1)
            row_down = str(requested_row - 1)

            # Append the eight surrounding positions (and middle position) to the list_of_exploding_indices
            list_of_exploding_indices.extend([left_col + row_down,
                                              left_col + str(requested_row),
                                              left_col + row_up])

            list_of_exploding_indices.extend([requested_column + row_down,
                                              requested_column + row_up])

            list_of_exploding_indices.extend([right_col + row_down,
                                              right_col + str(requested_row),
                                              right_col + row_up])

            # Creates blank list of objects impacted by the coming explosion
            list_of_exploding_pieces = []

            # For every position impacted by the coming explosion...
            for position in list_of_exploding_indices:
                # ... find the object which is stored at that position.
                temp_obj = find_piece_at_position(position)

                # ... and if that object is not None or a Pawn, append to the list_of_exploding_pieces.
                # Pawns are not affected by explosions per the assignment requirements.
                if temp_obj is not None and isinstance(temp_obj, Pawn) is False:
                    list_of_exploding_pieces.append(temp_obj)

            # Returns list of objects which would be impacted by a capturing explosion
            return list_of_exploding_pieces

        def initiate_move_on_board(piece_at_current_position, piece_at_position_being_moved_to):
            """
            Moves the piece_at_current_position to the requested position on the board.
            """
            # Retrieves the current_column and current_row
            current_column, current_row = current_position[0], int(current_position[1])

            # Sets the requested_column and requested_row from requested_position
            requested_column, requested_row = requested_position[0], int(requested_position[1])

            # Move piece_at_current_position to the requested position and update old position to '.'
            self._board[-requested_row][ord(requested_column) - 97] = piece_at_current_position
            piece_at_current_position.set_position(requested_position)
            self._board[-current_row][ord(current_column) - 97] = '.'

            # If a piece was captured by that move, it's explosion time!
            if isinstance(piece_at_position_being_moved_to, (ChessPiece, Pawn, Rook, Knight, Bishop, Queen, King)):
                
                print("\nCaptured piece at " + requested_position + "! (Explosion in surrounding 8 cells)")

                # If a Pawn captured a Pawn, both pieces are destroyed per the requirements
                # If a Pawn captured any other piece, the capturing Pawn is destroyed as well
                if isinstance(piece_at_current_position, Pawn):
                    self._board[-current_row][ord(current_column) - 97] = '.'
                    del piece_at_current_position

                self._board[-requested_row][ord(requested_column) - 97] = '.'

                # Checks if the captured piece was a King, and if so, designates the winner of the match
                if (isinstance(piece_at_position_being_moved_to, King) and
                        piece_at_position_being_moved_to.get_color() == 'white'):
                    self._game_state = 'BLACK_WON'

                if (isinstance(piece_at_position_being_moved_to, King) and
                        piece_at_position_being_moved_to.get_color() == 'black'):
                    self._game_state = 'WHITE_WON'

                del piece_at_position_being_moved_to

                # Remove any exploded (or the captured) piece(s) from the board and delete the piece objects
                for piece_impacted in list_of_pieces_impacted_by_explosion:
                    blown_up_column, blown_up_row = piece_impacted.get_row_and_column_from_position()
                    blow_up_row = int(blown_up_row)

                    # Removes the exploded piece from the board
                    self._board[-blow_up_row][ord(blown_up_column) - 97] = '.'

                    # Checks if the exploded / captured piece was a King (e.g., winning or losing move)
                    if isinstance(piece_impacted, King):
                        if piece_impacted.get_color() == 'white':
                            print("Black wins")
                            self._game_state = 'BLACK_WON'
                        elif piece_impacted.get_color() == 'black':
                            print("White wins")
                            self._game_state = 'WHITE_WON'

                    # Delete the ChessPiece-related object stored in the program's memory
                    del piece_impacted

        # Check to see if the game has already been won, if so return False
        if self._game_state != 'UNFINISHED':
            return False

        # Finds the pieces at current_position (if applicable)
        # If there is no piece_at_current_position, then output False
        piece_at_current_position = find_piece_at_position(current_position)
        if piece_at_current_position is None or piece_at_current_position == '.':
            print("No piece at that position - try agin.")
            return False

        # Check if the moving the piece belongs to the player whose turn it is
        # If the moving piece does not belong to the player, then output False
        if piece_at_current_position.get_color() != self._player_turn:
            print("That piece doesn't belong to player whose turn it is - try agin.")
            return False

        # Check to see if the requested move is legal
        legal_moves = piece_at_current_position.get_chess_piece_moves(self._board)
        if requested_position not in legal_moves:
            # Pawns are the only piece which Move vs Capture, so check if the requested position is a Capture instead
            if isinstance(piece_at_current_position, Pawn):
                legal_captures = piece_at_current_position.get_chess_piece_captures(self._board)
                # If the requested move is not a legal capture for the Pawn, return False
                if requested_position not in legal_captures:
                    print("That's not a legal move - try again.")
                    return False

            # If the piece_at_current_position is not a Pawn, return False
            else:
                print("That's not a legal move - try again.")
                return False

        # Record the piece at the requested position before a move is made
        piece_at_position_being_moved_to = find_piece_at_position(requested_position)

        # If the piece being moved is a King, and it would capture another piece, return False
        if (isinstance(piece_at_position_being_moved_to, (ChessPiece, Pawn, Rook, Knight, Bishop, Queen)) and
                isinstance(piece_at_current_position, King)):
            print("Kings are not allowed to capture other pieces - try again.")
            return False

        # Finds the pieces which would be impacted by an explosion
        list_of_pieces_impacted_by_explosion = find_pieces_impacted_by_explosion()

        # If the move would kill both Kings in one step, disallow this per requirements
        if isinstance(piece_at_position_being_moved_to, (ChessPiece, Pawn, Rook, Knight, Bishop, Queen)):
            king_counter = 0

            for piece in list_of_pieces_impacted_by_explosion:
                if isinstance(piece, King):
                    king_counter += 1

            if isinstance(piece_at_position_being_moved_to, King):
                king_counter += 1

            if king_counter == 2:
                print("This move would kill both Kings in one step, disallowed - try again.")
                return False

        # Initiates the move of the piece_at_current_position
        initiate_move_on_board(piece_at_current_position, piece_at_position_being_moved_to)

        # Updates the player_turn private data member to reflect the next player whose turn it is
        if self._player_turn == 'white':
            self._player_turn = 'black'
        elif self._player_turn == 'black':
            self._player_turn = 'white'

        # Made indicated move, removed any captured (exploded) pieces, updated whose turn it is, so returning True
        return True

    def print_board(self):
        """
        Prints the current state of the atomic chess board based on the positions
        of the pieces recorded in self._board private data member.
        """

        def print_border_letters():
            """
            Prints the letters (a through h) which are found on the top and bottom borders of the board.
            """
            print('  ', end='')
            for letters in self._list_of_columns:
                print(letters, end=' ')
            print('\n', end='')

        print('', end='\n')

        # Prints the top border of letters.
        print_border_letters()

        # Prints the inner contents of the board (e.g., all pieces / empty cells located within the 8x8 board).
        reverse_index_counter = -1
        for row in self._board:
            text_to_print = str(self._list_of_rows[reverse_index_counter])
            print(text_to_print, end=' ')

            for obj_at_index in row:
                if isinstance(obj_at_index, (Pawn, Rook, Knight, Bishop, Queen, King)):
                    if obj_at_index.get_color() == 'black':
                        text = colored(obj_at_index.get_name(), "black", "on_light_yellow", attrs=["bold"])
                        cprint(text, end=' ')
                    else:
                        text = colored(obj_at_index.get_name(), "white", "on_light_blue", attrs=["bold"])
                        cprint(text, end=' ')
                else:
                    text = colored(obj_at_index, "white")
                    print(text, end=' ')

            print('', end=text_to_print + '\n')
            reverse_index_counter -= 1

        # Prints the bottom border of letters.
        print_border_letters()

        print('', end='\n')

def main():
    game = AtomicChess()
    print("Welcome to Atomic Chess!\nWritten by github.com/sonnenco (2024)")

    while game.get_game_state() == 'UNFINISHED':
        game.print_board()
        print("It is " + game.get_player_turn() + "'s turn.")
        print("Cell to move from? (e.g., a1, d5)")
        current_space = input()
        print("Where to move?")
        requested_space = input()
        game.make_move(current_space, requested_space)

    print("\nWe have a winner! Final board:")
    game.print_board()

main()
