import pygame

from utils.jsondata import *
from settings.const import BOARD_CELL_SIZE, BOARD_OFFSET_LEFT, BOARD_OFFSET_TOP

from groups.groups import SpriteInteractive, ShadowGroup

from plants.sunbloom import Sunbloom
from plants.peashooter import Peashooter
from plants.wallnut import Wallnut, Susnut, Sus

class Board:
    def __init__(self, width: int, height: int, level=None, main=None, score=None):
        self.display_surface = pygame.display.get_surface()
        
        self.level = level
        self.main = main
        self.score = score

        self.width = width
        self.height = height

        self.board      = [ [0] * width for _ in range(height) ]
        self.rectangles = [ [0] * width for _ in range(height) ]

        self.shadow_group           = ShadowGroup(main)
        self.zombie_collision_group = SpriteInteractive(level, main)
        self.projectiles_group      = SpriteInteractive(level, main) 
        self.overlay_group          = SpriteInteractive(level, main)

        self.cell_size = BOARD_CELL_SIZE
        self.left = BOARD_OFFSET_LEFT
        self.top  = BOARD_OFFSET_TOP

        self.showcase_image = None
        self.showcase_image_rect = None


    def get_cell_indexes(self, pos):
        mouse_x, mouse_y = pos

        if (self.left <= mouse_x) and (self.top <= mouse_y):
            column = (mouse_x - self.left) // self.cell_size
            row = (mouse_y - self.top) // self.cell_size
            
            if (row < self.height) and (column < self.width):
                return column, row

        return None, None
    
    
    def get_plant_rect(self, row, column):
        return self.rectangles[row][column]

    
    def get_plant_cost(self, plant):
        global global_plants_data
        data = global_plants_data[plant]
        return data['cost']
    

    def handle_hover(self, pos, current_dragging):
        column, row = self.get_cell_indexes(pos)

        if (column != None) and (row != None) and (self.board[row][column] == 0):
            rect = self.rectangles[row][column]
            self.showcase_image = current_dragging[3].image.copy()
            self.showcase_image.set_alpha(128)
            self.showcase_image_rect = self.showcase_image.get_rect(center=rect.center)
        else:
            self.showcase_image = None
            self.showcase_image_rect = None


    def on_click(self, pos, current_dragging=None):
        self.zombie_collision_group.on_click(pos)
        self.overlay_group.on_click(pos)

        if current_dragging != None:
            mouse_x, mouse_y = pos

            if self.left < mouse_x < (self.left + (self.cell_size * self.width)) and self.top < mouse_y < self.top + (self.cell_size * self.height):
                column, row = self.get_cell_indexes(pos)

                if self.board[row][column] == 0:
                    self.place_plant(column, row, current_dragging)
                    return True
        return False


    # SPAWNING AND INITIALIZING NEW CLASSES HERE
    def place_plant(self, column, row, current_dragging):

        global global_plants_data

        rect = self.get_plant_rect(row, column)
        plant_name = current_dragging[1]

        defeat_callback = lambda ref: self.score.decrease( global_plants_data[plant_name]["score"]["defeat"] )

        cls = eval(plant_name)
        cls(
            self.zombie_collision_group, 
            self.shadow_group,
            self.projectiles_group, 
            self.overlay_group,
            True, # interact 
            defeat_callback=defeat_callback, # defeat callback
            pos_x=rect.x, pos_y=rect.y
        )

        self.board[row][column] = current_dragging[1] # set name of the plant
        self.showcase_image = None
        self.showcase_image_rect = None

        self.level.balance -= self.get_plant_cost(current_dragging[1])
        self.level.seeds_bank.start_cooldown(current_dragging[0], current_dragging[2], current_dragging[1])
        self.score.increase( global_plants_data[plant_name]["score"]["place"] )
        
        # sound = pygame.mixer.Sound("../assets/plant.mp3")
        # sound.set_volume(0.2)
        # sound.play() 

    def update(self, level):
        self.zombie_collision_group.update(level)
        self.projectiles_group.update(level)
        self.overlay_group.update(level)

        # print("board update, zombies len:", len(level.zombies))


    def render(self):
        for i in range(self.width):
            for j in range(self.height):

                posX = (i * self.cell_size) + self.left 
                posY = (j * self.cell_size) + self.top

                rect = pygame.Rect(posX, posY, self.cell_size, self.cell_size)
                self.rectangles[j][i] = rect

                # render cell border
                # pygame.draw.rect(self.display_surface, 'Black', rect, 2)

        if self.showcase_image != None and self.showcase_image_rect != None:
            self.display_surface.blit(self.showcase_image, self.showcase_image_rect)

        self.shadow_group.draw()
        self.zombie_collision_group.draw()


    def render_overlay(self):
        self.projectiles_group.draw()
        self.overlay_group.draw()