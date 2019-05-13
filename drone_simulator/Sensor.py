import pygame
from math import cos, sin, radians, inf


class Sensor:
    factor = 8

    def __init__(self, start_x, start_y, angle, radius, color, bounds_color):
        self.color = color
        self.bounds_color = bounds_color
        self.x_pos_start = start_x
        self.y_pos_start = start_y

        if angle < 0:
            angle = 360 + angle

        self.angle = angle
        self.radius = radius
        self.last_bound = tuple()

    def add_angle(self, angle):
        self.angle += angle
        if self.angle >= 360:
            self.angle = self.angle % 360
        elif self.angle < 0:
            self.angle = 360 + self.angle

    def calc_x_end(self):
        return self.x_pos_start + cos(radians(self.angle)) * self.radius

    def calc_y_end(self):
        return self.y_pos_start + sin(radians(self.angle)) * self.radius

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

        # check if a sensor meet a bounds.
        for dest in self.get_range():
            print(dest)
            if maze.get_at(dest) == self.bounds_color:
                print("bound")
                self.last_bound = dest
                return self.last_bound
        return inf

    def draw(self, game_display):
        """draw Lidar over the screen.

        :param game_display: a pygame surface (screen).
        :return:
        """
        if type(self.last_bound) is not tuple:
            pygame.draw.line(game_display, self.color, self.get_cord_start(), self.last_bound)
        else:
            pygame.draw.line(game_display, self.color, self.get_cord_start(), self.get_cord_end())

    def move(self, coordinate):
        """move sensor.

        :param coordinate: a drone coordinate.
        :return:
        """
        self.x_pos_start = coordinate[0]
        self.y_pos_start = coordinate[1]

    def get_range(self):
        """generate x,y range from x start, y start to end.

        :return:
        """
        return [(round(self.calc_x_by_radius(count)), round(self.calc_y_by_radius(count)))
                for count in range(1, self.radius+1)]

    def calc_x_by_radius(self, radius):
        return round(self.x_pos_start + cos(radians(self.angle)) * radius)

    def calc_y_by_radius(self, radius):
        return round(self.y_pos_start + sin(radians(self.angle)) * radius)
