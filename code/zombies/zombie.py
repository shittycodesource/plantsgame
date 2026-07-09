import pygame
from zombies.walker import Walker

class Zombie(Walker):
    def __init__(self, zombie_type, lane, wave_id, group, pos_x = 0, pos_y = 0, level_ref = 0):
        super().__init__('Basic', lane, wave_id, group, pos_x, pos_y, level_ref)

        self.sprites = [
            pygame.image.load(f'../assets/Zombie/1.png').convert_alpha(),
            pygame.image.load(f'../assets/Zombie/2.png').convert_alpha(),
            pygame.image.load(f'../assets/Zombie/3.png').convert_alpha(),
            pygame.image.load(f'../assets/Zombie/4.png').convert_alpha(),
            pygame.image.load(f'../assets/Zombie/5.png').convert_alpha(),
            pygame.image.load(f'../assets/Zombie/6.png').convert_alpha(),
            pygame.image.load(f'../assets/Zombie/7.png').convert_alpha(),
            pygame.image.load(f'../assets/Zombie/8.png').convert_alpha()
        ]

        self.sprites_orders = {
            "Plain":   [ 0, 1, 2, 3, 4, 5, 6, 7 ]
        }

        self.current_state = "Plain"
        self.sprites_order = self.sprites_orders[self.current_state]
        self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.hitbox = None

        self.resize_rect(pos_x, pos_y)
        self.resize_all_sprites()
        self.setup_hitbox()


    def update(self, pos, board, dt):
        self.walk(dt)
        self.animate()
        self.check_collision(pos, board)