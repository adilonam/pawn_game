class ChessBoard:
    def __init__(self):
        self.boardArray = [[" " for _ in range(8)] for _ in range(8)]
        self.round_time = 0
        self.round = 0
        self.enpassant = False
        self.enpassantCol = None

    def computeMove(self, move , playerColor):
        """
        Validates if the given move is a legal pawn move.
        :param move: str, chess move in format like 'h2h4'
        :return: bool, True if the move is valid, False otherwise
        """
        move = move.lower().strip()  # Convert to lowercase for case-insensitive comparison
        if len(move) != 4:
            return False  # Invalid move format
        
        start, end = move[:2], move[2:]
        start_col, start_row = ord(start[0]) - 97, 8 - int(start[1])
        end_col, end_row = ord(end[0]) - 97, 8- int(end[1])
        # Ensure the column remains the same (no sideways movement for pawns)
        if start_col != end_col:
            # Authorize diagonal move if opponent pawn is in the diagonal
            if abs(start_col - end_col) == 1 and abs(start_row - end_row) == 1:
                if playerColor == "W" and self.boardArray[end_row][end_col] == "B":
                    return True  # Valid capture move for white
                elif playerColor == "B" and self.boardArray[end_row][end_col] == "W":
                    return True  # Valid capture move for black
            return False
        else:
            # Pawn can move one or two squares forward from the starting position
            if playerColor == "B":
                if (end_row - start_row == 2 and self.round == 0) or end_row - start_row == 1:
                    return True  # Valid move for white
            elif playerColor == "W":
                if (start_row - end_row == 2 and  self.round == 0) or start_row - end_row == 1:
                    return True  # Valid move for black
        
        return False  # Invalid move

    def changePerspective(self, move, flag):
        # Compute the move on the board
        start_col = ord(move[0]) - ord('a')
        start_row = 8 - int(move[1])
        end_col = ord(move[2]) - ord('a')
        end_row = 8 - int(move[3])

        piece = self.boardArray[start_row][start_col]
        self.boardArray[start_row][start_col] = " "
        self.boardArray[end_row][end_col] = piece

    
