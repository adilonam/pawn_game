import math

def minimax(board, depth, alpha, beta, maximizing_player, player_color):
    if depth == 0 or is_terminal(board):
        return evaluate_board(board, player_color)
    
    if maximizing_player:
        max_eval = -math.inf
        for move in get_all_possible_moves(board, player_color):
            new_board = make_move(board, move)
            eval = minimax(new_board, depth - 1, alpha, beta, False, player_color)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        opponent_color = 'B' if player_color == 'W' else 'W'
        for move in get_all_possible_moves(board, opponent_color):
            new_board = make_move(board, move)
            eval = minimax(new_board, depth - 1, alpha, beta, True, player_color)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def is_terminal(board):
    # Check if the game is over (no pawns left or a pawn has reached the opposite end)
    white_exists = any('W' in cell for row in board for cell in row)
    black_exists = any('B' in cell for row in board for cell in row)
    if not white_exists or not black_exists:
        return True
    if any('W' in cell for cell in board[0]) or any('B' in cell for cell in board[7]):
        return True
    return False

def evaluate_board(board, player_color):
    score = 0
    for row in board:
        for cell in row:
            if player_color in cell:
                score += 1
            elif cell.strip() and player_color not in cell:
                score -= 1
    if any('W' in cell for cell in board[0]):
        score += 10000 if player_color == 'W' else -10000
    if any('B' in cell for cell in board[7]):
        score +=  10000 if player_color == 'B' else - 10000
    # Prioritize en passant moves
    for i in range(8):
        for j in range(8):
            # Reward pawns closer to the opponent's last row
            if player_color == 'W' and 'W' in board[i][j]:
                score += math.exp((7 - i) )
            elif player_color == 'B' and 'B' in board[i][j]:
                score +=  math.exp(i)
    return score

def get_all_possible_moves(board, player_color):
    moves = []
    direction = -1 if player_color == 'W' else 1
    opponent_color = 'B' if player_color == 'W' else 'W'
    
    for i in range(8):
        for j in range(8):
            if player_color in board[i][j]:  # Found a player's pawn
                
                # Normal move forward
                if 0 <= i + direction < 8 and board[i + direction][j] == ' ':
                    moves.append(((i, j), (i + direction, j)))
                    
                    # Initial two-step move
                    if player_color == 'W' and i == 6 and 0 <= i + 2 * direction < 8 and board[i + 2 * direction][j] == ' ':
                        moves.append(((i, j), (i + 2 * direction, j)))
                    elif player_color == 'B' and i == 1 and 0 <= i + 2 * direction < 8 and board[i + 2 * direction][j] == ' ':
                        moves.append(((i, j), (i + 2 * direction, j)))
                
                # Capturing moves
                for dj in [-1, 1]:  # Check both diagonals
                    if 0 <= i + direction < 8 and 0 <= j + dj < 8:
                        if opponent_color in board[i + direction][j + dj]:  # Normal capture
                            moves.append(((i, j), (i + direction, j + dj)))

                        # En passant check
                        if '*' in board[i][j + dj]:  # Adjacent pawn has *
                            if board[i][j + dj] == f"{opponent_color}*":  # Check if it's an opponent's pawn
                                moves.append(((i, j), (i + direction, j + dj)))  # En passant move

    return moves

def make_move(board, move):
    new_board = [row[:] for row in board]
    start, end = move
    
    if '*' in new_board[start[0]][end[1]]  and new_board[start[0]][end[1]][0] != new_board[start[0]][start[1]][0]:
        new_board[start[0]][end[1]] = ' '

    new_board[end[0]][end[1]] = new_board[start[0]][start[1]]
    new_board[start[0]][start[1]] = ' '
    return new_board

def get_best_move(board, player_color):
    best_move = None
    best_value = -math.inf
    for move in get_all_possible_moves(board, player_color):
        new_board = make_move(board, move)
        move_value = minimax(new_board, 3, -math.inf, math.inf, False, player_color)
        if move_value > best_value:
            best_value = move_value
            best_move = move
    return best_move

def position_to_chess_notation(position):
    row, col = position
    return chr(col + ord('a')) + str(8 - row)

def main():
    board = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'W'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'W', 'B', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    ]
    player_color = 'W'
    best_move = get_best_move(board, player_color)
    if best_move:
        start, end = best_move
        print(f"Best move: {position_to_chess_notation(start)}{position_to_chess_notation(end)}")
    else:
        print("No valid moves available")

if __name__ == "__main__":
    main()
