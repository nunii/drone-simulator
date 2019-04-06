import pygame
from math import cos, sin


class Sensor:
    factor = 8

    def __init__(self, start_x, start_y, color, bounds_color):
        self.color = color
        self.bounds_color = bounds_color
        self.x_position = start_x
        self.y_position = start_y
        self.rect = pygame.Rect((self.x_position, self.y_position, Sensor.factor, Sensor.factor))

    def check_bounds(self, maze):
        """
        check if the sensor get to a bounds.

        :param maze: a background maze.
        :return: coordinates of the observed bounds (or wall).
        :rtype: tuple
        """
        # check if x and y in the maze bounds.
        if maze.get_height() < round(self.x_position) or maze.get_width() < round(self.y_position):
            return round(self.x_position), round(self.y_position)
        # check if a sensor meet a bounds.
        if maze.get_at((round(self.x_position), round(self.y_position))) == self.bounds_color:
            return round(self.x_position), round(self.y_position)
        return None

    def draw(self, game_display):
        """
        draw drone over the screen.

        :param game_display: a pygame surface (screen).
        :return:
        """
        pygame.draw.rect(game_display, self.color, self.rect)

    def move(self, coordinate):
        """
        move sensor.

        :param coordinate: a drone coordinate.
        :return:
        """
        self.x_position = coordinate[0] + sin(45)*30
        self.y_position = coordinate[1] + cos(45)*30
        self.rect = pygame.Rect((self.x_position, self.y_position, Sensor.factor, Sensor.factor))
