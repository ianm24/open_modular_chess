# Open Modular Chess
The idea behind this project is making a version of chess where anyone can test out their own ideas for new pieces, board sizes, as well as win and lose conditions.
This idea is still in its infancy, but its structure is well defined (and becoming more well-defined as it is developed).

The base set in `/sets/base_set` is an example of the file structure and specifications that are used to define the base rules of chess.

## How to Use
TODO

## Making a Set
### Board Specification
TODO
### Win Condition Specification
TODO
### Lose Condition Specification
TODO
### Piece Specification
TODO
### Script Specification
TODO

## Repo Structure
```
open-modular-chess  
│   README.md (This Document)
│   LICENSE (Standard MIT License)
└───core
│   │   load_set.py (Used for loading sets into play)
└───sets
│   └───base_set
│       │   board.csv (8x8 Board with standard piece layout)
│       │   lose.py (Defines the losing state (lose king or get checkmated))
│       │   win.py (Defines the winning state (take king or checkmate opponent))
│       └───pieces
│       │   bishop.csv (Standard bishop piece)
│       │   king.csv (Standard king piece)
│       │   knight.csv (Standard knight piece)
│       │   pawn.csv (Standard pawn piece)
│       │   queen.csv (Standard queen piece)
│       │   rook.csv (Standard rook piece)
│       └───scripts
│       │   castle.py (Code for standard castling)
│       │   en_passant.py (Code for standard en_passant)

```

## Credits
Started by Ian McDowell September 2021