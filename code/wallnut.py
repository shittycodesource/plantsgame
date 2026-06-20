import pygame
from globalvariables import *
from plant import Plant
import time

class Wallnut(Plant):
    def __init__(self, collision_group, shadow_group, projectile_group, overlay_group, interact=True, pos_x = 0, pos_y = 0):
        super().__init__('Wallnut', collision_group, shadow_group)

        self.shadow_group = shadow_group

        self.frames_per_second = 1
        self.frame_start_time = time.time()
        self.frame_update_time = 0

        self.sprites = [
            pygame.image.load(f'../assets/Wallnut/1.png').convert_alpha(),
            pygame.image.load(f'../assets/Wallnut/5.png').convert_alpha(),
        ]
        self.sprites_orders = {
            "Plain":   [ 0, 0, 1, 0 ]
        }
        self.current_state = "Plain"
        self.sprites_order = self.sprites_orders[self.current_state]

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.hitbox = self.rect

        self.resize_rect(pos_x, pos_y)
        self.resize_all_sprites()
        self.setup_shadow()

    def update(self, level):
        self.frame_update_time = time.time()
        frame_delta = self.frame_update_time - self.frame_start_time

        self.current_sprite = int(frame_delta * self.frames_per_second % len(self.sprites_order))
        if frame_delta >= len(self.sprites_order):
            self.frame_start_time = time.time()
            self.frame_update_time = time.time()

        self.image = self.sprites[self.sprites_order[self.current_sprite]]
