import pygame
import globalvariables
import time

class Sun(pygame.sprite.Sprite):
    def __init__(self, group, value, pos_x, pos_y):
        super().__init__(group)

        self.group = group

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.width = 45
        self.height = 45

        self.value = value

        self.image = pygame.image.load(f'../assets/sun.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.hitbox = self.rect
        self.rect.topleft = [ self.pos_x, self.pos_y ]   

        self.start_time = time.time()
        self.update_time = 0.0
        self.interval = 5.0
        self.stop_scaling = False

        self.multiplier = 0.001

    def size(self):
        pass
        # if self.stop_scaling != True:
        #     self.update_time = time.time()
        #     delta_time = self.update_time - self.start_time

        #     self.multiplier += 0.025

        #     if delta_time >= self.interval:
        #         self.stop_scaling = True
        #         self.multiplier = 1
        #         print("done")

        #     self.image = pygame.transform.scale(self.image, (self.width * self.multiplier , self.height * self.multiplier))
        #     self.rect = self.image.get_rect()
        #     self.hitbox = self.rect
        #     self.rect.topleft = [ self.pos_x, self.pos_y ]      


    def on_click(self, pos):
        if self.rect.collidepoint(pos):
            self.group.level.balance += self.value
            self.kill()            


    def update(self, level):
        self.size()

        # Self destruct if sunbloom get's eaten and doesnt handle remove
        self.update_time = time.time()
        if self.update_time - self.start_time >= 10.0:
            self.kill()

    def draw_debug_boxes(self):
        pygame.draw.rect(pygame.display.get_surface(), 'Black', self.hitbox, 2)


# def move(pos, speed, points):
#     direction = pygame.math.Vector2(points[0]) - pos
#     if direction.length() <= speed:
#         pos = points[0]
#         points.append(points[0])
#         points.pop(0)
#     else:
#         direction.scale_to_length(speed)
#         new_pos = pygame.math.Vector2(pos) + direction
#         pos = (new_pos.x, new_pos.y) 
#     return pos


