import pygame
from Colors import Colors
import pandas as pd


# This class represents the game board.
# It uses the pygame library.
class Board:
    def __init__(self, width, height):
        pygame.init()
        pygame.display.set_caption('Drone Simulator')
        self.GAME_display = pygame.display.set_mode((width + 20, height + 20))
        self.clean()
        self.borders(width, height)
        self.game_score = 0
        self.width = width
        self.height = height

    def clean(self):
        self.GAME_display.fill(Colors.white)
        pygame.display.update()

    # Rect(Surface, color, [top left point (x,y) , width, height]) -> Rect
    def borders(self, height, width):
        # top line
        pygame.draw.rect(self.GAME_display, Colors.black, [0, 0, height + 20, 10])
        # bottom line
        pygame.draw.rect(self.GAME_display, Colors.black, [0, width + 10, height + 20, 10])
        # left line
        pygame.draw.rect(self.GAME_display, Colors.black, [0, 0, 10, height + 20])
        # right line
        pygame.draw.rect(self.GAME_display, Colors.black, [height + 10, 0, 10, width + 20])
        pygame.display.update()

    def get_screen(self):
        """
        get game screen.
        :return: a game screen.
        :rtype: a pygame screen object.
        """
        return self.GAME_display

    def close(self):
        print("preparing to exit...")
        pygame.quit()
        quit()

    def pop_exit_window(self):
        pygame.font.init()  # you have to call this at the start,

        myfont = pygame.font.SysFont('Comic Sans MS', 20)
        text = myfont.render('To restart press C, Exit press X', False, (50, 50, 50))
        text2 = myfont.render('Your final score is: %d ' % tuple([self.game_score]), False, Board.red)
        self.GAME_display.blit(text, (10, self.height / 2 + 50))
        self.GAME_display.blit(text2, (self.width / 2 - 60, self.height / 2))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # quit()
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        pygame.quit()
                        # quit()
                        return False
                    elif event.key == pygame.K_c:
                        self.clean()
                        return True
