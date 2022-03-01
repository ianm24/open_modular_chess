# Open Modular Chess
The idea behind this project is making a version of chess where anyone can test out their own ideas for new pieces, board sizes, as well as win and lose conditions.
This idea is still in its infancy, but its structure is well defined (and becoming more well-defined as it is developed).

The base set in `/sets/base_set` is an example of the file structure and specifications that are used to define the base rules of chess.

## How to Use
In a command window, go to the `src` directory and run `python3 open_modular_chess_core/main.py`

## Making a Set
### Board Specification
TODO
(note: p0 is any non-player piece)
### Win Condition Specification
TODO
### Lose Condition Specification
TODO
### Piece Specification
TODO
### Script Specification
TODO

### Set Validation
Order of validation:
 * pieces csv
 * pieces scripts
 * board
 * win
 * lose

## Testing
Tests are located in the `src/tests` directory. Test files follow the naming scheme `test_{name_of_file_tested}`. Test classes follow the naming scheme `Test{NameOfMethodBeingTested}` and each test follows the naming scheme `test_{description_of_test}`. 

Some tests require specific set conditions, these sets can be found in `sets/test_sets` and follow the naming scheme `test_set_{description_of_test}` where the description_of_test is the same as the testing method that uses the set.

To run all the tests, in a command window go to the `src` directory and run `python3 -m unittest -v`.

## Repo Structure
```
open-modular-chess  
│   README.md (This Document)
│   LICENSE (Standard MIT License)
└───src
|   └───open_modular_chess_core
|   |       __init__.py (Package Managing)
|   |       load_set.py (Used for loading sets into play)
|   |       main.py (The main program)
|   └───tests
|   |       __init__.py (Package Managing)
|   |       test_load_set.py (Fully tests the load_set.py code)
└───sets
│   └───base_set
│   |   │   board.csv (8x8 Board with standard piece layout)
│   |   │   lose.py (Defines the losing state (lose king or get checkmated))
│   |   │   win.py (Defines the winning state (take king or checkmate opponent))
│   |   └───pieces
│   |   |       bishop.csv (Standard bishop piece)
│   |   |       king.csv (Standard king piece)
│   |   |       knight.csv (Standard knight piece)
│   |   |       pawn.csv (Standard pawn piece)
│   |   |       queen.csv (Standard queen piece)
│   |   |       rook.csv (Standard rook piece)
│   |   └───scripts
│   |   |       castle.py (Code for standard castling)
│   |   |       en_passant.py (Code for standard en_passant)
│   └───test_sets (See above section for details)

```

## Credits
Started by Ian McDowell September 2021