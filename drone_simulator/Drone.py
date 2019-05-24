import pygame
from DroneState import DroneState
from math import cos, sin, radians, inf
from datetime import timedelta
import random


class Drone:
    MAX_SPEED = 3  # meter / sec
    MAX_YAW_SPEED = 180  # deg/sec  (aka  1.0 PI)
    MAX_FLIGHT_TIME = 60 * 5  # 5 Minute
    DT = 1.0 / 50  # ms ==> 50Hz

    def __init__(self, start_x, start_y, color, bounds_color, lidars, game_display):
        self.state = DroneState
        self.yaw = 0
        self.mode = self.state.GROUND
        self.speed = 0
        self.time_in_air = Drone.MAX_FLIGHT_TIME
        self.error_case = 0
        self.score = 0
        self.radius = 3
        self.x_position = start_x
        self.y_position = start_y
        self.lidars = lidars

        self.color = color
        self.bounds_color = bounds_color
        self.game_display = game_display  ## added for testings

    def rotate(self, maze, direction, game_display):
        """rotate the drone.

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
            lidar.add_angle(direction * self.speed)
            lidar.draw(maze=maze, game_display=self.game_display.get_screen())
        self.check_bounds(maze=maze, game_display=game_display)

    def get_position(self):
        """get drone coordinates.

        :return: a coordinates of the drone.
        :rtype: tuple. (x_position, y_position)
        """
        return round(self.x_position), round(self.y_position)

    def check_bounds(self, maze, game_display):
        """check if the drone get to bounds.

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
        # self.speed = 1  # if self.speed < 3 else 0
        # activate first algorithm
        self.second_algorithm(maze=maze, game_display=game_display)

    def set_state(self):
        lidars_states = [len(state.detected_list) for state in self.lidars]
        lidars_states = list(filter(lambda lid: lid == self.lidars[0].radius, lidars_states))
        if self.time_in_air == 0:
            self.state = DroneState.LAND
        elif len(lidars_states) == 3:
            self.state = DroneState.FLY_FAST
            self.forward(acc=2)
        elif len(self.lidars[0].detected_list) <= self.lidars[0].radius // 3:
            self.state = DroneState.MAJOR_BUMP
            self.backward(acc=3)
        elif len(lidars_states) == 1:
            self.state = DroneState.MINOR_BUMP
            self.backward()
        elif len(lidars_states) == 2:
            self.state = DroneState.MINOR_BUMP
            self.backward(0.3)
        else:
            self.state = DroneState.FLY_SLOW
            self.forward()

    def first_algorithm(self, maze, game_display):
        """
        The first Algroithm:
        Move in your current direction untill u meet a wall.
        If u met a wall turn 30degrees to the left or right (mostly right).
        Generated by random.
        :param maze:
        :param game_display:
        :return:
        """
        # generate a number between -1 to 1
        x = random.uniform(-1, 1)
        # if x <= 0 : direction will be -1.  else direction is 1
        x = -1 if x <= -0.6 else 1
        self.move(maze=maze, game_display=game_display) if not self.is_crashed(maze) else None
        # if met a bound at range "distance_from_wall".
        while self.met_a_bound(maze=maze, distance_from_wall=10):
            self.rotate(maze=maze, direction=x, game_display=game_display)

    def second_algorithm(self, maze, game_display):
        """The second Algroithm:
            1. Move in your current direction untill u meet a wall.\n
            1.1 If u met a wall follow the direction of the longest lidar beam.\n
            1.2 If they are all equal turn left or right by random.

        :param maze:
        :param game_display:
        :return:
        """
        self.set_state()
        # if not met a bound at range "distance_from_wall.
        if self.met_a_bound(maze=maze, distance_from_wall=10):
            angle = self.get_max_angle()
            diff_angle = abs(angle - self.lidars[0].angle) % 360
            direction = 1 if (angle - self.lidars[0].angle) % 360 < 180 else -1
            if diff_angle == 0:
                for _ in range(22):
                    self.rotate(maze=maze, direction=direction, game_display=game_display)
            else:
                for _ in range(int(diff_angle // 3)):
                    self.rotate(maze=maze, direction=direction, game_display=game_display)
            self.forward()
        else:
            # move to the direction of the longest lidar beam.
            self.move(maze=maze, game_display=game_display)
        self.is_crashed(maze)

    def forward(self, acc=1.):
        """speed up the drone forward.

        :return:
        """
        n_speed = self.speed + 0.2 * acc
        self.speed = n_speed if n_speed < 3 else 3

    def backward(self, acc=1.):
        """speed up the drone forward.

        :return:
        """
        n_speed = self.speed - 0.2 * acc
        self.speed = n_speed if n_speed > 0 else 0.2

    def handle_keys(self, maze, game_display, key):
        """handle keys, move a drone by the pressed key.

        :return: true if the drone moves, otherwise false.
        :rtype: bool
        """
        self.time_in_air -= 1 / 25 if self.time_in_air > 0 else self.time_in_air
        if self.time_in_air == 0:
            self.state = DroneState.LAND
            return False
        self.check_bounds(maze=maze, game_display=game_display)
        if key[pygame.K_a]:
            self.auto_move(maze=maze, game_display=game_display)
        # if left key pressed, go left.
        if key[pygame.K_LEFT]:
            self.rotate(maze=maze, direction=-1, game_display=game_display)
            return True
        # if right key pressed, go right.
        if key[pygame.K_RIGHT]:
            self.rotate(maze=maze, direction=1, game_display=game_display)
            return True
        # if up key pressed,up go left
        if key[pygame.K_UP]:
            # update y position
            self.forward()
            self.move(maze=maze, game_display=game_display)
            return True
        # if down key pressed, go down.
        if key[pygame.K_DOWN]:
            self.backward()
            self.move(maze=maze, game_display=game_display)
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
        # lst = self.lidars[0].get_range()
            if maze.get_at(lst[-1 * distance_from_wall]) == self.lidars[0].bounds_color:
                return True
        return False

    def is_crashed(self, maze):
        """
        if drone has crashed to wall
        :param maze:
        :return:
        """
        x, y = self.get_position()
        x += self.speed * self.calc_x()
        y += self.speed * self.calc_y()
        if maze.get_at((round(x), round(y))) == self.bounds_color:
            self.error_case += 1
            return True
        return False

    def get_lidar_angles(self):
        return [lidar.angle for lidar in self.lidars]

    def get_lidar_detected_len(self):
        return [len(lidar.detected_list) for lidar in self.lidars]

    def get_max_angle(self):
        choice = random.uniform(0, 1)
        angles = self.get_lidar_angles()
        radius = self.get_lidar_detected_len()
        max_radius_id = radius.index(max(radius))
        max_radius = max(radius)
        radius[max_radius_id] = 0
        sec_max = radius.index(max(radius))
        print(max_radius_id, max_radius, angles[max_radius_id])
        print(sec_max, radius[sec_max], angles[sec_max])
        return angles[max_radius_id] if (max_radius == 30 or abs(max_radius - radius[sec_max]) < 20) and choice < 0.7 \
            else angles[sec_max]

    def get_info_dict(self):
        return {
            'yaw': self.yaw,
            'speed': self.speed,
            'left': self.lidars[2],
            'right': self.lidars[1],
            'head': self.lidars[0],
            'crash': self.error_case,
            'score': self.score,
            'battery': str(timedelta(seconds=self.time_in_air)).split('.')[0]
        }
