import pygame


class Drone:
    factor = 15

    def __init__(self, start_x, start_y, color):
        self.color = color
        self.x_position = start_x
        self.y_position = start_y
        self.rect = pygame.Rect((self.x_position, self.y_position, Drone.factor, Drone.factor))

    def handle_keys(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.move_ip(-1, 0)
            self.x_position -= 1
        if key[pygame.K_RIGHT]:
            self.rect.move_ip(1, 0)
            self.x_position += 1
        if key[pygame.K_UP]:
            self.rect.move_ip(0, -1)
            self.y_position -= 1
        if key[pygame.K_DOWN]:
            self.rect.move_ip(0, 1)
            self.y_position += 1

    def get_position(self):
        """
        get drone coordinates.
        :return: a coordinates of the drone.
        :rtype: tuple. (x_position, y_position)
        """
        return self.x_position, self.y_position

    def move_head(self, dx, dy):
        pass

    def update(self):
        pass

    def check_death(self, display_width, display_height):
        return False

    def draw(self, game_display):
        """
        draw drone over the screen.
        :param game_display: a pygame surface (screen).
        :return:
        """
        pygame.draw.rect(game_display, self.color, self.rect)

    @staticmethod
    def delete_old_rect(game_display, coordination, color):
        """
        delete old drone over the screen.
        :param color: a color to draw.
        :param coordination: a drone old coordination, tuple.
        :param game_display: a pygame surface (screen).
        :return:
        """
        background = pygame.Rect((coordination[0], coordination[1], Drone.factor, Drone.factor))
        pygame.draw.rect(game_display, color, background)
