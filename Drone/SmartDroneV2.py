from Drone import Drone
from Drone import DroneState
from SLAMGraph import SLAMGraph
import pygame
from math import isinf
from random import uniform


class SmartDroneV2(Drone):
    """
    Smart-DroneV2, a drone which can make it's own decision in a maze.\n
    Drone use head lidar to decide which speed to use, and left and right
    lidars to rotate.
    Except when head lidar is very close(distance from a wall is less then 1/3)
    to a wall, then rotate.
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
        self.slam = SLAMGraph()
        self.distance = 0
        self.last_point_name = 'home'
        self.slam.add_point(name=self.last_point_name, data={'angle': self.yaw,
                                                             'duration': 0,
                                                             'time': self.time_in_air})
        self.last_check = self.lidars[0].radius if isinf(self.lidars[0].get_sense()) else self.lidars[0].get_sense()

    def handle_keys(self, maze, game_display, key):
        """handle keys, move a drone by the pressed key.

        :return: true if the drone moves, otherwise false.
        :rtype: bool
        """
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
            self.state = DroneState.LAND
        if key[pygame.K_w]:
            self.slam.show()
        return False

    def auto_move(self, maze, game_display):
        """Implements of the algorithm:
            1. an head lidar indicate infinity - fly fast.
            2. an head lidar indicate 1m - bump fast and rotate.
            3. an head lidar indicate between 1m-2m - fly slowly.
            4. an head lidar indicate between 2m-3m - fly regular.
            5. an right lidar indicate less then infinity - rotate left 20 degree.
            6. an left lidar indicate less then infinity - rotate right 20 degree.

        :param maze:
        :param game_display:
        :return:
        """
        self.is_interesting()
        self.rotates(maze=maze, game_display=game_display)
        self.move(game_display=game_display, maze=maze)
        self.distance += self.speed

    def get_duration(self, current_time):
        """compute duration between current time and last time.

        :param current_time: int, a current time in seconds.
        :return: a duration since last time.
        :rtype: int
        """
        return current_time - self.slam.get_data(node_name=self.last_point_name)['time']

    def is_interesting(self):
        """check if happens somethings interesting add it to SLAM graph."""
        current_time = self.time_in_air
        if self.last_point_name == 'home':
            new_name = 'node 1'
        else:
            new_name = 'node {0}'.format(int(self.last_point_name.split()[1]) + 1)
        new_sense = self.lidars[0].radius if isinf(self.lidars[0].get_sense()) else self.lidars[0].get_sense()

        if abs(new_sense - self.last_check) >= 9 * self.lidars[0].radius / 10:
            self.slam.add_point(name=new_name, data={'angle': self.yaw,
                                                     'duration': self.get_duration(current_time=current_time),
                                                     'time': current_time})
            self.slam.add_edge(from_node=self.last_point_name, to_node=new_name, distance=self.distance)
            self.distance = 0
            self.last_point_name = new_name

    def move(self, game_display, maze):
        """move forward or backward.
        fly fast - an head lidar indicate infinity.
        fly regular - an head lidar indicate between 2m-3m.
        fly slowly - an head lidar indicate between 1m-2m.
        bump fast - an head lidar indicate 1m.

        :param game_display:
        :param maze:
        :return:
        """
        if isinf(self.lidars[0].get_sense()):
            self.forward(acc=2)
        elif self.lidars[0].get_sense() >= 2 * self.lidars[0].radius // 3:
            self.backward(acc=0.5)
        elif self.lidars[0].get_sense() >= self.lidars[0].radius // 3:
            self.backward()
        else:
            self.backward(acc=2)
        Drone.move(self, game_display=game_display, maze=maze)

    def rotates(self, maze, game_display):
        """rotate drone. (Yaw)
        rotate right or left  - an head lidar indicate 1m.
        rotate left 20 degree - an right lidar indicate less then infinity.
        rotate right 20 degree - an left lidar indicate less then infinity.

        :param maze:
        :param game_display:
        :return:
        """
        if self.lidars[0].get_sense() <= self.lidars[0].radius // 3:
            if uniform(0, 1) > 0.7:
                self.rotate_right(angle=45, maze=maze, game_display=game_display)
            else:
                self.rotate_left(angle=45, maze=maze, game_display=game_display)
        # fix to left.
        if self.lidars[1].get_sense() <= 2 * self.lidars[1].radius // 3:
            self.rotate_left(angle=10, maze=maze, game_display=game_display)
        # fix to right.
        if self.lidars[2].get_sense() <= 2 * self.lidars[0].radius // 3:
            self.rotate_right(angle=10, maze=maze, game_display=game_display)

    def rotate_right(self, angle, maze, game_display):
        """rotate drone in some angle to the right.

        :param angle: an angle to rotate.
        :param maze: a background maze.
        :param game_display: a pygame surface (screen).
        :return:
        """
        for _ in range(angle):
            self.rotate(maze=maze, direction=1, game_display=game_display)

    def rotate_left(self, angle, maze, game_display):
        """rotate drone in some angle to the left.

        :param angle: an angle to rotate.
        :param maze: a background maze.
        :param game_display: a pygame surface (screen).
        :return:
        """
        for _ in range(angle):
            self.rotate(maze=maze, direction=-1, game_display=game_display)
