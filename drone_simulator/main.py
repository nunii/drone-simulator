from drone_simulator import Drone
from drone_simulator import Board
from drone_simulator import Colors
from drone_simulator import Sensor
from math import cos, sin
import pygame
import os

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
    # initialize Sensor
    odometer = Sensor(start_x=20 + sin(45)*20, start_y=20 + cos(45)*20, color=Colors.red, bounds_color=Colors.maze_black)
    # initialize Drone
    drone = Drone(start_x=20, start_y=20, color=Colors.teal, bounds_color=Colors.maze_black, odometer=odometer)
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
        # draw the drone over the screen.
        odometer.draw(game_display=game_display.get_screen())
        # drone keys handle. (move the drone while keys pressed)
        drone.handle_keys(maze=maze, game_display=game_display.get_screen())
        # get drone updated coordinates
        new_drone_coordinate = drone.get_position()
        # the drone is change position
        if new_drone_coordinate != drone_coordinate:
            # delete old position.
            drone.delete_old_rect(game_display=game_display.get_screen(), coordination=drone_coordinate,
                                  color=Colors.white)
            pygame.PixelArray(game_display.get_screen()).replace(color=Colors.red, repcolor=Colors.white)
        # update drone coordinates
        drone_coordinate = new_drone_coordinate
        # draw the drone over the screen.
        drone.draw(game_display=game_display.get_screen())
        # draw the drone over the screen.
        odometer.draw(game_display=game_display.get_screen())
        # update screen display.
        pygame.display.update()
        # update layers over screen.
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
