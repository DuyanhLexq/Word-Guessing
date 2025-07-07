import pygame
import threading
import io
import time
import consts
import logging
from GUI.hint import Hint
from core.logger import log
from GUI.button import Button
# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = consts.SCREEN_HEIGHT

# Set up the display
pygame.display.set_caption(consts.GAME_CAPTION)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_play = True
clock = pygame.time.Clock()

# Create a main logger for the application
main_logger = log("Main", level=logging.INFO)
main_logger.info("Game started")

# ----- HintFrame Class -----


# ----- Initialize HintFrame -----
frame_width = int(SCREEN_WIDTH * 0.5)
frame_height = int(SCREEN_HEIGHT * 0.7)
frame_x = int(SCREEN_WIDTH * 0.02)
frame_y = int(SCREEN_HEIGHT * 0.1)


data_list = [
    open("test.txt",encoding="utf-8").read()[:int(1e3)],
    open(r"C:\Project_Python\applications\Word-Guessing\assets\images\u.png", 'rb').read(),
    "Another string of text here.",
]
newHint = Hint(data_list,frame_x,frame_y,frame_width,frame_height,SCREEN_WIDTH,SCREEN_HEIGHT,
               waitImage=consts.HINT_FRAME_LOADING_IMAGE_PATH,
    fontPath=consts.HINT_FRAME_TEXT_FONT_PATH,
    fontSize=consts.HINT_FRAME_TEXT_SIZE,
    fontColor=consts.HINT_FRAME_TEXT_COLOR
               )

# ----- Data List -----


newHint.data_list = data_list
newHint.preload_all_data()

# ----- Forward/Back Buttons -----
font = pygame.font.SysFont("arial", 24)
forward_btn = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 60, 120, 40)
back_btn = pygame.Rect(30, SCREEN_HEIGHT - 60, 120, 40)



# ----- Main Game Loop -----
while game_play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_logger.info("Quit event detected")
            game_play = False
        else:
            newHint.handleEvent(event)

    # Clear the screen
    screen.fill(consts.DEFAULT_BACKGROUND_COLOR)
    # Update and draw the frame
    newHint.update()
    newHint.draw(screen)

    # Update the display
    pygame.display.update()
    clock.tick(consts.FPS)

# Log game exit and quit Pygame
main_logger.info("Game stopped")
pygame.quit()