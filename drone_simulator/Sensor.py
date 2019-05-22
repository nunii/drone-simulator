import pygame
from math import cos, sin, radians, inf


class Sensor:
    factor = 8

    def __init__(self, start_x, start_y, angle, radius, color, bounds_color):
        self.color = color
        # maze bounds color.
        self.bounds_color = bounds_color
        self.x_pos_start = start_x
        self.y_pos_start = start_y

        if angle < 0:
            angle = 360 + angle

        self.angle = angle
        # lidar beam length
        self.radius = radius
        # tuple for the last (X,Y) of the bound point seen.
        self.last_bound = tuple()
        # list for the last 3 (X,Y) of the bound points seen.
        self.last_3_bounds = [0, 0, 0]
        self.detected_list = []
        # self.detected_list_length = 0

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
        self.detected_list = self.get_range()
        self.last_bound = inf
        # check if a sensor meet a bounds.
        for idx, dest in enumerate(self.detected_list):
            if maze.get_at(dest) == self.bounds_color:
                self.last_bound = self.detected_list[idx]
                self.detected_list = self.detected_list[:idx]
                # self.detected_list_length = len(self.detected_list)
                print(len(self.detected_list))
                return self.last_bound
        return inf

    def draw(self, maze, game_display):
        """
        draw Lidar over the screen.
        :param game_display: a pygame surface (screen).
        :param maze:
        :return:
        """
        bound = self.check_bounds(maze)
        if self.check_bounds(maze) == () or not type(bound) is tuple:
            pygame.draw.line(game_display, self.color, self.get_cord_start(), self.get_cord_end())
        else:
            # edit the lidar beam length
            wall = self.detected_list[-1] if len(self.detected_list) >= 1 else self.get_cord_start()
            print(wall)
            pygame.draw.line(game_display, self.color, self.get_cord_start(), wall)

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

    def add_last_bound(self, dest):
        """
        short code for implementing a Queue list.
        :param dest:
        :return:
        """
        temp1 = self.last_3_bounds[1]
        temp2 = self.last_3_bounds[2]
        self.last_3_bounds[0] = temp1
        self.last_3_bounds[1] = temp2
        self.last_3_bounds[2] = dest

    def __str__(self):
        list_len = len(self.detected_list)
        return str(list_len) if list_len < 3 else "Infinity"
