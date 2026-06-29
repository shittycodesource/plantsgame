import pygame, math

class ShadowGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        
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
            # sprite.draw_view_box()
            # sprite.draw_debug_boxes()

class SpriteInteractive(YSortCameraGroup):
    def __init__(self, level):
        super().__init__()
        self.level = level

    def on_click(self, pos):
        for sprite in self.sprites():
            sprite.on_click(pos)

    def update(self, level):
        for sprite in self.sprites():
            sprite.update(level)

    # def draw(self):
    #     for sprite in self.sprites():
    #         self.display_surface.blit(sprite.image, sprite.rect)


class ZombiesGroup(SpriteInteractive):
    def __init__(self, level):
        super().__init__(level)
        self.level = level
        # self.copy = self.sprites()

    def update(self, pos, board, level):
        # local = level.wave_health
        # progress = level.wave_damage_to_finish 

        for sprite in self.sprites():
            if sprite.hitbox.x < -60:
                level.game_state_manager.set_state('lost')
            
            sprite.update(pos, board)


    # def draw(self):
    #     for sprite in self.sprites():
    #         self.display_surface.blit(sprite.image, sprite.rect)
            # sprite.render_hitbox()