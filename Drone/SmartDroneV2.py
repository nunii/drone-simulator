from Drone import Drone
from Drone import DroneState
import pygame


class SmartDrone(Drone):
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
        pass

