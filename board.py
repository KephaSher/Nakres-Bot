from util import timer
from exceptions import IllegalMoveError

STARTING = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

class Board:
    def __init__(self, fen = STARTING):
        # the FEN notation includes all information required for a board
        # a single string

        # some rules regarding FEN:
        # https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation#Definition

        self.fen = fen

    def __str__(self):
        ret = str()
        rows = self.fen.split('/')
        for row in rows:
            s = row[:8]
            rev2 = list()
            for i in s:
                if i.isdigit():
                    rev2 += ["   "] * int(i)
                else:
                    rev2.append(" " + i + " ")
            ret += "|".join(rev2) + "\n"
            ret += "-" * 32 + "\n"
        
        stats = rows[-1][9: ].split(" ")
        ret += "White to move" if stats[0] == 'w' else "Black to move" + "\n"
        ret += "Casting rights: " + stats[1] + "\n"
        ret += "En passant square: " + stats[2] + "\n"
        ret += "Halfmove clock: " + stats[3] + "\n"
        ret += "Total moves: " + stats[4]
        return ret
        
    def move(move: str):
        if type(move) != str:
            raise IllegalMoveError(move)
        
        

print(Board())
