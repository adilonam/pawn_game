


import random


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


