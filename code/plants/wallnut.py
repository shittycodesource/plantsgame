import pygame
import time

from utils.jsondata import *
from plants.plant import Plant

class Basenut(Plant):
    def __init__(self, name, collision_group, shadow_group, projectile_group, overlay_group, interact=True, defeat_callback=None, pos_x = 0, pos_y = 0):
        super().__init__(name, collision_group, shadow_group, interact, defeat_callback)

        self.shadow_group = shadow_group

        self.sprites = [
            pygame.image.load(f'../assets/Wallnut/1.png').convert_alpha(),
            pygame.image.load(f'../assets/Wallnut/5.png').convert_alpha(),

            pygame.image.load(f'../assets/Wallnut/2.png').convert_alpha(),
            pygame.image.load(f'../assets/Wallnut/6.png').convert_alpha(),
            
            pygame.image.load(f'../assets/Wallnut/3.png').convert_alpha(),
            
            pygame.image.load(f'../assets/Wallnut/4.png').convert_alpha(),
            pygame.image.load(f'../assets/Wallnut/7.png').convert_alpha(),
        ]
        self.sprites_orders = {
            "Plain":   [ 0, 0, 1, 0 ],
            "crack_1": [ 2, 2, 3, 2 ],
            "crack_2": [ 4, 4, 4, 4 ],
            "crack_3": [ 5, 5, 6, 5 ]
        }
        
        self.frames_per_second = 1

        self.setup(pos_x, pos_y)

    def update(self, level, dt):
        self.frame_handler(dt)
        self.damage_state_check()

    def damage_state_check(self):
        if self.health > 999:
            self.sprites_state = "Plain"
            return
        elif self.health > 600:
            self.sprites_state = "crack_1"
            return
        elif self.health > 400:
            self.sprites_state = "crack_2"
            return
        elif self.health > 200:
            self.sprites_state = "crack_3"

class Wallnut(Basenut):
    def __init__(self, collision_group, shadow_group, projectile_group, overlay_group, interact=True, defeat_callback=None, pos_x = 0, pos_y = 0):
        super().__init__('Wallnut', collision_group, shadow_group, projectile_group, overlay_group, interact, defeat_callback, pos_x = 0, pos_y = 0)
        self.setup(pos_x, pos_y)


class Susnut(Basenut):
    def __init__(self, collision_group, shadow_group, projectile_group, overlay_group, interact=True, defeat_callback=None, pos_x = 0, pos_y = 0):
        super().__init__('Susnut', collision_group, shadow_group, projectile_group, overlay_group, interact, defeat_callback, pos_x = 0, pos_y = 0)

        self.sprites = [ pygame.image.load(f'../assets/Susnut/Susnut.png').convert_alpha() ]
        self.setup(pos_x, pos_y)

    def update(self, level, dt):
        pass

class Sus(Basenut):
    def __init__(self, collision_group, shadow_group, projectile_group, overlay_group, interact=True, defeat_callback=None, pos_x = 0, pos_y = 0):
        super().__init__('Sus', collision_group, shadow_group, projectile_group, overlay_group, interact, defeat_callback, pos_x = 0, pos_y = 0)
        self.sprites = [ pygame.image.load(f'../assets/Sus/Sus.png').convert_alpha() ]
        self.setup(pos_x, pos_y)

    def update(self, level, dt):
        pass