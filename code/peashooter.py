import pygame
import time
from random import uniform, randint

from globalvariables import *
from settings import *
from plant import Plant
from pea import Pea


class Peashooter(Plant):
    def __init__(self, collision_group, projectile_group, overlay_group, interact=True, pos_x = 0, pos_y = 0):
        super().__init__('Peashooter', collision_group)
        
        self.group = collision_group
        self.pea_group = projectile_group
        self.interact = interact

        self.start_time = time.time()
        self.update_time = 0.0
        self.shoot_interval = uniform(1.3, 1.5)

        self.frames_per_second = 2
        self.frame_start_time = time.time()
        self.frame_update_time = 0

        self.sprites = [
            # Plain
            pygame.image.load(f'../assets/Peashooter/1.png').convert_alpha(),
            pygame.image.load(f'../assets/Peashooter/2.png').convert_alpha(),
            pygame.image.load(f'../assets/Peashooter/3.png').convert_alpha(),
        ]
        self.sprites_orders = {
            "Plain":   [ 0, 1, 2, 1 ]
        }
        self.current_state = "Plain"
        self.sprites_order = self.sprites_orders[self.current_state]

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()

        self.view_box = None
        self.is_seeing_zombies = False

        self.resize_rect(pos_x, pos_y)
        self.resize_all_sprites()

        self.view_box = self.rect
        self.view_box = self.view_box.inflate(0, -50)
        self.view_box.width = BOARD_CELL_SIZE * 9


    def check_view(self, zombies):
        self.is_seeing_zombies = False
        
        for zombie in zombies:
            if self.view_box.colliderect(zombie.hitbox):
                self.is_seeing_zombies = True
                break


    def shoot(self):
        if self.interact:
            if self.is_seeing_zombies == True:
                pea = Pea(
                    self.pea_group, 
                    self.rect.x + self.width - PEA_CELL_RIGHT_OFFSET, 
                    self.rect.y + PEA_CELL_TOP_OFFSET + (3 * (self.current_sprite % 3))
                )


    def update(self, level):
        # Viewbox collision
        self.check_view(level.zombies)

        # Shoot and animation
        self.frame_update_time = time.time()
        self.update_time = time.time()

        frame_delta = self.frame_update_time - self.frame_start_time
        delta_time = self.update_time - self.start_time

        if self.current_sprite == 0 and delta_time >= 1.0:
            self.start_time = time.time()
            self.update_time = time.time()
            self.shoot()

        self.current_sprite = int(frame_delta * self.frames_per_second % len(self.sprites_order))
        if frame_delta >= len(self.sprites_order):
            self.frame_start_time = time.time()
            self.frame_update_time = time.time()

        self.image = self.sprites[self.sprites_order[self.current_sprite]]


    def draw_view_box(self):
        pygame.draw.rect(pygame.display.get_surface(), 'Black', self.view_box, 2)


    def draw_debug_boxes(self):
        self.draw_view_box()
