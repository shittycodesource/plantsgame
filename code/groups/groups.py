import pygame, math

from settings.const import DRAW_YSORT_GROUP_VIEWBOXES

class ShadowGroup(pygame.sprite.Group):
    def __init__(self, main):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.main = main

    def draw(self):
        for sprite in self.sprites():
            self.display_surface.blit(sprite.image, sprite.rect)


class YSortCameraGroup(pygame.sprite.Group): 
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        
    def draw(self):
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.hitbox.centery):
            self.display_surface.blit(sprite.image, sprite.rect)
            
            if (DRAW_YSORT_GROUP_VIEWBOXES):
                sprite.draw_view_box()
                sprite.draw_debug_boxes()


class SpriteInteractive(YSortCameraGroup):
    def __init__(self, level, main):
        super().__init__()

        self.level = level
        self.main = main

    def on_click(self, pos):
        for sprite in self.sprites():
            sprite.on_click(pos)

    def update(self, level):
        for sprite in self.sprites():
            sprite.update(self.level, self.main.dt)

    # def draw(self):
    #     for sprite in self.sprites():
    #         self.display_surface.blit(sprite.image, sprite.rect)



class ZombiesGroup(SpriteInteractive):
    def __init__(self, level, main):
        super().__init__(level, main)

    def update(self, pos, board, level):
        for sprite in self.sprites():
            if sprite.hitbox.x < -60:
                level.game_state_manager.set_state('lost')
            
            sprite.update(pos, board, self.main.dt)


    # def draw(self):
    #     for sprite in self.sprites():
    #         self.display_surface.blit(sprite.image, sprite.rect)
            # sprite.render_hitbox()