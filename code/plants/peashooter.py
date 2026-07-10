import pygame
import time
from random import uniform, randint

from utils.jsondata import *
from settings.const import BOARD_CELL_SIZE, PEA_CELL_RIGHT_OFFSET, PEA_CELL_TOP_OFFSET

from plants.plant import Plant
from projectiles.pea import Pea


class Peashooter(Plant):
    def __init__(self, collision_group, shadow_group, projectile_group, overlay_group, interact=True, defeat_callback=None, pos_x = 0, pos_y = 0):
        super().__init__('Peashooter', collision_group, shadow_group, interact, defeat_callback)
        
        self.group = collision_group
        self.shadow_group = shadow_group
        self.pea_group = projectile_group
        self.interact = interact

        self.time_interval_mark = uniform(1.3, 1.5)

        self.sprites = [
            # Plain
            pygame.image.load(f'../assets/Peashooter/1.png').convert_alpha(),
            pygame.image.load(f'../assets/Peashooter/2.png').convert_alpha(),
            pygame.image.load(f'../assets/Peashooter/3.png').convert_alpha(),
        ]

        self.sprites_orders = { "Plain":   [ 0, 1, 2, 1 ] }
        self.frames_per_second = 2

        self.setup(pos_x, pos_y)

        self.view_box = self.rect
        self.view_box = self.view_box.inflate(0, -50)
        self.view_box.width = BOARD_CELL_SIZE * 9
        self.is_seeing_zombies = False


    def check_view(self, zombies):
        self.is_seeing_zombies = False
        
        for zombie in zombies:
            if self.view_box.colliderect(zombie.hitbox):
                self.is_seeing_zombies = True
                break


    def shoot(self):
        if self.interact:
            if self.is_seeing_zombies == True:
                pos_x = self.rect.x + self.width - PEA_CELL_RIGHT_OFFSET
                pos_y = self.rect.y + PEA_CELL_TOP_OFFSET + (3 * (self.current_sprite % 3))
                
                pea = Pea(self.pea_group, self.shadow_group, pos_x, pos_y)

    def time_event(self):
        self.shoot()
        self.time_interval_mark = uniform(1.3, 1.5)


    def update(self, level, dt):
        self.check_view(level.zombies) # Viewbox collision
        self.time_handler(dt)
        self.frame_handler(dt)

 
    def draw_view_box(self):
        pygame.draw.rect(pygame.display.get_surface(), 'Black', self.view_box, 2)


    def draw_debug_boxes(self):
        self.draw_view_box()
