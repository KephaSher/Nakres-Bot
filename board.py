from util import timer
from exceptions import IllegalMoveError
import numpy as np
from bitmasks import *

class Piece:
    def __init__(self, position: int, value: int):
        self.value = value # value encodes type + piece
        self.pos = position

    def __str__(self):
        return PIECE_TO_FEN[self.value] + " " + str(self.pos)

    # a bitmask of possible moves. Might be blocked, need to check later
    # return a list of bits, to be or-ed
    def get_move_mask(self):
        return MOVE_MASK[self.value][self.pos]

class Move:
    # if going to an empty square, NULL_MOVE will be used
    # for castling, only the king's movement is described
    def __init__(self, piece1: Piece, piece2: Piece, is_promotion: bool, is_castle: bool):
        self.piece1 = piece1
        self.piece2 = piece2
        self.is_promotion = is_promotion

class Board:
    def __init__(self, fen = STARTING):
        # the FEN notation includes all information required for a board
        # a single string

        # some rules regarding FEN:
        # https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation#Definition

        self.fen = fen

        # 1D array representation using 5 bit integers
        self.board = self.__convert_to_board(self.fen)

        # 1 if there's a piece, 0 if not
        self.bitmask = (self.board != 0)

        # 1 for white, 0 for black
        self.to_move = 1

        self.passant = -1 # I shall worry about this later, -1 for null, otherwise index 
        self.white_castle_left = 1
        self.white_castle_right = 1
        self.black_castle_left = 1
        self.black_castle_right = 1
        self.total_moves = 1
        self.halfclock = 0 # I shall worry about this later

        # self.pieces[PIECE] = piece index (ignore pieces[0])
        # loop over this list when searching for legal moves
        self.pieces = []
        for pos in range(len(self.board)):
            if (self.board[pos]):
                self.pieces.append(Piece(pos, self.board[pos]))
    
    def __str__(self):
        ret = str()
        for i in range(8):
            ret2 = str()
            for j in range(8):
                ret2 += PIECE_TO_FEN[self.board[i * 8 + j]]
            ret += " " + " | ".join(ret2) + "\n" + "-" * 31 + "\n"

        ret += "White to move" if self.to_move else "Black to move" + "\n"
        ret += "White Casting rights: " + str(self.white_castle_left) + str(self.white_castle_right) + "\n"
        ret += "Black Casting rights: " + str(self.black_castle_left) + str(self.black_castle_right) + "\n"
        ret += "En passant square: " + ("-" if self.passant == -1 else str(self.board[self.passant])) + "\n"
        ret += "Halfmove clock: " + str(self.halfclock) + "\n"
        ret += "Total moves: " + str(self.total_moves)
        return ret

    # converts fen to board
    def __convert_to_board(self, fen):
        ret = np.zeros(64, dtype = int)
        newstr = str()

        for row in fen.split("/"):
            rank = row[:8]
            for box in rank:
                if box.isdigit():
                    newstr += " " * int(box)
                else:
                    newstr += box
        
        for i in range(64):
            ret[i] = FEN_TO_PIECE[newstr[i]]

        return ret

    def coordToNum(self, coord: str):
        return (8 - int(coord[1])) * 8 + (ord(coord[0]) - ord('a'))

    def castle_move(self, move: str):
        pass

    # this function just moves the pieces, WITH NO CHECKS OF ANY KIND
    def normal_move(self, move: str):
        if type(move) != str:
            raise IllegalMoveError(move, "is not of type str")
        
        is_promotion = len(move) == 5

        first_pos = self.coordToNum(move[:2])
        second_pos = self.coordToNum(move[2:])

        if (is_promotion):
            # change the second pos to the promotion piece
            self.board[second_pos] = FEN_TO_PIECE[move[-1]]
            # set the first pos to empty
            self.board[first_pos] = NULL_PIECE
        else: 
            # takes (or not)
            self.board[second_pos] = self.board[first_pos]
            # set first pos to empty
            self.board[first_pos] = NULL_PIECE

        self.to_move = 1 - self.to_move
        self.total_moves += 1

    def legal_moves(self):
        ret = []

        
#             if (self.board[second_pos] >> 3) ^ (self.board[first_pos >> 3]):
#                raise IllegalMoveError(move, "attempted to move to a position occupied by friendly pieces")

# bitboards uses approx 67M per piece, I will brute force for now

B = Board()
print(B)
