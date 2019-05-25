from Drone import DroneFactory
from drone_simulator import Board
from drone_simulator import Colors
from Sensor import Sensor
from PIL import Image
import pygame
import os

# project root path.
root_path = os.path.dirname(os.path.dirname(__file__))


def main():
    # initialize
    clock = pygame.time.Clock()
    # windows size by taking the image and get the height/width
    img_path = root_path + "/mazes/"
    maze_name = 'p12.png'
    img = Image.open(img_path + maze_name)
    window_width, window_height = img.size
    window_height += 30
    # initialize Drone
    game_display = Board(width=window_width, height=window_height, color=Colors.white, borders_color=Colors.black)
    # start position
    x = 80
    y = 20
    # initialize Sensors
    lidar_head = Sensor(start_x=x, start_y=y, angle=0, radius=30, color=Colors.red, bounds_color=Colors.maze_black)
    lidar_right = Sensor(start_x=x, start_y=y, angle=45, radius=30, color=Colors.red, bounds_color=Colors.maze_black)
    lidar_left = Sensor(start_x=x, start_y=y, angle=315, radius=30, color=Colors.red, bounds_color=Colors.maze_black)
    lidars = [lidar_head, lidar_right, lidar_left]
    # initialize Drone
    drone = DroneFactory.create_drone("SmartDrone")(start_x=x,
                                                    start_y=x,
                                                    color=Colors.teal,
                                                    bounds_color=Colors.maze_black,
                                                    lidars=lidars)
    # read maze image.
    maze = pygame.image.load(os.path.join(root_path, 'mazes', maze_name))
    while True:  # while the program runs.
        # get events and handle.
        event = [e.type for e in pygame.event.get()]
        # if clicked on the window's X.
        if pygame.QUIT in event:
            game_display.close()
            break
        # drone keys handle. (move the drone while keys pressed)
        key = pygame.key.get_pressed()
        drone.handle_keys(maze=maze, game_display=game_display.get_screen(), key=key)
        # draw the drone over the screen.
        drone.draw(game_display=game_display.get_screen())
        # update layers over screen.
        game_display.update_text(drone.get_info_dict())
        # update screen display.
        pygame.display.update()
        pygame.display.flip()
        game_display.time += 1 / 25
        clock.tick(25)


if __name__ == "__main__":
    main()
