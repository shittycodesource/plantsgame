import pygame
from globalvariables import *
from plant import Plant
import time

class Peashooter(Plant):
    def __init__(self, collidable_group, not_collidable_group, interact=True, pos_x = 0, pos_y = 0):
        super().__init__('Peashooter', collidable_group)
        
        self.group = collidable_group
        self.pea_group = not_collidable_group
        self.interact = interact

        self.frames_per_second = 3
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

        self.resize_rect(pos_x, pos_y)
        self.resize_all_sprites()

    def update(self):
        self.frame_update_time = time.time()
        frame_delta = self.frame_update_time - self.frame_start_time

        self.current_sprite = int(frame_delta * self.frames_per_second % len(self.sprites_order))
        if frame_delta >= len(self.sprites_order):
            self.frame_start_time = time.time()
            self.frame_update_time = time.time()

        self.image = self.sprites[self.sprites_order[self.current_sprite]]
