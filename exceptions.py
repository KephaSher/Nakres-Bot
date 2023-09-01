class IllegalMoveError(Exception):
    def __init__(self, move: str, message="is not legal"):
        self.move = move
        self.message = "Move " + move + ": " + message
        super().__init__(self.message)
