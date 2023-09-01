STARTING = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

BLACK =  0b01000
WHITE =  0b10000

JUICER = 0b00001
HORSE =  0b00010
BISHOP = 0b00011
ROOK =   0b00100
QUEEN =  0b00101
KING =   0b00110

NULL_PIECE = 0

# look up dictionaty from fen notation to np array
FEN_TO_PIECE = {'r': BLACK | ROOK, 'R': WHITE | ROOK, 
    'p': BLACK | JUICER, 'P': WHITE | JUICER,
    'n': BLACK | HORSE, 'N': WHITE | HORSE, 
    'b': BLACK | BISHOP, 'B': WHITE | BISHOP,
    'q': BLACK | QUEEN, 'Q': WHITE | QUEEN,
    'k': BLACK | KING, 'K': WHITE | KING, 
    ' ': NULL_PIECE}

PIECE_TO_FEN = {v: k for k, v in FEN_TO_PIECE.items()}

import numpy as np

# MOVE MASK
# --------------------------------------------------------------------------
# piece type, position on board, mask
MOVE_MASK = np.zeros(32 * 64 * 64, dtype=bool).reshape(32, 64, 64)

# BLACK JUICERS
# It could either (1) move forward one step (2) move forward 2 steps (3) en-passant
# Mask only contains (1). We will adjust the mask to include (2) and (3) in a later process
piece = BLACK | JUICER
for pos in range(64):
    if pos + 8 <= 63:
        MOVE_MASK[piece][pos][pos + 8] = 1

# WHITE JUICERS
piece = WHITE | JUICER
for pos in range(64):
    if pos - 8 >= 0:
        MOVE_MASK[piece][pos][pos - 8] = 1

# BLACK/WHITE HORSE
for color in [0b10000, 0b01000]:
    piece = color | HORSE
    for pos in range(64):
        (row, col) = (pos // 8, pos % 8)
        moves = [(row - 2, col - 1), (row - 2, col + 1), (row - 1, col - 2), (row - 1, col + 2), 
                 (row + 1, col - 2), (row + 1, col + 2), (row + 2, col - 1), (row + 2, col + 1)]
        moves = [move[0] * 8 + move[1] for move in moves if (0 <= move[0] <= 7 and 0 <= move[1] <= 7)]
        MOVE_MASK[piece][pos][moves] = 1

# BLACK/WHITE BISHOP
for color in [0b10000, 0b01000]:
    piece = color | BISHOP
    for pos in range(64):
        (row, col) = (pos // 8, pos % 8)
        # 2 diagonals
        moves = [(row + i, col + k * i) for k in [-1, 1] for i in range(-7, 8) if i != 0]
        moves = [move[0] * 8 + move[1] for move in moves if (0 <= move[0] <= 7 and 0 <= move[1] <= 7)]
        MOVE_MASK[piece][pos][moves] = 1

for color in [0b10000, 0b01000]:
    piece = color | ROOK
    for pos in range(64):
        (row, col) = (pos // 8, pos % 8)
        # 2 ranks
        moves = [(row + i, col) for i in range(-7, 8) if i != 0]
        moves += [(row, col + i) for i in range(-7, 8) if i != 0]
        moves = [move[0] * 8 + move[1] for move in moves if (0 <= move[0] <= 7 and 0 <= move[1] <= 7)]
        MOVE_MASK[piece][pos][moves] = 1

for color in [0b10000, 0b01000]:
    piece = color | QUEEN
    for pos in range(64):
        (row, col) = (pos // 8, pos % 8)
        # 2 ranks
        moves = [(row + i, col) for i in range(-7, 8) if i != 0]
        moves += [(row, col + i) for i in range(-7, 8) if i != 0]
        moves += [(row + i, col + k * i) for k in [-1, 1] for i in range(-7, 8) if i != 0]
        moves = [move[0] * 8 + move[1] for move in moves if (0 <= move[0] <= 7 and 0 <= move[1] <= 7)]
        MOVE_MASK[piece][pos][moves] = 1

for color in [0b10000, 0b01000]:
    piece = color | KING
    for pos in range(64):
        (row, col) = (pos // 8, pos % 8)
        moves = [(row + 1, col), (row + 1, col + 1), (row + 1, col - 1), (row, col + 1),
                 (row, col - 1), (row - 1, col + 1), (row - 1, col), (row - 1, col - 1)]
        moves = [move[0] * 8 + move[1] for move in moves if (0 <= move[0] <= 7 and 0 <= move[1] <= 7)]
        MOVE_MASK[piece][pos][moves] = 1

# --------------------------------------------------------------------------