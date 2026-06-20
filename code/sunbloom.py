import pygame
import time
from random import *

from globalvariables import *

from plant import Plant
from sun import *

class Sunbloom(Plant):
    def __init__(self, collidable_group, not_colliadble_group, interact=True, pos_x=0, pos_y=0):
        super().__init__('Sunbloom', collidable_group)

        self.group = collidable_group
        self.sun_group = not_colliadble_group
        self.interact = interact

        self.start_time = time.time()
        self.update_time = 0.0
        # self.reset_interval = uniform(15.0, 24.0)
        self.reset_interval = 3.0

        self.frames_per_second = 3
        self.frame_start_time = time.time()
        self.frame_update_time = 0

        self.sprites = [
            # Plain
            pygame.image.load(f'../assets/Sunbloom/1.png').convert_alpha(),
            pygame.image.load(f'../assets/Sunbloom/2.png').convert_alpha(),
            pygame.image.load(f'../assets/Sunbloom/3.png').convert_alpha(),

            # Lighter
            pygame.image.load(f'../assets/Sunbloom/4.png').convert_alpha(),
            pygame.image.load(f'../assets/Sunbloom/5.png').convert_alpha(),
            pygame.image.load(f'../assets/Sunbloom/6.png').convert_alpha(),
        ]
        self.sprites_orders = {
            "Plain":   [ 0, 1, 0, 2 ],
            "Lighten": [ 3, 4, 3, 5 ]
        }
        self.current_state = "Plain"
        self.sprites_order = self.sprites_orders[self.current_state]

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()

        self.resize_rect(pos_x, pos_y)
        self.resize_all_sprites()
        
        self.spawned_sun = None


    def lighten(self):
        if (self.interact):
            if self.current_state == "Plain":
                if self.spawned_sun != None: 
                    self.spawned_sun.kill()
                    self.sun_group.empty()
                
                self.current_state = "Lighten"
                self.reset_interval = 1
                self.spawned_sun = Sun(self.sun_group, 25, self.rect.x + randint(-10, 100), self.rect.y + (self.height // 2) + randint(-5, 5))
            else:
                self.reset_interval = uniform(15.0, 24.0)
                self.current_state = "Plain"

            self.sprites_order = self.sprites_orders[self.current_state]


    def on_click(self, pos):
        pass

    def update(self):
        self.frame_update_time = time.time()
        self.update_time = time.time()

        frame_delta = self.frame_update_time - self.frame_start_time
        delta_time = self.update_time - self.start_time

        # Change state timer
        if delta_time >= self.reset_interval:
            self.start_time = time.time()
            self.lighten()

        # Sprite Animation
        self.current_sprite = int(frame_delta * self.frames_per_second % len(self.sprites_order))
        if frame_delta >= len(self.sprites_order):
            self.frame_start_time = time.time()
            self.frame_update_time = time.time()

        self.image = self.sprites[self.sprites_order[self.current_sprite]]
