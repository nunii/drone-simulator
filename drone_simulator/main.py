from drone_simulator import Drone
from drone_simulator import Board
from drone_simulator import Colors
from drone_simulator import Sensor
import pygame
import os

#import sys
#sys.setrecursionlimit(100000)  # need to delete this and fix the recursion.

# project root path.
root_path = os.path.dirname(os.path.dirname(__file__))


def main():
    # initialize
    clock = pygame.time.Clock()
    # windows size
    window_width = 910
    window_height = 610
    # initialize Drone
    game_display = Board(width=window_width, height=window_height, color=Colors.white, borders_color=Colors.black)
    # start position
    x = 20
    y = 20
    # initialize Sensors
    lidar_head = Sensor(start_x=x, start_y=y, angle=0, radius=3, color=Colors.red, bounds_color=Colors.maze_black)
    lidar_right = Sensor(start_x=x, start_y=y, angle=45, radius=3, color=Colors.red, bounds_color=Colors.maze_black)
    lidar_left = Sensor(start_x=x, start_y=y, angle=-315, radius=3, color=Colors.red, bounds_color=Colors.maze_black)
    lidars = [lidar_head, lidar_right, lidar_left]
    # initialize Drone
    drone = Drone(start_x=x, start_y=x, color=Colors.teal, bounds_color=Colors.maze_black, lidars=lidars, game_display=game_display)
    # drone coordinate (x, y)
    drone_coordinate = drone.get_position()
    # read maze image.
    maze = pygame.image.load(os.path.join(root_path, 'mazes', 'maze-01.png'))

    while True:  # while the program runs.
        # get events and handle.
        for event in pygame.event.get():
            # if clicked on the window's X.
            if event.type == pygame.QUIT:
                pygame.quit()
        # draw the drone over the screen.
        drone.draw(game_display=game_display.get_screen())
        # drone keys handle. (move the drone while keys pressed)
        key = pygame.key.get_pressed()
        drone.handle_keys(maze=maze, game_display=game_display.get_screen(), key=key)
        # get drone updated coordinates
        drone.get_position()
        # draw the drone over the screen.
        drone.draw(game_display=game_display.get_screen())
        # update screen display.
        pygame.display.update()
        # update layers over screen.
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
