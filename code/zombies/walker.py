import pygame
import time

from utils.jsondata import global_zombie_data
from settings.const import ZOMBIE_WIDTH, ZOMBIE_HEIGHT, ZOMBIE_HITBOX_OFFSET, ZOMBIE_BOTTOM_OFFSET, ZOMBIE_TOP_OVERLAP

from random import uniform, randint

class Walker(pygame.sprite.Sprite):
    def __init__(self, zombie_type, lane, wave_id, group, pos_x = 0, pos_y = 0, level_ref = 0):
        super().__init__(group)
        self.display_surface = pygame.display.get_surface()

        global global_zombie_data

        self.level_ref = level_ref
        self.data = global_zombie_data[zombie_type]
        self.speed = self.data['speed']
        self.health = self.data['health']
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

        self.type = 'Zombie'
    

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


    def walk(self, dt):
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

        # Check board collisions
        board_collided_sprite = pygame.sprite.spritecollideany(dummy_sprite, board.zombie_collision_group)
        if board_collided_sprite:
            column, row = board.get_cell_indexes(board_collided_sprite.rect.topleft)
            if column != None and row != None:
                self.speed = 0
                self.attack(pos, board, column, row, board_collided_sprite)
            else:
                print("What the fuck?")
        else:
            if self.current_sprite != 3 and self.current_sprite != 7 and self.current_sprite != 0:
                self.speed = self.data['speed']

        # Check projectile collisions
        projectile_sprite = pygame.sprite.spritecollideany(dummy_sprite, board.projectiles_group)
        if (projectile_sprite):
            self.take_damage(projectile_sprite.damage)
            projectile_sprite.kill()
        
        dummy_sprite.kill()


    def take_damage(self, damage):
        print("Zombie damaged", damage)
        
        if self.health - damage > 0:
            self.health -= damage
            self.level_ref.add_damage(damage)
        else:
            print("Zombie defeated")
            # globalvariables.score += 450
            self.kill()
            self.level_ref.add_damage(self.health)


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


    def update(self, level, dt):
        self.walk(dt)
        self.animate()        


    def on_click(self, pos):
        pass

    def draw_debug_boxes(self):
        self.render_hitbox()