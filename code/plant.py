import pygame
import globalvariables

from globalvariables import * # import global_plants_data
from settings import * # import constants

from plantshadow import PlantShadow

class Plant(pygame.sprite.Sprite):

    def __init__(self, name, group, shadow_group):
        super().__init__(group)
        global global_plants_data

        self.shadow_group = shadow_group

        self.name = name
        self.data = global_plants_data[name]
        self.health = self.data['health']
        self.width = PLANT_WIDTH
        self.height = PLANT_HEIGHT

        self.sprites = []
        self.current_sprite = 0
        self.image = pygame.image.load(f'../assets/wallnut/sus.png')

        self.shadow = None

    def kill(self):
        self.shadow.kill()
        super().kill()
        
    def setup_shadow(self):
        self.shadow = PlantShadow(self.name, self.shadow_group, self.rect.x, self.rect.y, self.width, self.height)

    def resize_rect(self, pos_x = 0, pos_y = 0):
        self.rect.topleft = [ pos_x, pos_y ]
        self.rect.width = self.width
        self.rect.height = self.height
        self.hitbox = self.rect


    def resize_all_sprites(self):
        for i, sprite in enumerate(self.sprites):
            self.sprites[i] = pygame.transform.scale(sprite, (self.width, self.height))

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect.width = self.width
        self.rect.height = self.height


    def damage(self, amount):
        if self.health - amount > 0:
            self.health -= amount
            return False
        else:
            return True

    def on_click(self, pos):
        pass

    def update(self, level):
        pass

    def draw_debug_boxes(self):
        pass