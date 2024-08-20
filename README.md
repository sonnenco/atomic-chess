# ⚛️ Atomic Chess ♟️

[Atomic Chess (Wikipedia)](https://en.wikipedia.org/wiki/Atomic_chess) is a two-player variant of traditional chess, played in the terminal. This version of the game introduces explosive twists and fast-paced strategy, offering a unique chess experience right from your command line.

### Table of Contents

1. [Installation and Dependencies](#installation-and-dependencies)
2. [How to Play](#how-to-play)
3. [Architecture](#architecture)

## Installation and Dependencies

To get started with Atomic Chess, you need to have Python installed on your system. You can clone the repository and install any necessary dependencies.

#### Prerequisites:

    Python 3.6 or higher
    Git (optional, for cloning the repository)
    [Termcolor](https://pypi.org/project/termcolor/)

#### Clone this repository using Git:

```bash
git clone https://github.com/sonnenco/atomic-chess.git
cd atomic-chess
```

## How to Play

To start a game of Atomic Chess, simply run the Python script:

#### Windows:
```bash
py ChessVar.py
```
#### Cross-Platform:
```bash
python3 ChessVar.py
```

Follow the on-screen instructions to play the game. Both players take turns entering their moves in standard chess notation.

### Game Rules

Atomic Chess follows most of the traditional rules of chess but with a key difference:

    Explosions: When a piece (except for pawns) captures another piece, an explosion occurs. The explosion destroys the capturing piece, the captured piece, and all adjacent pieces (including pawns), except for kings.
    Checkmate: Unlike traditional chess, delivering checkmate does not end the game. The goal is to capture the opponent's king via an explosion.
    Pawns: Pawns are not affected by the explosive effects but still capture and move as in standard chess.

## Architecture

#### class ChessVar:
* Initializes board for gameplay.
* Provides get methods for _game_state and _player_turn.
* Method make_move (and sub-methods) determine if moves are legal and executes them (if move is not legal, or the piece does not belong to the player whose turn it is, or the move would break the rules of atomic chess, disallows the move and prints error to terminal).
    
#### class ChessPiece:
* Defines parent attributes (e.g., name, color, position) and methods for all pieces.

#### class Pawn, Rook, Knight, Bishop, Queen, King:
* Defines unique attributes and methods for specific pieces (e.g., legal moves for     specific pieces, or for Pawns specifically, the diagonal capture separate from moves).

#### def main():
* Initiates the game and maintains gameplay until game state indicates a winner.

