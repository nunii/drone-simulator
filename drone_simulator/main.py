from drone_simulator import Drone
from drone_simulator import Board
from drone_simulator import Colors
import pygame
import numpy as np


def main():
    # initialize
    clock = pygame.time.Clock()
    # windows size
    window_width = 910
    window_height = 610
    # initialize Board and Drone
    game_display = Board(window_width, window_height)
    drone = Drone(20, 20, Colors.teal)
    # drone coordinate (x, y)
    drone_coordinate = (20, 20)

    while True:  # while the program runs.
        # get events and handle.
        for event in pygame.event.get():
            # if clicked on the window's X.
            if event.type == pygame.QUIT:
                pygame.quit()
        # draw the drone over the screen.
        drone.draw(game_display=game_display.get_screen())
        # drone keys handle. (move the drone while keys pressed)
        drone.handle_keys()
        # get drone updated coordinates
        new_drone_coordinate = drone.get_position()
        # the drone is change position
        if new_drone_coordinate != drone_coordinate:
            # delete old position.
            drone.delete_old_rect(game_display=game_display.get_screen(), coordination=drone_coordinate,
                                  color=Colors.white)
        # update drone coordinates
        drone_coordinate = new_drone_coordinate
        # update screen display.
        pygame.display.update()
        # update layers over screen.
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
