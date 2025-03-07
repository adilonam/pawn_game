import pygame
import time as time_module
class UserInterface:
    def __init__(self, surface, chessboard):
        self.surface = surface
        self.chessboard = chessboard
        self.playerColor = None
        self.firstgame = True
        self.time = 0
        self.load_images()
        self.selected_piece = None
        self.selected_pos = None

        self.socketObject = None
        self.light_square_color = (240, 217, 181)  # Beige
        self.dark_square_color = (181, 136, 99)    # Brown
        
        self.label_gap = self.surface.get_width() * 20 // 600
        self.square_len = (self.surface.get_width() - 2 * self.label_gap) // 8

    def load_images(self):
        self.images = {
            "W": pygame.image.load("Chess_Images/wp.png"),
            "B": pygame.image.load("Chess_Images/bp.png")
        }

    def drawComponent(self):
        self.surface.fill((181, 136, 99))
        font = pygame.font.SysFont(None, 24)
        if self.playerColor:
            pygame.display.set_caption(f'Pawn Game : {self.playerColor}')
        for row in range(8):
            for col in range(8):
                square_color = self.light_square_color if (row + col) % 2 == 0 else self.dark_square_color
                pygame.draw.rect(self.surface, square_color, pygame.Rect(self.label_gap + col * self.square_len, self.label_gap + row * self.square_len, self.square_len, self.square_len))
                piece = self.chessboard.boardArray[row][col]
                if piece != " ":
                    self.surface.blit(self.images[piece], (self.label_gap + col * self.square_len, self.label_gap + row * self.square_len))
                # Draw row numbers on the left side
                if col == 0:
                    row_label = font.render(str(8 - row), True, (0, 0, 0))
                    self.surface.blit(row_label, (0, self.label_gap + row * self.square_len + self.square_len // 2))
                # Draw column letters on the bottom
                if row == 7:
                    col_label = font.render(chr(97 + col), True, (0, 0, 0))
                    self.surface.blit(col_label, (self.label_gap + col * self.square_len + self.square_len // 2, self.surface.get_height() - self.label_gap))
        pygame.display.flip()

    def handle_event(self, event):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = (x - self.label_gap) // self.square_len
            row = (y - self.label_gap) // self.square_len
            if 0 <= col < 8 and 0 <= row < 8:
                if  self.chessboard.boardArray[row][col][0] == self.playerColor:
                    print(f"Selected piece: {self.chessboard.boardArray[row][col]}")
                    self.selected_piece = self.chessboard.boardArray[row][col]
                    self.selected_pos = (row, col)
                if self.selected_piece:
                    move_from = chr(97 + self.selected_pos[1]) + str(8 - self.selected_pos[0])
                    move_to = chr(97 + col) + str(8 - row)
                    move = f"{move_from}{move_to}"
                    if not self.chessboard.computeMove(move , self.playerColor):
                        return False, ""
                    self.chessboard.boardArray[self.selected_pos[0]][self.selected_pos[1]] = " "
                    self.chessboard.boardArray[row][col] = self.selected_piece
                    self.selected_piece = None
                    self.selected_pos = None
                    self.chessboard.round += 1
                    self.drawComponent()
                    return True, f"{move_from}{move_to}"
                
        return False, ""
        
    def check_win_loss(self):
        white_pawn_exists = False
        black_pawn_exists = False
        for i in range(64):
            if self.chessboard.boardArray[i // 8][i % 8] == "W":
                white_pawn_exists = True
                if i // 8 == 0:  # White pawn reaches the last row
                    return 'W'
            elif self.chessboard.boardArray[i // 8][i % 8] == "B":
                black_pawn_exists = True
                if i // 8 == 7:  # Black pawn reaches the last row
                    return 'B'
        if not white_pawn_exists:
            return 'B'
        if not black_pawn_exists:
            return 'W'
        return None

    def clientMove(self):
        is_moved = False
        while not is_moved:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.socketObject.close()
                    break
                is_moved, movement = self.handle_event(event)
        flag = self.check_win_loss()
        return movement,flag
