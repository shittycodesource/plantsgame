import pygame
import time
from random import *

from utils.jsondata import *

from plants.plant import Plant
from plants.sun import Sun

class Sunbloom(Plant):
    def __init__(self, collision_group, shadow_group, projectile_group, overlay_group, interact=True, defeat_callback=None, pos_x=0, pos_y=0):
        super().__init__('Sunbloom', collision_group, shadow_group, interact, defeat_callback)

        self.group = collision_group
        self.shadow_group = shadow_group
        self.sun_group = overlay_group
        self.interact = interact

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

        self.frames_per_second = 3

        self.setup(pos_x, pos_y)
        
        self.spawned_sun = None

    def time_event(self):
        self.lighten()

    def lighten(self):
        if (self.interact):
            if self.sprites_state == "Plain":

                if self.spawned_sun != None: 
                    self.spawned_sun.kill()
                    self.sun_group.empty()
                
                self.time_interval_mark = 4.0
                self.sprites_state = "Lighten"

                self.spawned_sun = Sun(self.sun_group, 25, self.rect.x + randint(-10, 100), self.rect.y + (self.height // 2) + randint(-5, 5))
           
            else:
                self.time_interval_mark = uniform(15.0, 24.0)
                self.sprites_state = "Plain"

            self.sprites_current_order = self.sprites_orders[self.sprites_state]

    def on_click(self, pos):
        pass
