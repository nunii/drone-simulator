import pygame
from math import cos, sin, radians, inf


class Sensor:
    factor = 8

    def __init__(self, start_x, start_y, angle, radius, color, bounds_color):
        self.color = color
        self.bounds_color = bounds_color
        self.x_pos_start = start_x
        self.y_pos_start = start_y
        self.angle = angle
        self.radius = radius
        self.last_bound = tuple()

    #@property
    def angle(self):
        return self.angle

    #@angle.setter
    def add_angle(self, angle):
        self.angle += angle
        if self.angle >= 360:
            self.angle = 0
        if self.angle < 0:
            self.angle = 359

    def calc_x_end(self):
        return self.x_pos_start + cos(radians(self.angle)) * self.radius

    def calc_y_end(self):
        return self.x_pos_start + sin(radians(self.angle)) * self.radius

    def get_cord_start(self):
        return round(self.x_pos_start), round(self.y_pos_start)

    def get_cord_end(self):
        return round(self.calc_x_end()), round(self.calc_y_end())

    def check_bounds(self, maze):
        """
        check if the sensor get to a bounds.

        :param maze: a background maze.
        :return: coordinates of the observed bounds (or wall).
        :rtype: tuple or string
        """
        # check if x and y in the maze bounds.
        if maze.get_height() < round(self.x_pos_start * self.radius) \
                or maze.get_width() < round(self.y_pos_start * self.radius):
            self.last_bound = maze.get_height(), maze.get_width()
            return self.last_bound

        # check if a sensor meet a bounds.
        for dest in range(1, self.radius + 1):
            if maze.get_at((round(self.x_pos_start + dest), round(self.y_pos_start + dest))) == self.bounds_color:
                self.last_bound = round(self.x_pos_start), round(self.y_pos_start)
                return self.last_bound
        return inf

    def draw(self, game_display):
        """draw Lidar over the screen.

        :param game_display: a pygame surface (screen).
        :return:
        """
        pygame.draw.line(game_display, self.color, self.get_cord_start(), self.get_cord_end())

    def move(self, coordinate):
        """move sensor.

        :param coordinate: a drone coordinate.
        :return:
        """
        self.x_pos_start = coordinate[0]
        self.y_pos_start = coordinate[1]
