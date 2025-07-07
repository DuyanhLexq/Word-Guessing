import pygame
import threading
import io
import time
import logging
from core.logger import log

class HintFrame:
    """
    A custom frame widget for displaying text or images with scroll bars and zoom functionality.
    """
    def __init__(self, x, y, width, height, bar_width=15, *,
                 waitImage=None, fontPath=None, fontSize=22, fontColor=(0, 0, 0)):
        """
        Initialize the HintFrame.

        Args:
            x (int): X-coordinate of the frame's top-left corner.
            y (int): Y-coordinate of the frame's top-left corner.
            width (int): Width of the frame.
            height (int): Height of the frame.
            bar_width (int, optional): Width of the scroll bars. Defaults to 15.
            waitImage (str, optional): Path to an image to display while loading. Defaults to None.
            fontPath (str, optional): Path to a font file. Defaults to None (uses Arial).
            fontSize (int, optional): Font size for text. Defaults to 22.
            fontColor (tuple, optional): RGB color tuple for text. Defaults to (0, 0, 0).
        """
        # Set up logging for this instance
        self.logger = log("GUI.hintFrame", level=logging.INFO)
        self.logger.info("Initializing HintFrame")

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Create a surface with alpha support (RGBA)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Set background color (light gray with transparency)
        self.bg_color = (150, 150, 150, 100)

        # Define scroll bar areas
        self.bar_width = bar_width
        self.scroll_area_y = pygame.Rect(self.width - bar_width, 0, bar_width, self.height)  # Vertical scroll area
        self.scroll_area_x = pygame.Rect(0, self.height - bar_width, self.width, bar_width)  # Horizontal scroll area

        # Initialize scroll bars (rounded, dark gray)
        self.bar_rect_y = pygame.Rect(self.width - bar_width, 0, bar_width, 50)  # Vertical bar
        self.bar_rect_x = pygame.Rect(0, self.height - bar_width, 50, bar_width)  # Horizontal bar
        self.bar_color = (100, 100, 100)

        # Dragging state
        self.dragging_y = False
        self.dragging_x = False
        self.last_mouse_y = 0
        self.last_mouse_x = 0

        # Data storage
        self.data_list = []  # List of text strings or image bytes
        self.renders = []    # List of rendered surfaces or None
        self.current_index = 0  # Index of the currently displayed item

        # Load font with error handling
        try:
            if fontPath:
                self.font = pygame.font.Font(fontPath, fontSize)
            else:
                self.font = pygame.font.SysFont("arial", fontSize)
        except Exception as e:
            self.logger.error(f"Failed to load font: {e}. Falling back to Arial.")
            self.font = pygame.font.SysFont("arial", fontSize)
        self.font_color = fontColor

        # Scroll offsets
        self.scroll_offset_y = 0
        self.scroll_offset_x = 0

        # Zoom levels for images
        self.zoom_levels = {}

        # Load placeholder image or create a default one
        if waitImage:
            try:
                img = pygame.image.load(waitImage).convert_alpha()
                img = pygame.transform.smoothscale(img, (self.width - bar_width, self.height - bar_width))
                self.placeholder = img
            except Exception as e:
                self.logger.error(f"Failed to load waitImage: {e}. Using default placeholder.")
                self.placeholder = pygame.Surface((self.width - bar_width, self.height - bar_width), pygame.SRCALPHA)
                self.placeholder.fill((100, 100, 100, 100))
        else:
            self.placeholder = pygame.Surface((self.width - bar_width, self.height - bar_width), pygame.SRCALPHA)
            self.placeholder.fill((100, 100, 100, 100))

    def preload_all_data(self):
        """
        Preload all data items asynchronously using threads.

        For images, loads from bytes; for text, renders to a surface.
        """
        self.logger.info("Preloading all data items")
        def load_task(index, data):
            time.sleep(0.5 + index * 0.2)  # Simulate loading delay
            if isinstance(data, bytes):
                # Load image from bytes
                try:
                    img_surface = pygame.image.load(io.BytesIO(data)).convert_alpha()
                    self.logger.info(f"Loaded image at index {index}")
                except Exception as e:
                    self.logger.error(f"Failed to load image at index {index}: {e}")
                    img_surface = self.render_text_surface("[Invalid Image]", (255, 0, 0))
                self.renders[index] = img_surface
            else:
                # Render text
                text_surface = self.render_text_surface(str(data), self.font_color)
                self.renders[index] = text_surface
                self.logger.info(f"Rendered text at index {index}")
            if index == self.current_index:
                self.adjust_scroll_bars()

        for i, data in enumerate(self.data_list):
            self.renders.append(None)
            threading.Thread(target=load_task, args=(i, data), daemon=True).start()

    def render_text_surface(self, text, color):
        """
        Render text into a surface with word wrapping.

        Args:
            text (str): The text to render.
            color (tuple): RGB color tuple for the text.

        Returns:
            pygame.Surface: The rendered text surface.
        """
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] < self.width - self.bar_width - 10:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        line_height = self.font.get_height() + 4
        text_height = line_height * len(lines)
        text_surf = pygame.Surface((self.width - self.bar_width, text_height), pygame.SRCALPHA)
        y = 0
        for line in lines:
            rendered_line = self.font.render(line, True, color)
            text_surf.blit(rendered_line, (0, y))
            y += line_height
        return text_surf

    def adjust_scroll_bars(self):
        """
        Adjust the size of scroll bars based on the content dimensions.
        """
        surface = self.renders[self.current_index]
        if surface:
            zoom = self.zoom_levels.get(self.current_index, 1.0)
            content_height = int(surface.get_height() * zoom)
            content_width = int(surface.get_width() * zoom)

            # Adjust vertical scroll bar
            if content_height <= self.height:
                self.bar_rect_y.height = self.height
            else:
                ratio_y = self.height / content_height
                self.bar_rect_y.height = max(30, self.height * ratio_y)

            # Adjust horizontal scroll bar
            if content_width <= self.width:
                self.bar_rect_x.width = self.width
            else:
                ratio_x = self.width / content_width
                self.bar_rect_x.width = max(30, self.width * ratio_x)

    def handle_event(self, event):
        """
        Handle Pygame events such as mouse clicks and scrolling.

        Args:
            event (pygame.event.Event): The event to process.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handle mouse button presses
            mx, my = pygame.mouse.get_pos()
            local_x = mx - self.x
            local_y = my - self.y
            if event.button == 1:  # Left click
                if self.bar_rect_y.collidepoint(local_x, local_y):
                    self.dragging_y = True
                    self.last_mouse_y = local_y
                    self.logger.info("Started dragging vertical scroll bar")
                elif self.bar_rect_x.collidepoint(local_x, local_y):
                    self.dragging_x = True
                    self.last_mouse_x = local_x
                    self.logger.info("Started dragging horizontal scroll bar")

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.dragging_y:
                    self.dragging_y = False
                    self.logger.info("Stopped dragging vertical scroll bar")
                if self.dragging_x:
                    self.dragging_x = False
                    self.logger.info("Stopped dragging horizontal scroll bar")

        elif event.type == pygame.MOUSEWHEEL:
            mods = pygame.key.get_mods()
            if mods & pygame.KMOD_CTRL and isinstance(self.data_list[self.current_index], bytes):
                # Zoom with Ctrl + mouse wheel (for images only)
                zoom = self.zoom_levels.get(self.current_index, 1.0)
                zoom += event.y * 0.1
                zoom = max(0.1, min(5.0, zoom))
                self.zoom_levels[self.current_index] = zoom
                self.adjust_scroll_bars()
                self.logger.info(f"Zoomed to {zoom:.2f} on image at index {self.current_index}")
            else:
                # Scroll vertically
                self.scroll_offset_y += -event.y * 20
                self.clamp_scroll_offsets()
                self.update_bar_positions()
                self.logger.info("Scrolled vertically")

    def clamp_scroll_offsets(self):
        """
        Ensure scroll offsets stay within valid bounds.
        """
        surface = self.renders[self.current_index]
        if surface:
            zoom = self.zoom_levels.get(self.current_index, 1.0)
            h = int(surface.get_height() * zoom)
            w = int(surface.get_width() * zoom)
            self.scroll_offset_y = max(0, min(self.scroll_offset_y, max(0, h - self.height)))
            self.scroll_offset_x = max(0, min(self.scroll_offset_x, max(0, w - self.width)))
        else:
            self.scroll_offset_y = 0
            self.scroll_offset_x = 0

    def update_bar_positions(self):
        """
        Update scroll bar positions based on scroll offsets.
        """
        surface = self.renders[self.current_index]
        if surface:
            zoom = self.zoom_levels.get(self.current_index, 1.0)
            h = int(surface.get_height() * zoom)
            w = int(surface.get_width() * zoom)
            if h > self.height:
                percent_y = self.scroll_offset_y / (h - self.height)
                self.bar_rect_y.y = percent_y * (self.height - self.bar_rect_y.height)
            else:
                self.bar_rect_y.y = 0
            if w > self.width:
                percent_x = self.scroll_offset_x / (w - self.width)
                self.bar_rect_x.x = percent_x * (self.width - self.bar_rect_x.width)
            else:
                self.bar_rect_x.x = 0

    def update(self):
        """
        Update the frame state, handling scroll bar dragging.
        """
        mx, my = pygame.mouse.get_pos()
        local_x = mx - self.x
        local_y = my - self.y
        if self.dragging_y:
            delta_y = local_y - self.last_mouse_y
            self.bar_rect_y.y += delta_y
            self.last_mouse_y = local_y
            self.clamp_bar_y()
            self.update_scroll_offset_y()
        if self.dragging_x:
            delta_x = local_x - self.last_mouse_x
            self.bar_rect_x.x += delta_x
            self.last_mouse_x = local_x
            self.clamp_bar_x()
            self.update_scroll_offset_x()

    def clamp_bar_y(self):
        """
        Keep the vertical scroll bar within its bounds.
        """
        self.bar_rect_y.y = max(0, min(self.bar_rect_y.y, self.height - self.bar_rect_y.height))

    def clamp_bar_x(self):
        """
        Keep the horizontal scroll bar within its bounds.
        """
        self.bar_rect_x.x = max(0, min(self.bar_rect_x.x, self.width - self.bar_rect_x.width))

    def update_scroll_offset_y(self):
        """
        Update vertical scroll offset based on scroll bar position.
        """
        surface = self.renders[self.current_index]
        zoom = self.zoom_levels.get(self.current_index, 1.0)
        if surface and surface.get_height() * zoom > self.height:
            percent = self.bar_rect_y.y / (self.height - self.bar_rect_y.height)
            self.scroll_offset_y = percent * (surface.get_height() * zoom - self.height)
        else:
            self.scroll_offset_y = 0

    def update_scroll_offset_x(self):
        """
        Update horizontal scroll offset based on scroll bar position.
        """
        surface = self.renders[self.current_index]
        zoom = self.zoom_levels.get(self.current_index, 1.0)
        if surface and surface.get_width() * zoom > self.width:
            percent = self.bar_rect_x.x / (self.width - self.bar_rect_x.width)
            self.scroll_offset_x = percent * (surface.get_width() * zoom - self.width)
        else:
            self.scroll_offset_x = 0

    def draw(self, target_surface:pygame.Surface):
        """
        Draw hermana frame onto the target surface.

        Args:
            target_surface (pygame.Surface): The surface to draw onto.
        """
        # Clear the surface
        self.surface.fill((0, 0, 0, 0))
        # Draw the background
        pygame.draw.rect(self.surface, self.bg_color, (0, 0, self.width, self.height), border_radius=8)
        surface = self.renders[self.current_index]
        if surface:
            # Apply zoom and draw the content
            zoom = self.zoom_levels.get(self.current_index, 1.0)
            scaled = pygame.transform.rotozoom(surface, 0, zoom)
            clip_rect = pygame.Rect(self.scroll_offset_x, self.scroll_offset_y, self.width, self.height)
            self.surface.blit(scaled, (0, 0), area=clip_rect)
        else:
            # Show placeholder if content isn't loaded
            self.surface.blit(self.placeholder, (0, 0))
        # Draw scroll bars
        pygame.draw.rect(self.surface, self.bar_color, self.bar_rect_y, border_radius=self.bar_width // 2)
        pygame.draw.rect(self.surface, self.bar_color, self.bar_rect_x, border_radius=self.bar_width // 2)
        # Blit the frame to the target surface
        target_surface.blit(self.surface, (self.x, self.y))
