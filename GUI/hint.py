import pygame
from typing import List
from GUI.hintFrame import HintFrame


class Hint(HintFrame):
    def __init__(self,data_list:List, x, y, width, height,screen_width:int ,screen_height:int, bar_width=15, *,
                 waitImage=None, fontPath=None, fontSize=22, fontColor=(0, 0, 0), buttonFont = "arial", buttonFontSize = 24):
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
        self.button_font = pygame.font.SysFont(buttonFont, buttonFontSize)
        self.forward_btn = pygame.Rect(screen_width - 150, screen_height - 60, 120, 40)
        self.back_btn = pygame.Rect(30, screen_height - 60, 120, 40)
    
    def Hint_handle_event(self,event:pygame.event.Event)-> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if self.forward_btn.collidepoint(mx, my):
                if self.current_index < len(self.data_list) - 1:
                    self.current_index += 1
                    self.scroll_offset_x = 0
                    self.scroll_offset_y = 0
                    self.zoom_levels[self.current_index] = 1.0
                    self.adjust_scroll_bars()
                    self.logger.info(f"Navigated to next item: index {self.current_index}")
            elif self.back_btn.collidepoint(mx, my):
                if self.current_index > 0:
                    self.current_index -= 1
                    self.scroll_offset_x = 0
                    self.scroll_offset_y = 0
                    self.zoom_levels[self.current_index] = 1.0
                    self.adjust_scroll_bars()
                    self.logger.info(f"Navigated to previous item: index {self.current_index}")
    def drawButton(self,screen:pygame.Surface) -> None:
        pygame.draw.rect(screen, (0, 100, 255), self.forward_btn, border_radius=8)  # Blue forward button
        pygame.draw.rect(screen, (0, 200, 100), self.back_btn, border_radius=8)     # Green back button
        fwd_text = self.button_font.render("Forward", True, (255, 255, 255))
        back_text = self.button_font.render("Back", True, (255, 255, 255))
        screen.blit(fwd_text, (self.forward_btn.x + 10, self.forward_btn.y + 5))
        screen.blit(back_text, (self.back_btn.x + 25, self.back_btn.y + 5))


    def draw(self,screen:pygame.Surface) -> None:
        super().draw(screen)
        self.drawButton(screen)


