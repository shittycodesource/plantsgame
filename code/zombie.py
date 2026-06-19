import pygame
import time
from random import uniform, randint
import globalvariables
from settings import *

class Walker(pygame.sprite.Sprite):
    def __init__(self, zombie_type, lane, wave_id, group, pos_x = 0, pos_y = 0):
        super().__init__(group)
        self.display_surface = pygame.display.get_surface()

        self.data = globalvariables.global_zombie_data[zombie_type]
        self.speed = self.data['speed']
        self.wave_id = wave_id

        self.width = ZOMBIE_WIDTH
        self.height = ZOMBIE_HEIGHT

        self.frames_per_second = 2 + uniform(0, 0.8)
        self.frame_start_time = time.time()
        self.frame_update_time = 0
        self.frame_delta = 0

        self.sprites = [ pygame.image.load(f'../assets/Zombie/1.png').convert_alpha() ]
        self.sprites_orders = { "Plain": [ 0 ] }
        self.current_state = "Plain"
        self.sprites_order = self.sprites_orders[self.current_state]

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.hitbox = None

        self.float_pos_x = pos_x
        self.float_pos_y = pos_y

        self.started_attacking = False
        self.start_time = time.time()
        self.update_time = 0.0
        self.attack_interval = uniform(1.0, 2.0)
    

    def setup_hitbox(self):
        self.hitbox = self.rect.copy()
        self.hitbox.height = self.rect.height - (ZOMBIE_BOTTOM_OFFSET + ZOMBIE_TOP_OVERLAP)
        self.hitbox.y += ZOMBIE_TOP_OVERLAP
        self.hitbox_offset = ZOMBIE_HITBOX_OFFSET
        self.hitbox = self.hitbox.inflate(self.hitbox_offset * -2, 0)


    def resize_rect(self, pos_x = 0, pos_y = 0):
        self.rect.topleft = [ pos_x, pos_y ]
        self.rect.width = self.width
        self.rect.height = self.height


    def resize_all_sprites(self):
        for i, sprite in enumerate(self.sprites):
            self.sprites[i] = pygame.transform.scale(sprite, (self.width, self.height))

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]


    def walk(self):
        dt = globalvariables.dt        
        self.float_pos_x -= (self.speed * dt)

        self.rect.x = int(self.float_pos_x)
        self.hitbox.x = int(self.float_pos_x) + self.hitbox_offset


    def animate(self):
        self.frame_update_time = time.time()
        self.frame_delta = self.frame_update_time - self.frame_start_time

        self.current_sprite = int(self.frame_delta * self.frames_per_second % len(self.sprites_order))

        if self.current_sprite == 3 or self.current_sprite == 7 or self.current_sprite == 0:
            self.speed = 0.0

        if self.frame_delta >= len(self.sprites_order):
            self.frame_start_time = time.time()
            self.frame_update_time = time.time()
            self.frame_delta = 0.0

        self.image = self.sprites[self.sprites_order[self.current_sprite]]


    def check_collision(self, pos, board):
        dummy_sprite = pygame.sprite.Sprite()
        dummy_sprite.rect = self.hitbox

        collided_sprite = pygame.sprite.spritecollideany(dummy_sprite, board.plants)
        if collided_sprite:
            self.speed = 0
            # print(f'collided: {collided_sprite.rect.y} {collided_sprite.rect.height} {int(self.hitbox.y)}')
            column, row = board.get_cell_indexes(collided_sprite.rect.topleft)
            if column != None and row != None:
                self.attack(pos, board, column, row, collided_sprite)
            else:
                print("WHAT THE FUCk????") # this should not happen at all
                # if it happened it is certified what the fuck moment
        else:
            if self.current_sprite != 3 and self.current_sprite != 7 and self.current_sprite != 0:
                self.speed = self.data['speed']

        dummy_sprite.kill()


    def take_damage(self, damage):
        pass


    def attack(self, pos, board, column, row, collided_sprite):
        if self.started_attacking == False:
            self.started_attacking = True
            self.start_time = time.time()

        self.update_time = time.time()
        delta_time = self.update_time - self.start_time

        if delta_time >= self.attack_interval:
            self.start_time = time.time()
            self.update_time = time.time()
            damage = randint(10, 20)
            is_defeated = collided_sprite.damage(damage)

            print('ZOMBIE ATTACK: ', damage)

            if is_defeated:
                self.started_attacking = False
                board.board[row][column] = 0
                board.rectangles[row][column] = 0
                collided_sprite.kill()


    def render_hitbox(self):
        pygame.draw.rect(self.display_surface, 'Black', self.hitbox, 2)


    def update(self):
        self.walk()
        self.animate()        


    def on_click(self, pos):
        pass


class Zombie(Walker):
    def __init__(self, zombie_type, lane, wave_id, group, pos_x = 0, pos_y = 0):
        super().__init__('Basic', lane, wave_id, group, pos_x, pos_y)

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


    def update(self, pos, board):
        self.walk()
        self.animate()
        self.check_collision(pos, board)