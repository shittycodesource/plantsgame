import pygame, json
from random import uniform, choices, randint
import time 

import numpy as np

from globalvariables import *
from settings import *
from board import Board
from seeds import SeedsBank
from debug import debug

from group import SpriteInteractive, ZombiesGroup

from sunbloom import Sunbloom
from peashooter import Peashooter

from zombie import Zombie

class Level:
    
    def __init__(self, level_number, main_ref):

        self.level_number = level_number
        self.main_ref = main_ref

        self.loaded = self.load_level_data(self.level_number)
        self.seeds = self.load_seeds(self.loaded)
        self.balance = self.loaded['start_sun']

        self.display_surface = pygame.display.get_surface()

        self.zombies = ZombiesGroup(self)
        self.visual_group = SpriteInteractive(self) # some interactive sprites in background


        self.board = Board(8, 5, self)
        self.seeds_bank = SeedsBank(self)

        self.background = pygame.image.load('../assets/lawn.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (1440, 720))
        self.background_rect = self.background.get_rect()

        self.zombie_wave  = [ ]
        self.zombies_current_wave = 0
        self.max_zombie_waves = self.loaded['wave_count']

        self.wave_health = 0
        self.wave_took_damage = 0

        self.wave_start_time = time.time()
        self.wave_update_time = 0.0
        self.wave_timer = 0.0 # delta time
        self.first_level_offset = 5.0
        self.wave_cooldown = uniform(25.0 + self.first_level_offset, 35.0 + self.first_level_offset)
        
        self.lanes_weights = [ 1,1,1,1,1 ]
        self.lanes_weights_inverse = [ 1,1,1,1,1 ]

        self.prepare_waves_data()
        self.update_wave_timer()


    def load_level_data(self, level_number):

        with open(f'../json/level_{level_number}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data


    def load_seeds(self, loaded):
        if loaded['custom_select_plants'] == False:
            return loaded['available_plants']
        else:
            # Make custom selection
            return [ "Sunbloom", "Peashooter", "Wallnut" ]


    def prepare_waves_data(self):
        global global_zombie_data

        for zombie in self.loaded['waves'][self.zombies_current_wave]['zombies']:
            self.wave_health += global_zombie_data[zombie]['health']
            weight = global_zombie_data[zombie]['weight']

            lane = self.find_optimal_lane(weight)
            self.lanes_weights[lane - 1] += weight

            zombie_x, zombie_y = self.get_zombie_lane_coordinate(lane)
            Zombie('Basic', lane, self.zombies_current_wave, self.zombies, 900 + randint(-150, 150), zombie_y) 


    def update_wave_timer(self):
        self.wave_update_time = time.time()
        
        self.wave_timer = self.wave_update_time - self.wave_start_time

        if self.wave_timer >= self.wave_cooldown:
            self.wave_start_time = time.time()
            self.wave_timer = 0
            print("Spawn next wave")


    def find_optimal_lane(self, weight):
        lanes = [ 1, 2, 3, 4, 5 ]
        
        inverse_weights_alt = (np.max(self.lanes_weights) + np.min(self.lanes_weights)) - self.lanes_weights # alternative
        self.lanes_weights_inverse = inverse_weights_alt

        result = choices(lanes, weights=self.lanes_weights_inverse , k=1)
        # lane = (result[0] + int(uniform(0, 100.0))) 
        lane = result[0] 

        print("Optimal lane: ", result[0])
        # print("Optimal lane + random: ", lane)
        return lane


    def get_zombie_lane_coordinate(self, lane):
        return ( screen_width, BOARD_OFFSET_TOP + (BOARD_CELL_SIZE * (lane - 1)) - ZOMBIE_TOP_OVERLAP)


    def spawn_zombies(self):
        pass
        # for wave in self.zombie_waves[self.zombies_current_wave]['zombies']:
        #     zombie_x, zombie_y = self.get_zombie_lane_coordinate(randint(1, 5))
        #     self.zombie = Zombie('Basic', 1, self.zombies, zombie_x, zombie_y)    



    def on_mouse_move(self, pos):
        if self.seeds_bank.current_dragging != None:
            self.board.handle_hover(pos, self.seeds_bank.current_dragging)
        self.seeds_bank.on_mouse_move(pos)


    def on_click(self, pos):
        self.seeds_bank.on_click(pos)
        response = self.board.on_click(pos, self.seeds_bank.current_dragging)
        
        if response: self.seeds_bank.stop_dragging()
        



    def update(self, pos):
        self.visual_group.update()
        
        self.board.update()
        self.zombies.update(pos, self.board)
        
        self.seeds_bank.update()

        self.update_wave_timer()


    def render(self):
        self.display_surface.blit(self.background, self.background_rect)
        
        self.board.render()
        self.zombies.draw()

        self.board.render_overlay()

        self.visual_group.draw()
        
        self.seeds_bank.render()

        debug(f'Level Data: ')
        if (SHOW_LEVEL_LOAD_DATA):  
            for i, item in enumerate(self.loaded):
                if item == 'available_plants':
                    debug(f'{item} (seeds): {self.seeds}', 50 + i * 30)
                elif item == 'start_sun':
                    debug(f'{item}: {self.loaded[item]}', 50 + i * 30)                
                    debug(f'sun: {self.balance}', 50 + len(self.loaded) * 30)
                else:
                    debug(f'{item}: {self.loaded[item]}', 50 + i * 30)
        if (SHOW_ZOMBIE_DATA):
                debug(f'waves: {self.loaded['waves']}', 50 + 30)
                debug(f'wave health: {self.wave_health}', 50 + 60)
                debug(f'wave timer: {self.wave_timer}', 50 + 90)
                debug(f'wave cooldown: {self.wave_cooldown}', 50 + 120)
                debug(f'lanes_weights : {self.lanes_weights}', 50 + 150)
                debug(f'lanes_weights_inverse : {self.lanes_weights_inverse}', 50 + 180)
