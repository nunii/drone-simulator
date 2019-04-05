from Drone import Drone
from Board import Board
from SnakeBody import SnakeBody
from Food import Food
import pygame
import time
import numpy as np


def main():
    clock = pygame.time.Clock()
    window_width = 910
    window_height = 610
    display_width = 905
    display_height = 605
    game = True

    while game:
        score = 60
        game_display = Board(window_width, window_height)
        drone = Drone(20, 20, 3)
        food = Food(10, display_width, display_height, 10, drone)

        font = pygame.font.SysFont('Time New Roman, Arial', 20)
        text = font.render('Score: %d' % tuple([game_display.game_score]), False, Board.gold)

        x_change = 0
        y_change = 0
        first_time = True
        eat = True
        mov = 0

        data_sets = np.arange(66)

        while True:  # while the program runs.
            for event in pygame.event.get():
                # if clicked on the window's X.
                if event.type == pygame.QUIT:
                    pygame.quit()
                    game = False
                # if a keyboard key has been pressed.
                if event.type == pygame.KEYDOWN:
                    first_time = False
                    # if it was the left arrow
                    if event.key == pygame.K_LEFT:
                        if x_change != 10:
                            x_change = -10
                            y_change = 0
                            mov = 4
                    # if it was the right arrow
                    elif event.key == pygame.K_RIGHT:
                        if x_change != -10:
                            x_change = 10
                            y_change = 0
                            mov = 6
                    # if it was the up arrow
                    elif event.key == pygame.K_UP:
                        if y_change != 10:
                            x_change = 0
                            y_change = -10
                            mov = 8
                    # if it was the down arrow
                    elif event.key == pygame.K_DOWN:
                        if y_change != -10:
                            x_change = 0
                            y_change = 10
                            mov = 2
            # if it's while we haven't clicked anything when the window pops.
            if not first_time:
                drone.update()
            # still need to figure out.--------------
            if score % 10 == 0 and eat:
                drone.append(SnakeBody(drone[len(drone) - 1].x, drone[len(drone) - 1].y))
                print(len(drone))
                eat = False
            drone.move_head(x_change, y_change)  # changes the head's x,y. making it "move"

            if (food.food_x + 10 > drone[0].x >= food.food_x
                    and food.food_y + 10 > drone[0].y >= food.food_y):
                score += 10
                game_display.game_score += 1
                food = Food(10, display_width, display_height, 10, drone)

                eat = True

            if drone.check_death(display_width, display_height):
                if game_display.pop_exit_window(data_sets):
                    break

            game_display.clean()
            # game_display.borders(display_height, display_width)
            pygame.draw.rect(game_display.GAME_display, Board.red,
                             (food.food_x, food.food_y, Drone.factor, Drone.factor))
            drone.draw(game_display.GAME_display)
            game_display.GAME_display.blit(text, (game_display.width - 50, 50))
            pygame.display.flip()
            time.sleep(0.120)
            clock.tick(60)


if __name__ == "__main__":
    main()
