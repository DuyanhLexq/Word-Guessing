import pygame
import threading
import io
import time
import consts
import logging
from GUI.hint import Hint
from core.logger import log
from GUI.button import Button
from GUI.label import Label
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
frame_height = int(SCREEN_HEIGHT * 0.8)
frame_x = int(SCREEN_WIDTH * 0.02)
frame_y = int(SCREEN_HEIGHT * 0.05)


data_list = [
    open("test.txt",encoding="utf-8").read(),
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
x,y = consts.LEVEL_LABLE_X_PERCENT *SCREEN_WIDTH,consts.LEVEL_LABLE_Y_PERCENT*SCREEN_HEIGHT
size = [consts.LEVEL_LABEL_WIDTH_PERCENT*SCREEN_WIDTH, consts.LEVEL_LABEL_HEIGHT_PERCENT*SCREEN_HEIGHT]
modelabel = Label(x,y,*size,content=f"{consts.LEVEL_LABLE_CONTENT} {consts.LEVEL_TEXTS[2]}",font= consts.HINT_FRAME_TEXT_FONT_PATH,borderRadius= 8,bgColor= consts.LEVEL_LABEL_BG_COLOR)



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
    modelabel.draw(screen)


    # Update the display
    pygame.display.update()
    clock.tick(consts.FPS)

# Log game exit and quit Pygame
main_logger.info("Game stopped")
pygame.quit()