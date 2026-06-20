import pygame
import globalvariables

class Projectile(pygame.sprite.Sprite):

    def __init__(self, name, group, pos_x = 0, pos_y = 0):
        super().__init__(group)

        self.group = group
        self.data = globalvariables.global_projectiles_data[name]

        self.width = self.data['width']
        self.height = self.data['height']

        self.sprites = [ pygame.image.load(f'../assets/{path}').convert_alpha() for path in (self.data['images']) ] 
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()

        self.hitbox = self.rect
        self.hitbox_offset = 0

        self.float_pos_x = pos_x
        self.float_pos_y = pos_y

        self.speed = self.data['speed']
        self.damage = self.data['damage']

        self.type = 'Projectile'

        self.resize_all_sprites()


    def resize_all_sprites(self):
        for i, sprite in enumerate(self.sprites):
            self.sprites[i] = pygame.transform.scale(sprite, (self.width, self.height))

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect.width = self.width
        self.rect.height = self.height


    def move(self):
        dt = globalvariables.dt        
        self.float_pos_x += (self.speed * dt)

        self.rect.x   = int(self.float_pos_x)
        self.hitbox.x = int(self.float_pos_x) + self.hitbox_offset
        self.rect.y   = int(self.float_pos_y)

    def on_click(self, pos):
        pass


    def update(self, level):
        self.move()

    def draw_debug_boxes(self):
        pygame.draw.rect(pygame.display.get_surface(), 'Black', self.hitbox, 2)


class Pea(Projectile):
    def __init__(self, group, pos_x, pos_y):
        super().__init__("Pea", group, pos_x, pos_y)
        self.group = group