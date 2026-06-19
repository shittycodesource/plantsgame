import pygame

class YSortCameraGroup(pygame.sprite.Group): 
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        
    def draw(self):
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.hitbox.centery):
            self.display_surface.blit(sprite.image, sprite.rect)

class SpriteInteractive(YSortCameraGroup):
    def __init__(self, level):
        super().__init__()
        self.level = level

    def on_click(self, pos):
        for sprite in self.sprites():
            sprite.on_click(pos)

    def update(self):
        for sprite in self.sprites():
            sprite.update()

    # def draw(self):
    #     for sprite in self.sprites():
    #         self.display_surface.blit(sprite.image, sprite.rect)


class ZombiesGroup(SpriteInteractive):
    def __init__(self, level):
        super().__init__(level)

    def update(self, pos, board):
        for sprite in self.sprites():
            sprite.update(pos, board)

    # def draw(self):
    #     for sprite in self.sprites():
    #         self.display_surface.blit(sprite.image, sprite.rect)
            # sprite.render_hitbox()