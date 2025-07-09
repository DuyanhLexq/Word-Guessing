import pygame
import re

class Label:
    def __init__(self, x: int, y: int, width: int, height: int,
                 bgColor=(255, 255, 255, 255), content="", font="arial", fontSize=24,
                 fontColor=(0, 0, 0), borderRadius=0, imagePath=None) -> None:
        """
        Tạo một Label với text nhiều màu.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.bgColor = bgColor
        self.content = content
        try:
            self.font = pygame.font.Font(font,fontSize)
        except:
            self.font = pygame.font.SysFont(font,fontSize)
        self.defaultFontColor = fontColor
        self.borderRadius = borderRadius
        self.imagePath = imagePath
        self.image = None
        self.visible = True  # trạng thái hiển thị

        # Nếu có ảnh thì load ảnh
        if self.imagePath:
            try:
                self.image = pygame.image.load(self.imagePath).convert_alpha()
                self.image = pygame.transform.scale(self.image, (width, height))
            except pygame.error as e:
                print(f"Không load được ảnh: {self.imagePath}. Lỗi: {e}")
                self.image = None

    def parse_text(self, text):
        """
        Parse text dạng <#hex>content</>
        Trả về list (content, color)
        """
        pattern = r"<#([0-9a-fA-F]{6})>(.*?)</>"
        matches = re.findall(pattern, text)
        result = []
        pos = 0
        for match in matches:
            color_hex, content = match
            color_rgb = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
            start = text.find(f"<#{color_hex}>{content}</>", pos)
            if start > pos:
                # text trước đoạn có tag
                plain_text = text[pos:start]
                result.append((plain_text, self.defaultFontColor))
            result.append((content, color_rgb))
            pos = start + len(f"<#{color_hex}>{content}</>")
        if pos < len(text):
            # text còn lại
            result.append((text[pos:], self.defaultFontColor))
        return result

    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return  # không vẽ nếu label bị ẩn

        if self.image:
            surface.blit(self.image, self.rect)
        else:
            # Tạo surface hỗ trợ alpha
            label_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            pygame.draw.rect(label_surface, self.bgColor, label_surface.get_rect(), border_radius=self.borderRadius)
            surface.blit(label_surface, self.rect.topleft)

            # Render từng đoạn text
            x_offset = self.rect.x + 5  # padding nhỏ bên trái
            y_center = self.rect.centery
            parts = self.parse_text(self.content)
            for part_text, part_color in parts:
                text_surface = self.font.render(part_text, True, part_color)
                text_rect = text_surface.get_rect(midleft=(x_offset, y_center))
                surface.blit(text_surface, text_rect)
                x_offset += text_surface.get_width()

    def updateText(self, new_text: str):
        """Cập nhật nội dung chữ"""
        self.content = new_text

    def hide(self):
        """Ẩn label"""
        self.visible = False

    def show(self):
        """Hiện lại label"""
        self.visible = True

    def delete(self):
        """Xóa label (giải phóng ảnh nếu có)"""
        if self.image:
            del self.image
        self.content = ""
        self.visible = False
