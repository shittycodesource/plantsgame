import pygame

from settings.const import PLANT_WIDTH, PLANT_HEIGHT
from plants.shadow import PlantShadow

from utils.jsondata import global_plants_data

class Plant(pygame.sprite.Sprite):

    def __init__(self, name, group, shadow_group, interact=True, defeat_callback=None):
        super().__init__(group)

        global global_plants_data

        self.shadow_group = shadow_group
        self.shadow = None

        self.name = name
        self.data = global_plants_data[name]
        self.health = self.data['health']
        self.width = PLANT_WIDTH
        self.height = PLANT_HEIGHT


        self.sprites = [ pygame.image.load(f'../assets/default.png').convert_alpha() ]
        self.current_sprite = 0
        self.sprites_state = "Plain"
        self.sprites_orders = { "Plain":  [ 0 ] }
        self.sprites_current_order = self.sprites_orders[self.sprites_state]

        self.image = self.sprites[self.current_sprite]

        # Time events
        self.time_accumulator = 0.0
        self.time_interval_mark = 5.0

        # Handle frame changes
        self.frames_per_second = 15
        self.frame_duration = 1.0 / self.frames_per_second
        self.frame_accumulator = 0.0

        self.defeat_callback = defeat_callback

    def setup(self, pos_x, pos_y):
        self.sprites_current_order = self.sprites_orders[self.sprites_state]
        
        self.setup_image_and_rect()
        self.resize_rect(pos_x, pos_y)
        self.resize_all_sprites()
        self.setup_shadow()

    def setup_image_and_rect(self):
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()

    def kill(self):
        self.shadow.kill()
        super().kill()
        

    def defeat(self):
        if self.defeat_callback != None:
            self.defeat_callback(self)
            print(self.name, "caused callback")
        
        self.kill()


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


    def update(self, level, dt):
        self.time_handler(dt)
        self.frame_handler(dt)


    def draw_debug_boxes(self):
        pass


    def time_handler(self, dt):
        self.time_accumulator += dt

        if self.time_accumulator >= self.time_interval_mark:
            self.time_event()
            self.time_accumulator -= self.time_interval_mark


    def time_event(self):
        pass


    def frame_handler(self, dt):
        self.frame_accumulator += dt

        sprite = int(self.frame_accumulator * self.frames_per_second % len(self.sprites_current_order))
        if self.current_sprite != sprite:
            self.current_sprite = sprite
    
            self.sprites_current_order = self.sprites_orders[self.sprites_state]
    
            self.image = self.sprites[self.sprites_current_order[self.current_sprite]]
        
            # Reset accumulator
            if self.frame_accumulator >= len(self.sprites_current_order):
                self.frame_accumulator -= len(self.sprites_current_order)