import pygame

class UserInterface:
    def __init__(self, surface, chessboard):
        self.surface = surface
        self.chessboard = chessboard
        self.playerColor = None
        self.firstgame = True
        self.time = 0
        self.load_images()

    def load_images(self):
        self.images = {
            "wp": pygame.image.load("Chess_Images/wp.png"),
            "bp": pygame.image.load("Chess_Images/bp.png")
        }

    def drawComponent(self):
        self.surface.fill((255, 255, 255))
        font = pygame.font.SysFont(None, 24)
        for row in range(8):
            for col in range(8):
                piece = self.chessboard.boardArray[row][col]
                if piece != " ":
                    self.surface.blit(self.images[piece], (col * 75, row * 75))
                # Draw row numbers on the left side
                if col == 0:
                    row_label = font.render(str(8 - row), True, (0, 0, 0))
                    self.surface.blit(row_label, (5, row * 75 + 30))
            # Draw column letters on the bottom
            col_label = font.render(chr(97 + col), True, (0, 0, 0))
            self.surface.blit(col_label, (col * 75 + 30, 600 - 20))
        pygame.display.flip()

    def clientMove(self):
        # Handle player move input
        # Return the move and flag indicating win/lose status
        pass
