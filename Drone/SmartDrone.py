from Drone import Drone
from Drone import DroneState
from random import uniform
import pygame
import math


class SmartDrone(Drone):
    """
    Smart-Drone, a drone which can make it's own decision in a maze.\n
    """
    def __init__(self, start_x, start_y, color, bounds_color, lidars: list):
        """Smart-Drone initialize.

        :param start_x: a x start point in a maze.
        :param start_y: a y start point in a maze.
        :param color: a drone color.
        :param bounds_color: a bounds color
        :param lidars: a list of lidars. (list of Sensor object)
        """
        Drone.__init__(self, start_x, start_y, color, bounds_color, lidars)
        self.auto_flag = False
        self.stuck = False
        self.last_cord = tuple

    def auto_move(self, game_display, maze):
        """Implements of the algorithm:
            1. Set a state (LAND, FLY_FAST, MAJOR_BUMP, MINOR_BUMP, FLY_SLOW).\n
            2. Move in your current direction until one of your liadrs meet a wall in their quarter radius.\n
            2.1 If u met a wall follow the direction of the longest lidar beam.\n
            2.2 If they are all equal turn left or right by random.

        :param maze: a background maze.
        :param game_display: a pygame surface (screen).
        """
        self.set_state()
        if self.stuck:
            for _ in range(160):
                angle = self.get_max_angle()
                diff_angle = (angle - self.lidars[0].angle) % 360
                direction = 1 if diff_angle < 180 else -1
                self.rotate(maze=maze, direction=direction, game_display=game_display)
        # if not met a bound at range "distance_from_wall.
        if self.is_met_a_bound(maze=maze, distance_from_wall=10):
            angle = self.get_max_angle()
            diff_angle = (angle - self.lidars[0].angle) % 360
            direction = 1 if diff_angle < 180 else -1
            if diff_angle == 0:
                for _ in range(20):
                    direction = 1 if uniform(0, 1) < 0.7 else -1
                    self.rotate(maze=maze, direction=direction, game_display=game_display)
            else:
                for _ in range(int(diff_angle * 0.7)):
                    self.rotate(maze=maze, direction=direction, game_display=game_display)
        else:
            # move to the direction of the longest lidar beam.
            self.move(maze=maze, game_display=game_display)
        self.is_crashed(maze)

    def set_state(self):
        """Set Drone state according to lidars info.\n
        States:
            * LAND - if battery if over.
            * FLY_FAST - if all lidars returns infinity.
            * MAJOR_BUMP - if the head lidar is sees a wall in the range of  one-third.
            * MINOR_BUMP - if one lidar return infinity.
            * FLY_SLOW - otherwise.
        """
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
        else:
            self.state = DroneState.FLY_SLOW
            self.forward()

    def handle_keys(self, maze, game_display, key):
        """handle keys, move a drone by the pressed key.

        :return: true if the drone moves, otherwise false.
        :rtype: bool
        """
        # get position every 5 sec.
        if self.time_in_air % 5 == 0:
            self.last_cord = self.get_position()

        Drone.handle_keys(self, maze, game_display, key)
        if self.auto_flag:
            if self.state == DroneState.LAND and self.time_in_air > 0:
                self.state = DroneState.TAKE_OFF
            self.auto_move(maze=maze, game_display=game_display)
        if key[pygame.K_a]:
            self.auto_move(maze=maze, game_display=game_display)
        if key[pygame.K_d] and self.time_in_air > 0:
            self.auto_flag = True
        if key[pygame.K_s]:
            self.auto_flag = False
            self.state = DroneState.LAND
        return False

    def is_stuck(self):
        x1, y1 = self.get_position()
        x2, y2 = self.last_cord
        expression = math.pow(x1-x2, 2) + math.pow(y1-y2, 2)
        if round(math.sqrt(expression)) >= 5:
            self.stuck = True

    def is_met_a_bound(self, maze, distance_from_wall):
        """A function to check if met a bound at range "distance_from_wall"

        :param maze: a background maze.
        :param distance_from_wall: a safety distance constant.
        :return: if one of the lidars sees a wall in a one-quarter radius.
        :rtype: bool
        """
        # generate a number between -1 to 1
        # x = random.uniform(0, 1)
        # if x > 0.6:
        for lidar in self.lidars:
            if len(lidar.detected_list) < lidar.radius // 4:
                return True

                # lst = lidar.get_range()
                # if maze.get_at(lst[-1 * distance_from_wall]) == self.lidars[0].bounds_color:
                #     return True
        # else:
        #     lst = self.lidars[0].get_range()
        #     if maze.get_at(lst[-1 * distance_from_wall]) == self.lidars[0].bounds_color:
        #         return True
        return False

    def get_lidar_angles(self):
        """collect current angels from lidars.

        :return: an angels list.
        :rtype: list
        """
        return [lidar.angle for lidar in self.lidars]

    def get_lidar_detected_len(self):
        """collect current detected points from lidars.

        :return: an detected points.
        :rtype: list
        """
        return [len(lidar.detected_list) for lidar in self.lidars]

    def get_max_angle(self):
        """get the angle from the longest detected points from lidars.

        :return: an angle.
        :rtype: float
        """
        # get sensors angles.
        angles = self.get_lidar_angles()
        # get lidars radius of detected bounds.
        radius = self.get_lidar_detected_len()
        # get lidar id, max radius.
        max_radius_id = radius.index(max(radius))
        # get lidar max radius, value.
        max_radius = max(radius)
        # change max radius to -1 for find the second max.
        radius[max_radius_id] = -1
        # find second max id.
        sec_max_id = radius.index(max(radius))
        if (max_radius == 30 or abs(max_radius - radius[sec_max_id]) > 10) and uniform(0, 1) < 0.7:
            return angles[max_radius_id]
        else:
            return angles[sec_max_id]
