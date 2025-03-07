import pygame

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

        light_square_color = (240, 217, 181)  # Beige
        dark_square_color = (181, 136, 99)    # Brown
        
        label_gap = self.surface.get_width() * 20 // 600
        square_len = (self.surface.get_width() - 2 * label_gap) // 8

    def load_images(self):
        self.images = {
            "wp": pygame.image.load("Chess_Images/wp.png"),
            "bp": pygame.image.load("Chess_Images/bp.png")
        }

    def drawComponent(self):
        self.surface.fill((181, 136, 99))
        font = pygame.font.SysFont(None, 24)
        
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
                if self.selected_piece:
                    self.chessboard.boardArray[self.selected_pos[0]][self.selected_pos[1]] = " "
                    self.chessboard.boardArray[row][col] = self.selected_piece
                    self.selected_piece = None
                    self.selected_pos = None
                else:
                    self.selected_piece = self.chessboard.boardArray[row][col]
                    self.selected_pos = (row, col)
        self.drawComponent()

    def clientMove(self):
        # Handle player move input
        # Return the move and flag indicating win/lose status
        pass
