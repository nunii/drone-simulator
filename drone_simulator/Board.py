import pygame
from Colors import Colors


# This class represents the game board.
# It uses the pygame library.
class Board:
    def __init__(self, width, height, color, borders_color):
        pygame.init()
        pygame.font.init()
        self.GAME_display = pygame.display.set_mode((width + 20, height + 20))
        pygame.display.set_caption('Drone Simulator')
        self.color = color
        self.borders_color = borders_color

        self.clean()
        self.borders(width, height)
        self.game_score = 0
        self.width = width
        self.height = height

        self.font = pygame.font.SysFont('Comic Sans MS', 20)
        self.font_color = Colors.blue_black
        self.out_string = "Y: {yaw}, S:{speed}, lidar[ L:{left} R:{right} H:{head} ], Crashed:{crash}, Score:{score}" \
            .format(yaw=0, speed=0, left=0, right=0, head=0, crash=0, score=0)
        self.text = self.font.render(self.out_string, False, self.font_color)
        pygame.draw.rect(self.GAME_display, Colors.white, pygame.Rect(20, 10, self.text.get_width(), self.text.get_height()))
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

    # def put_text(self):
        # pygame.font.init()  # you have to call this at the start,
        # text = self.font.render(str(obj), False, (50, 50, 50))
        # out_string = "Y: {yaw}, S:{speed}, lidar[ L:{left} R:{right} H:{head} ], Crashed:{crash}, Score:{score}"
        # self.GAME_display.blit(text, (10, self.height / 2 + 50))
        # pygame.display.update()

    def update_text(self, lst):
        pygame.draw.rect(self.GAME_display, Colors.white, pygame.Rect(20, 10, self.text.get_width(), self.text.get_height()))
        self.out_string = "Y: {yaw}, S:{speed}, lidar[ L:{left} R:{right} H:{head} ], Crashed:{crash}, Score:{score}"\
            .format(yaw=lst[0], speed=lst[1], left=lst[2], right=lst[3],
                    head=lst[4], crash=lst[5], score=lst[6])
        self.text = self.font.render(self.out_string, True, self.font_color)
        self.GAME_display.blit(self.text, (20, 10))




