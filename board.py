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
        start_col = ord(move[0]) - ord('a')
        start_row = 8 - int(move[1])
        end_col = ord(move[2]) - ord('a')
        end_row = 8 - int(move[3])

        piece = self.boardArray[start_row][start_col]
        self.boardArray[start_row][start_col] = " "
        self.boardArray[end_row][end_col] = piece
