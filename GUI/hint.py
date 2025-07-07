import pygame
import consts
from typing import List
from GUI.hintFrame import HintFrame
from GUI.button import Button


class Hint(HintFrame):
    def __init__(self,data_list:List, x, y, width, height,screen_width:int ,screen_height:int, bar_width=15, *,
                 waitImage=None, fontPath=None, fontSize=22, fontColor=(0, 0, 0)):
        super().__init__(
            x,
            y,
            width,
            height,
            bar_width= bar_width,
            waitImage= waitImage,
            fontPath= fontPath,
            fontSize= fontSize,
            fontColor= fontColor
        )
        self.button_font = pygame.font.SysFont(consts.HINT_BUTTON_FONT, consts.HINT_BUTTON_SIZE)
        self.forward_btn = Button(consts.HINT_FORWARD_BUTTON_X_PERCENT*screen_width,consts.HINT_FORWARD_BUTTON_Y_PERCENT*screen_height, 120, 40, "Forward", hover= True,borderRadius= 8)
        self.back_btn = Button(30,screen_height-60, 120, 40, "Back",hover= True,borderRadius= 8)
    
    def forward_btn_func(self):
        if self.current_index < len(self.data_list) - 1:
            self.current_index += 1
            self.scroll_offset_x = 0
            self.scroll_offset_y = 0
            self.zoom_levels[self.current_index] = 1.0
            self.adjust_scroll_bars()
            self.logger.info(f"Navigated to next item: index {self.current_index}")

    def back_btn_func(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.scroll_offset_x = 0
            self.scroll_offset_y = 0
            self.zoom_levels[self.current_index] = 1.0
            self.adjust_scroll_bars()
            self.logger.info(f"Navigated to previous item: index {self.current_index}")
    
    def handleEvent(self,event:pygame.event.Event)-> None:
        super().handle_event(event)
        self.forward_btn.handle_event(event,callback= self.forward_btn_func)
        self.back_btn.handle_event(event, callback= self.back_btn_func)

    def drawButton(self,screen:pygame.Surface) -> None:
        self.back_btn.draw(screen)
        self.forward_btn.draw(screen)


    def draw(self,screen:pygame.Surface) -> None:
        super().draw(screen)
        self.drawButton(screen)


