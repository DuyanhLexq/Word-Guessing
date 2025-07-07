import pygame
import threading

class Button:
    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            content: str = None,
            textColor: tuple[int, int, int] = (255, 255, 255),
            textFont: str = None,
            imagePath: str = None,
            borderRadius: float = 0,
            hover: bool = False,
            pathSound: str = None):
        

        self.original_rect = pygame.Rect(x, y, width, height)
        self.rect = self.original_rect.copy()
        self.content = content
        self.textColor = textColor
        self.borderRadius = borderRadius
        self.hover_enabled = hover
        self.image = None
        self.sound = None
        self.pathSound = pathSound

        if imagePath:
            self.image = pygame.image.load(imagePath).convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, (width, height))

        if pathSound:
            self.sound = pygame.mixer.Sound(pathSound)

        if textFont:
            try:
                self.font = pygame.font.SysFont(textFont,int(height * 0.5))
            except:
                self.font = pygame.font.Font(textFont, int(height * 0.5))
        else:
            self.font = pygame.font.SysFont(None, int(height * 0.5))

        self.is_hovered = False
        self.clicked = False
        self.is_pressed = False

    def draw(self, screen: pygame.Surface):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        if self.hover_enabled:
            if self.is_hovered:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Hover and click effects
        if self.hover_enabled and self.is_hovered:
            if self.is_pressed:
                scale_factor = 0.90  # scale down when pressed
            else:
                scale_factor = 0.95  # scale down when hovering
        else:
            scale_factor = 1.0

        scaled_width = int(self.original_rect.width * scale_factor)
        scaled_height = int(self.original_rect.height * scale_factor)
        self.rect.width = scaled_width
        self.rect.height = scaled_height
        self.rect.center = self.original_rect.center

        if self.image:
            scaled_image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
            screen.blit(scaled_image, self.rect)
        else:
            color = (180, 180, 180) if self.is_hovered else (100, 100, 100)
            pygame.draw.rect(screen, color, self.rect, border_radius=int(self.borderRadius))

            if self.content:
                text_surface = self.font.render(self.content, True, self.textColor)
                text_rect = text_surface.get_rect(center=self.rect.center)
                screen.blit(text_surface, text_rect)
        
        
        

    def collidepoint(self,x:float, y:float) -> bool:
        return self.rect.collidepoint(x,y)

    def handle_event(self, event: pygame.event.Event, callback=None,args:tuple = ()):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.is_hovered:
                if self.sound:
                    self.sound.play()
                if callback:
                    callback(*args)
                self.clicked = True
            self.is_pressed = False

    def handle_event_threaded(self, event: pygame.event.Event, callback=None,args:tuple = ()):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.is_hovered:
                if self.sound:
                    self.sound.play()
                if callback:
                    thread = threading.Thread(target=callback, args= args)
                    thread.start()
                self.clicked = True
            self.is_pressed = False