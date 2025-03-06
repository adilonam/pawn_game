class ChessBoard:
    def __init__(self):
        self.boardArray = [[" " for _ in range(8)] for _ in range(8)]
        self.round = 0
        self.enpassant = False
        self.enpassantCol = None

    def changePerspective(self):
        # Change the perspective of the board
        pass

    def computeMove(self, move, flag):
        # Compute the move on the board
        pass
