import pygame
from settings.const import SCREEN_WIDTH, SCREEN_HEIGHT 

class WaveBar:

    def __init__(self, screen, level_ref):
        self.level = level_ref
        self.display_surface = screen

        self.width = 200
        self.height = 20
        self.padding = 20
        self.bg_color = (40, 40, 40)
        self.bar_color = (0, 255, 0)
        self.border_color = (100, 100, 100)
        self.border_width = 2
        self.progress = 0

        self.wave_damage_to_finish = 0
        self.wave_damage_taken = 0
        
        self.font = pygame.font.Font('../assets/Tiny5.ttf', 24)

    def update(self, progress):
        self.progress = progress
        # self.wave_damage_to_finish = wave_damage_to_finish
        # self.wave_damage_taken = wave_damage_taken

        # if (self.wave_damage_taken):
        #     self.progress = min(100, (self.wave_damage_taken / self.wave_damage_to_finish) * 100)
        #     print(self.progress, '%')


    def render(self):
        x = SCREEN_WIDTH - self.width - self.padding
        y = SCREEN_HEIGHT - self.height - self.padding
        
        bar_rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(self.display_surface, self.bg_color, bar_rect)
        
        fill_width = (self.progress / 100) * self.width
        
        fill_x = x + self.width - fill_width
        fill_rect = pygame.Rect(fill_x, y, fill_width, self.height)
        pygame.draw.rect(self.display_surface, self.bar_color, fill_rect)
        
        pygame.draw.rect(self.display_surface, self.border_color, bar_rect, self.border_width)
        
        if self.font:
            text = self.font.render(f"{int(self.progress)}%", True, (255, 255, 255))
            text_rect = text.get_rect(center=(x + self.width // 2, y + self.height // 2))
            self.display_surface.blit(text, text_rect)