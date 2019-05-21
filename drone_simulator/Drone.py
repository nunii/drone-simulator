import pygame
from DroneState import DroneState
from math import cos, sin, radians, inf
import random


class Drone:
    MAX_ACC = 2  # meter / sec^2
    MAX_SPEED = 3  # meter / sec
    MAX_YAW_SPEED = 180  # deg/sec  (aka  1.0 PI)
    Max_FLIGHT_TIME = 60 * 5  # 5 Minute
    DT = 1.0/50  # ms ==> 50Hz

    def __init__(self, start_x, start_y, color, bounds_color, lidars, game_display):
        self.state = DroneState
        self.yaw = 0
        self.mode = self.state.GROUND
        self.speed = 0
        self.acc = 0
        self.time_in_air = 0
        self.error_case = 0
        self.score = 0
        self.radius = 3
        self.x_position = start_x
        self.y_position = start_y
        self.lidars = lidars

        self.color = color
        self.bounds_color = bounds_color
        self.game_display = game_display  ## added for testings

    def rotate(self, maze, direction):
        """
        rotate the drone.
        :param direction:
        :param maze:
        :return:
        """

        self.yaw += direction * self.speed
        if self.yaw >= 360:
            self.yaw = self.yaw % 360
        elif self.yaw < 0:
            self.yaw = 360 + self.yaw

        for lidar in self.lidars:
            lidar.add_angle(direction*self.speed)
            lidar.draw(maze=maze, game_display=self.game_display.get_screen())

    def get_position(self):
        """
        get drone coordinates.
        :return: a coordinates of the drone.
        :rtype: tuple. (x_position, y_position)
        """
        return round(self.x_position), round(self.y_position)

    def check_bounds(self, maze, game_display):
        """
        check if the drone get to bounds.
        :param game_display: a screen object.
        :param maze: a background maze.
        :return: true if we reach the bounds (or wall).
        :rtype: boolean
        """
        for lidar in self.lidars:
            # check sensor.
            lidar_info = lidar.check_bounds(maze=maze)
            # if sensor find a bounds.
            if type(lidar_info) is tuple:
                # draw a bounds.
                self.draw_bounds(game_display=game_display, coordination=lidar_info)

        if maze.get_at((int(self.x_position), int(self.y_position))) == self.bounds_color:
            self.error_case += 1
        return False

    def draw(self, game_display):
        """
        draw drone over the screen.
        :param game_display: a pygame surface (screen).
        :return:
        """
        pygame.draw.circle(game_display, self.color, self.get_position(), self.radius)

    def draw_bounds(self, game_display, coordination):
        """
        draw a bounds by the drone observation.
        :param coordination: a drone bounds observation, tuple.
        :param game_display: a main screen.
        :return:
        """
        pygame.draw.circle(game_display, self.bounds_color, coordination, 3)

    def change_lidars_positions(self, maze, game_display):
        """
        change lidars positions and draw.
        :param game_display:
        :param maze:
        :return:
        """
        for lidar in self.lidars:
            lidar.move(coordinate=self.get_position())
            lidar.draw(maze=maze, game_display=game_display)

    def calc_x(self):
        return cos(radians(self.yaw)) * self.radius

    def calc_y(self):
        return sin(radians(self.yaw)) * self.radius

    def move(self, game_display, maze):
        self.x_position += self.speed * self.calc_x()
        self.y_position += self.speed * self.calc_y()
        # update odometer position.
        self.change_lidars_positions(maze=maze, game_display=game_display)

    def auto_move(self, game_display, maze):
        """
        Implement the autonomous algorithms
        :param game_display:
        :param maze:
        :return:
        """
        self.speed = 1  # if self.speed < 3 else 0
        # activate first algorithm
        self.first_algorithm(maze=maze, game_display=game_display)

    def first_algorithm(self, maze, game_display):
        """
        The first algroithm:
        Move in your current direction untill u meet a wall.
        If u met a wall turn 30degrees to the left or right.
        :param maze:
        :param game_display:
        :return:
        """
        # generate a number between -1 to 1
        x = random.uniform(-1, 1)
        # if x <= 0 : direction will be -1.  else direction is 1
        x = -1 if x <= 0 else 1
        self.move(maze=maze, game_display=game_display) if not self.crashed(maze) else None
        # if met a bound at range "distance_from_wall.
        while self.met_a_bound(maze=maze, distance_from_wall=10):
            self.rotate(maze=maze, direction=x)
        self.check_bounds(maze=maze, game_display=game_display)

    def handle_keys(self, maze, game_display, key):
        """
        handle keys, move a drone by the pressed key.
        :return: true if the drone moves, otherwise false.
        :rtype: bool
        """
        if key[pygame.K_a]:
            self.auto_move(maze=maze, game_display=game_display)
        # if left key pressed, go left.
        if key[pygame.K_LEFT]:
            self.rotate(maze=maze, direction=-1)
            self.check_bounds(maze=maze, game_display=game_display)
            return True
        # if right key pressed, go right.
        if key[pygame.K_RIGHT]:
            self.rotate(maze=maze, direction=1)
            self.check_bounds(maze=maze, game_display=game_display)
            return True
        # if up key pressed,up go left
        if key[pygame.K_UP]:
            # update y position
            self.speed += 1 if self.speed < 3 else 0
            self.move(maze=maze, game_display=game_display)
            self.check_bounds(maze=maze, game_display=game_display)
            return True
        # if down key pressed, go down.
        if key[pygame.K_DOWN]:
            self.speed -= 1 if self.speed > 0 else 0
            self.move(maze=maze, game_display=game_display)
            self.check_bounds(maze=maze, game_display=game_display)
            return True
        return False

    def met_a_bound(self, maze, distance_from_wall):
        """
        A function to check if met a bound at range "distance_from_wall"
        :param maze:
        :param distance_from_wall:
        :return: bool
        :rtype: bool
        """
        for lidar in self.lidars:
            lst = lidar.get_range()
            if maze.get_at(lst[-1 * distance_from_wall]) == lidar.bounds_color:
                return True
        return False

    def crashed(self, maze):
        """
        if dron has crashed to wall
        :param maze:
        :return:
        """
        if maze.get_at(self.get_position()) == self.bounds_color:
            print("crashed into a wall")
            return True
        return False
