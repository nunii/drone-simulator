import pygame


class Drone:
    factor = 15

    def __init__(self, start_x, start_y, color, bounds_color, odometer):
        self.color = color
        self.bounds_color = bounds_color
        self.x_position = start_x
        self.y_position = start_y
        self.rect = pygame.Rect((self.x_position, self.y_position, Drone.factor, Drone.factor))
        self.odometer = odometer

    def handle_keys(self, maze, game_display):
        """
        handle keys, move a drone by the pressed key.

        :return: true if the drone moves, otherwise false.
        :rtype: boolean
        """
        key = pygame.key.get_pressed()
        # check if the key pressed moved the drone to bounds.
        if self.check_bounds(maze=maze, key_pressed=key, game_display=game_display):
            return False
        # if left key pressed, go left.
        if key[pygame.K_LEFT]:
            self.rect.move_ip(-1, 0)
            # update x position
            self.x_position -= 1
            # # move sensor.
            # self.odometer.move(x_dir=self.x_position, y_dir=self.y_position)
            return True
        # if right key pressed, go right.
        if key[pygame.K_RIGHT]:
            self.rect.move_ip(1, 0)
            # update x position
            self.x_position += 1
            # # move sensor.
            # self.odometer.move(x_dir=self.x_position, y_dir=self.y_position)
            return True
        # if up key pressed,up go left
        if key[pygame.K_UP]:
            self.rect.move_ip(0, -1)
            # update y position
            self.y_position -= 1
            # # move sensor.
            # self.odometer.move(x_dir=self.x_position, y_dir=self.y_position)
            return True
        # if down key pressed, go down.
        if key[pygame.K_DOWN]:
            self.rect.move_ip(0, 1)
            # update y position
            self.y_position += 1
            # # move sensor.
            # self.odometer.move(x_dir=self.x_position, y_dir=self.y_position)
            return True
        return False

    def get_position(self):
        """
        get drone coordinates.

        :return: a coordinates of the drone.
        :rtype: tuple. (x_position, y_position)
        """
        return self.x_position, self.y_position

    def update(self):
        pass

    def check_bounds(self, maze, key_pressed, game_display):
        """
        check if the drone get to bounds.

        :param game_display:
        :param key_pressed: a key pressed.
        :param maze: a background maze.
        :return: true if we reach the bounds (or wall).
        :rtype: boolean
        """
        print('check')
        # check sensor.
        odometer_info = self.odometer.check_bounds(maze=maze)
        # if sensor find a bounds.
        if odometer_info:
            # draw a bounds.
            self.draw_bounds(game_display=game_display, coordination=odometer_info)

        if key_pressed[pygame.K_LEFT] and maze.get_at((self.x_position - 1, self.y_position)) == self.bounds_color:
            # draw a bounds.
            self.draw_bounds(game_display=game_display, coordination=(self.x_position - 5, self.y_position))
            return True
        if key_pressed[pygame.K_RIGHT] and maze.get_at((self.x_position + 1, self.y_position)) == self.bounds_color:
            # draw a bounds.
            self.draw_bounds(game_display=game_display, coordination=(self.x_position + 2, self.y_position))
            return True
        if key_pressed[pygame.K_UP] and maze.get_at((self.x_position, self.y_position - 5)) == self.bounds_color:
            # draw a bounds.
            self.draw_bounds(game_display=game_display, coordination=(self.x_position, self.y_position - 2))
            return True
        if key_pressed[pygame.K_DOWN] and maze.get_at((self.x_position, self.y_position + 5)) == self.bounds_color:
            # draw a bounds.
            self.draw_bounds(game_display=game_display, coordination=(self.x_position, self.y_position + 5))
            return True
        return False

    def draw(self, game_display):
        """draw drone over the screen.

        :param game_display: a pygame surface (screen).
        :return:
        """
        pygame.draw.rect(game_display, self.color, self.rect)

    def draw_bounds(self, game_display, coordination):
        """draw a bounds by the drone observation.

        :param coordination: a drone bounds observation, tuple.
        :param game_display: a main screen.
        :return:
        """
        bounds = pygame.Rect((coordination[0], coordination[1], 15, 15))
        pygame.draw.rect(game_display, self.bounds_color, bounds)

    @staticmethod
    def delete_old_rect(game_display, coordination, color):
        """delete old drone over the screen.

        :param color: a color to draw.
        :param coordination: a drone old coordination, tuple.
        :param game_display: a pygame surface (screen).
        :return:
        """
        background = pygame.Rect((coordination[0], coordination[1], Drone.factor, Drone.factor))
        pygame.draw.rect(game_display, color, background)
