import pygame

from utils.jsondata import global_projectiles_data

class ProjectileShadow(pygame.sprite.Sprite):
    def __init__(self, name, group, pos_x=0, pos_y=0, width=100, height=100):
        super().__init__(group)
        self.group = group

        global global_projectiles_data

        self.data = global_projectiles_data[name]

        self.width = width + self.data['shadow']['width_extend']
        self.height = height + self.data['shadow']['height_extend']
        
        self.image = pygame.image.load(f'../assets/Shadow/{name}_shadow.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, ( self.width, self.height ))
        self.image.set_alpha(18)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x + self.data['shadow']['offset_x']
        self.rect.y = pos_y + self.data['shadow']['offset_y']

    