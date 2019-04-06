from drone_simulator import Drone
from drone_simulator import Board
from drone_simulator import Colors
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
    # initialize Board and Drone
    game_display = Board(window_width, window_height)
    drone = Drone(20, 20, Colors.teal, Colors.maze_black)
    # drone coordinate (x, y)
    drone_coordinate = (20, 20)
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
        drone.handle_keys(maze=maze, game_display=game_display.get_screen())
        # print(maze.get_at(drone_coordinate))
        # get drone updated coordinates
        new_drone_coordinate = drone.get_position()
        # the drone is change position
        if new_drone_coordinate != drone_coordinate:
            # delete old position.
            drone.delete_old_rect(game_display=game_display.get_screen(), coordination=drone_coordinate,
                                  color=Colors.white)
        # update drone coordinates
        drone_coordinate = new_drone_coordinate
        # draw the drone over the screen.
        drone.draw(game_display=game_display.get_screen())
        # update screen display.
        pygame.display.update()
        # update layers over screen.
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
