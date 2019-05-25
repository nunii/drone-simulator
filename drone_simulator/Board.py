import pygame
from Colors import Colors
from datetime import timedelta


# This class represents the game board.
# It uses the pygame library.
class Board:
    def __init__(self, width, height, color, borders_color):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Drone Simulator')
        self.GAME_display = pygame.display.set_mode((width + 20, height + 20))
        self.color = color
        self.borders_color = borders_color
        self.time = 0

        self.clean()
        self.borders(width, height)
        self.game_score = 0

        self.font = pygame.font.SysFont('Comic Sans MS', 20)
        self.font_color = Colors.blue_black
        self.info = "Y: {yaw:.3f}, S:{speed:.3f}, lidars[ L:{left} R:{right} H:{head} ], " \
                    "Crashed:{crash}, Score:{score}, time:{time}, battery:{battery}"
        self.text = self.font.render(self.info.format(yaw=0, speed=0, left=0, right=0, head=0,
                                                      crash=0, score=0,
                                                      time=str(timedelta(seconds=self.time)).split('.')[0],
                                                      battery=0)
                                     , False, self.font_color)
        pygame.draw.rect(self.GAME_display, Colors.white, pygame.Rect(20, 10, self.text.get_width(),
                                                                      self.text.get_height()))
        self.GAME_display.blit(self.text, (20, 10))
        pygame.display.update()

    def clean(self):
        self.GAME_display.fill(self.color)
        pygame.display.update()

    # Rect(Surface, color, [top left point (x,y) , width, height]) -> Rect
    def borders(self, height, width):
        # top line
        pygame.draw.rect(self.GAME_display, self.borders_color, [0, 0, height + 20, 10])
        # bottom line
        pygame.draw.rect(self.GAME_display, self.borders_color, [0, width + 10, height + 20, 10])
        # left line
        pygame.draw.rect(self.GAME_display, self.borders_color, [0, 0, 10, height + 20])
        # right line
        pygame.draw.rect(self.GAME_display, self.borders_color, [height + 10, 0, 10, width + 20])
        pygame.display.update()

    def get_screen(self):
        """get game screen.

        :return: a game screen.
        :rtype: a pygame screen object.
        """
        return self.GAME_display

    def close(self):
        print("preparing to exit...")
        pygame.display.quit()
        pygame.quit()
        print("end.")

    def update_text(self, dic):
        pygame.draw.rect(self.GAME_display, Colors.white, pygame.Rect(20, 10, self.text.get_width(),
                                                                      self.text.get_height()))
        text = self.info.format(yaw=dic['yaw'],
                                speed=dic['speed'],
                                left=dic['left'],
                                right=dic['right'],
                                head=dic['head'],
                                crash=dic['crash'],
                                score=dic['score'],
                                time=str(timedelta(seconds=self.time)).split('.')[0],
                                battery=dic['battery'])
        self.text = self.font.render(text, True, self.font_color)
        print(text)
        self.GAME_display.blit(self.text, (20, 10))
