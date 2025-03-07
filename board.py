import random

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
    
    def ai_move(self, playerColor):
        possible_moves = self.generate_moves(self.boardArray, playerColor)
        if possible_moves:
            return random.choice(possible_moves)
        return None

    def generate_moves(self, board, color):
        # Generate all possible moves for the given color
        moves = []
        for row in range(8):
            for col in range(8):
                if (color == "W" and board[row][col] == "W") or (color == "B" and board[row][col] == "B"):
                    if color == "W":
                        directions = [(-1, 0), (-2, 0), (-1, -1), (-1, 1)]
                    else:
                        directions = [(1, 0), (2, 0), (1, -1), (1, 1)]
                    for d_row, d_col in directions:
                        new_row, new_col = row + d_row, col + d_col
                        if 0 <= new_row < 8 and 0 <= new_col < 8:
                            move = f"{chr(col + 97)}{8 - row}{chr(new_col + 97)}{8 - new_row}"
                            if self.computeMove(move, color):
                                moves.append(move)
        return moves

class Node:
    def __init__(self, move=None, parent=None):
        self.move = move
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def add_child(self, child_node):
        self.children.append(child_node)

    def update(self, result):
        self.visits += 1
        self.wins += result

class MCTS:
    def __init__(self, board, playerColor):
        self.board = board
        self.playerColor = playerColor
        self.opponentColor = "B" if playerColor == "W" else "W"

    def select(self, node):
        # Select the child with the highest UCB1 value
        best_child = max(node.children, key=lambda child: child.wins / child.visits + (2 * (2 * (child.visits ** 0.5) / (1 + child.visits))))
        return best_child

    def expand(self, node):
        # Generate all possible moves and add them as children
        possible_moves = self.generate_moves(self.board, self.playerColor)
        for move in possible_moves:
            child_node = Node(move=move, parent=node)
            node.add_child(child_node)

    def simulate(self, node):
        # Simulate a random game from the current node
        current_board = self.board.copy()
        current_color = self.playerColor
        while not self.is_terminal(current_board):
            possible_moves = self.generate_moves(current_board, current_color)
            move = random.choice(possible_moves)
            self.make_move(current_board, move, current_color)
            current_color = "B" if current_color == "W" else "W"
        return self.get_result(current_board)

    def backpropagate(self, node, result):
        # Update the node and its ancestors with the result
        while node is not None:
            node.update(result)
            node = node.parent

    def get_best_move(self):
        root = Node()
        for _ in range(1000):  # Number of iterations
            node = root
            while node.children:
                node = self.select(node)
            self.expand(node)
            result = self.simulate(node)
            self.backpropagate(node, result)
        best_move = max(root.children, key=lambda child: child.visits).move
        return best_move

    def generate_moves(self, board, color):
        # Generate all possible moves for the given color
        moves = []
        for row in range(8):
            for col in range(8):
                if (color == "W" and board[row][col] == "W") or (color == "B" and board[row][col] == "B"):
                    if color == "W":
                        directions = [(-1, 0), (-2, 0), (-1, -1), (-1, 1)]
                    else:
                        directions = [(1, 0), (2, 0), (1, -1), (1, 1)]
                    for d_row, d_col in directions:
                        new_row, new_col = row + d_row, col + d_col
                        if 0 <= new_row < 8 and 0 <= new_col < 8:
                            move = f"{chr(col + 97)}{8 - row}{chr(new_col + 97)}{8 - new_row}"
                            if self.board.computeMove(move, color):
                                moves.append(move)
        return moves

    def make_move(self, board, move, color):
        # Make the move on the board
        start_col = ord(move[0]) - ord('a')
        start_row = 8 - int(move[1])
        end_col = ord(move[2]) - ord('a')
        end_row = 8 - int(move[3])
        board[end_row][end_col] = board[start_row][start_col]
        board[start_row][start_col] = " "

    def is_terminal(self, board):
        # Check if the game is over
        return False  # Simplified for this example

    def get_result(self, board):
        # Get the result of the game
        return 1  # Simplified for this example

    def copy(self):
        # Return a deep copy of the board
        return [row[:] for row in self.board]


