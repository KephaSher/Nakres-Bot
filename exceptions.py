class IllegalMoveError(Exception):
    def __init__(self, move: str, message="Move {} is not legal"):
        self.move = move
        self.message = message.format(move)
        super().__init__(self.message)
