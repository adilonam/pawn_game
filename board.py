import random

class ChessBoard:
    def __init__(self):
        self.boardArray = [[" " for _ in range(8)] for _ in range(8)]
        self.round_time = 0
        self.round = 0
        self.time = 0
        self.enpassant = False
        self.enpassantCol = None

    def computeMove(self, move , player_color):
        """
        Validates if the given move is a legal pawn move.
        :param move: str, chess move in format like 'h2h4'
        :return: bool, True if the move is valid, False otherwise
        """
        move = move.lower().strip()  # Convert to lowercase for case-insensitive comparison
        if len(move) != 4:
            return 0  # Invalid move format
        
        start, end = move[:2], move[2:]
        start_col, start_row = ord(start[0]) - 97, 8 - int(start[1])
        end_col, end_row = ord(end[0]) - 97, 8- int(end[1])
        # Ensure the start and end positions are within the board
        if not (0 <= start_col < 8 and 0 <= start_row < 8 and 0 <= end_col < 8 and 0 <= end_row < 8):
            return 0
        # Ensure the start position contains the player's pawn
        if self.boardArray[start_row][start_col] == " " or player_color not in self.boardArray[start_row][start_col]:
            return 0
        # Ensure the column remains the same (no sideways movement for pawns)
        if start_col != end_col:
            # Check for en passant move
            if  player_color == "W" and  self.boardArray[start_row][end_col] == "B*" and start_row - end_row == 1 and self.boardArray[end_row][end_col] == " ":
                return 2
            elif  player_color == "B" and  self.boardArray[start_row][end_col] == "W*" and end_row - start_row == 1 and self.boardArray[end_row][end_col] == " ":
                return 2
            # Authorize diagonal move if opponent pawn is in the diagonal
            if abs(start_col - end_col) == 1 and abs(start_row - end_row) == 1:
                if player_color == "W" and self.boardArray[end_row][end_col][0] == "B" and start_row > end_row:
                    return 1  # Valid capture move for white
                elif player_color == "B" and self.boardArray[end_row][end_col][0] == "W" and start_row < end_row:
                    return 1  # Valid capture move for black
            return 0
        else:
            # Pawn can move one or two squares forward from the starting position
            if player_color == "B":
                if (end_row - start_row == 2 and self.boardArray[start_row][start_col] == "B" and self.boardArray[end_row][end_col] == " " and start_row == 1 and  self.boardArray[end_row-1][end_col] == " ") or (end_row - start_row == 1 and self.boardArray[end_row][end_col] == " "):
                    return 1  # Valid move for black
            elif player_color == "W":
                if (start_row - end_row == 2 and self.boardArray[start_row][start_col] == "W"  and self.boardArray[end_row][end_col] == " " and start_row == 6 and self.boardArray[end_row+1][end_col] == " ") or (start_row - end_row == 1 and self.boardArray[end_row][end_col] == " "):
                    return 1  # Valid move for white
        
        return 0  # Invalid move

    def changePerspective(self, move):
        # Compute the move on the board
        start_col = ord(move[0]) - ord('a')
        start_row = 8 - int(move[1])
        end_col = ord(move[2]) - ord('a')
        end_row = 8 - int(move[3])
        for i in range(64):
            self.boardArray[i//8][i%8] = self.boardArray[i//8][i%8].replace("*", "")
        # Check for en passant move
        en_passant = ""
        if abs(start_row - end_row) == 2:
            en_passant = "*"
        piece = self.boardArray[start_row][start_col]
        self.boardArray[start_row][start_col] = " "
        self.boardArray[end_row][end_col] = piece[0] + en_passant
    



    
    def check_win_loss(self):
        white_pawn_exists = False
        black_pawn_exists = False
        for i in range(64):
            if "W" in self.boardArray[i // 8][i % 8] :
                white_pawn_exists = True
                if i // 8 == 0:  # White pawn reaches the last row
                    return 'W'
            elif "B" in self.boardArray[i // 8][i % 8] :
                black_pawn_exists = True
                if i // 8 == 7:  # Black pawn reaches the last row
                    return 'B'
        if not white_pawn_exists:
            return 'B'
        if not black_pawn_exists:
            return 'W'
        return "0"
    
    def setup(self, data):
        pawn_num = 0
        for i in range(64):
            self.boardArray[i // 8][i % 8] = " "
        for i in range(6, len(data), 4):
            piece_color = data[i].strip()
            piece_position = data[i + 1:i + 3].strip()
            row = 8 - int(piece_position[1])
            col = ord(piece_position[0]) - 97
            # Debugging statements
            if 0 <= row < 8 and 0 <= col < 8:
                if piece_color == 'W':
                    self.boardArray[row][col] = "W"
                else:
                    self.boardArray[row][col] = "B"
                pawn_num += 1
            else:
                print(f"Invalid position: {piece_position}")
        self.round_time = int(self.time / pawn_num)











