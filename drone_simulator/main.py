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
    # windows size by taking the image and get the height/width
    from PIL import Image
    img_path = root_path + "/mazes/"
    img = Image.open(img_path+'p11.png')
    window_width, window_height = img.size
    # initialize Drone
    game_display = Board(width=window_width, height=window_height, color=Colors.white, borders_color=Colors.black)
    # start position
    x = 50
    y = 70
    # initialize Sensors
    lidar_head = Sensor(start_x=x, start_y=y, angle=0, radius=20, color=Colors.red, bounds_color=Colors.maze_black)
    lidar_right = Sensor(start_x=x, start_y=y, angle=45, radius=20, color=Colors.red, bounds_color=Colors.maze_black)
    lidar_left = Sensor(start_x=x, start_y=y, angle=315, radius=20, color=Colors.red, bounds_color=Colors.maze_black)
    lidars = [lidar_head, lidar_right, lidar_left]
    # initialize Drone
    drone = Drone(start_x=x, start_y=x, color=Colors.teal, bounds_color=Colors.maze_black, lidars=lidars, game_display=game_display)
    # read maze image.
    maze = pygame.image.load(os.path.join(root_path, 'mazes', 'p11.png'))

    while True:  # while the program runs.
        # get events and handle.
        for event in pygame.event.get():
            # if clicked on the window's X.
            if event.type == pygame.QUIT:
                pygame.quit()

        # drone keys handle. (move the drone while keys pressed)
        key = pygame.key.get_pressed()
        drone.handle_keys(maze=maze, game_display=game_display.get_screen(), key=key)
        # draw the drone over the screen.
        drone.draw(game_display=game_display.get_screen())
        # update screen display.
        pygame.display.update()
        # update layers over screen.
        pygame.display.flip()
        clock.tick(10)


if __name__ == "__main__":
    main()
