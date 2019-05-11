import pygame
from DroneState import DroneState


class Drone:
    MAX_ACC = 2  # meter / sec^2
    MAX_SPEED = 3  # meter / sec
    MAX_YAW_SPEED = 180  # deg/sec  (aka  1.0 PI)
    Max_FLIGHT_TIME = 60 * 5  # 5 Minute
    DT = 1.0/50  # ms ==> 50Hz

    def __init__(self, start_x, start_y, color, bounds_color, lidars):
        self.state = DroneState
        self.yaw = 0
        self.yaw_speed = 0
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

    def rotate(self, direction):
        """

        :param direction:
        :return:
        """
        self.yaw += direction * self.yaw_speed
        for lidar in self.lidars:
            lidar.angle = self.yaw
            lidar.draw()

    def get_position(self):
        """
        get drone coordinates.

        :return: a coordinates of the drone.
        :rtype: tuple. (x_position, y_position)
        """
        return self.x_position, self.y_position

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
            if lidar_info:
                # draw a bounds.
                self.draw_bounds(game_display=game_display, coordination=lidar_info)

        if maze.get_at((self.x_position, self.y_position)) == self.bounds_color:
            self.error_case += 1
        return False

    def draw(self, game_display):
        """draw drone over the screen.

        :param game_display: a pygame surface (screen).
        :return:
        """
        pygame.draw.circle(game_display, self.color, self.get_position(), self.radius)

    def draw_bounds(self, game_display, coordination):
        """draw a bounds by the drone observation.

        :param coordination: a drone bounds observation, tuple.
        :param game_display: a main screen.
        :return:
        """
        pygame.draw.circle(game_display, self.bounds_color, coordination, 3)

    def change_lidars_positions(self, game_display):
        """change lidars positions and draw.

        :param game_display:
        :return:
        """
        for lidar in self.lidars:
            lidar.move(coordinate=self.get_position())
            lidar.draw(game_display=game_display)

    def handle_keys(self, maze, game_display, key):
        """
        handle keys, move a drone by the pressed key.

        :return: true if the drone moves, otherwise false.
        :rtype: boolean
        """
        # if left key pressed, go left.
        if key[pygame.K_LEFT]:
            self.rotate(-1)
            self.check_bounds(maze=maze, game_display=game_display)
            return True
        # if right key pressed, go right.
        if key[pygame.K_RIGHT]:
            self.rotate(1)
            self.check_bounds(maze=maze, game_display=game_display)
            return True
        # if up key pressed,up go left
        if key[pygame.K_UP]:
            # update y position
            self.speed += 1 if self.speed < 3 else 0
            # update odometer position.
            self.change_lidars_positions(game_display=game_display)
            return True
        # if down key pressed, go down.
        if key[pygame.K_DOWN]:
            self.speed -= 1 if self.speed > 0 else 0
            # update odometer position.
            self.change_lidars_positions(game_display=game_display)
            return True
        return False

