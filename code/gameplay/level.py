import pygame, json
from random import uniform, choices, randint
import time 

import numpy as np

from settings.const import SCREEN_WIDTH, BOARD_OFFSET_TOP, BOARD_CELL_SIZE, ZOMBIE_TOP_OVERLAP, SHOW_LEVEL_LOAD_DATA, SHOW_ZOMBIE_DATA
from settings.paths import read_txt, write_txt

from gameplay.board import Board
from gameplay.seeds import SeedsBank
from gameplay.wavebar import WaveBar

from groups.groups import SpriteInteractive, ZombiesGroup

from zombies.zombie import Zombie

from utils.jsondata import global_zombie_data
from utils.debug import debug

class Level:
    
    def __init__(self, screen, game_state_manager, score, level_number, main_ref):
        self.display_surface = screen
        self.level_number = level_number

        self.main_ref = main_ref
        self.game_state_manager = game_state_manager
        self.score = score

    def setup(self, number):
        self.level_number = number
        self.loaded = self.load_level_data(self.level_number)
        self.seeds = self.load_seeds(self.loaded)
        self.balance = self.loaded['start_sun']

        self.zombies = ZombiesGroup(self, self.main_ref)
        self.visual_group = SpriteInteractive(self, self.main_ref)

        self.board = Board(9, 5, self, self.main_ref, self.score)
        self.seeds_bank = SeedsBank(self)
        self.wavebar = WaveBar(self.display_surface, self)

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
        self.wave_cooldown = uniform(5.0 + self.first_level_offset, 7.0 + self.first_level_offset)
        
        self.wave_damage_taken = 0
        self.wave_damage_to_finish = 0
        
        self.lanes_weights = [ 1,1,1,1,1 ]
        self.lanes_weights_inverse = [ 1,1,1,1,1 ]

        self.zombies_took_damage = 0
        self.waves_done = False

        self.prepare_waves_data()
        self.update_wave_timer()
        self.calculate_waves_health()

    def reset(self, number):
        self.setup(number)

    def load_level_data(self, level_number):
        with open(f'../json/level_{level_number}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data


    def load_seeds(self, loaded):
        if loaded['custom_select_plants'] == False:
            return loaded['available_plants']
        else:
            # Make custom selection
            # return [ "Sunbloom", "Peashooter", "Wallnut", "Susnut", "Sus" ]
            return [ "Sunbloom", "Peashooter", "Wallnut" ]


    def calculate_waves_health(self):
        global global_zombie_data

        for i in range(self.max_zombie_waves):
            for zombie in self.loaded['waves'][i]['zombies']:
                self.wave_damage_to_finish += global_zombie_data[zombie]['health']


    def add_damage(self, damage):
        self.zombies_took_damage += damage
        self.local_damage += damage


    def prepare_waves_data(self):
        global global_zombie_data

        if self.waves_done != True:
            self.wave_health = 0
            self.local_damage = 0
            for zombie in self.loaded['waves'][self.zombies_current_wave]['zombies']:
                self.wave_health += global_zombie_data[zombie]['health']
                weight = global_zombie_data[zombie]['weight']

                lane = self.find_optimal_lane(weight)
                self.lanes_weights[lane - 1] += weight

                zombie_x, zombie_y = self.get_zombie_lane_coordinate(lane)
                Zombie('Basic', lane, self.zombies_current_wave, self.zombies, SCREEN_WIDTH + randint(20, 150), zombie_y, self) 


    def update_wave_timer(self):
        if self.waves_done != True:
            if (self.wave_health / 2 <= self.local_damage):
                self.wave_update_time = time.time()
                
                self.wave_timer = self.wave_update_time - self.wave_start_time

                if self.wave_timer >= self.wave_cooldown:
                    self.wave_start_time = time.time()
                    self.wave_timer = 0

                    if self.zombies_current_wave + 1 != self.max_zombie_waves:
                        self.zombies_current_wave = self.zombies_current_wave + 1
                        self.prepare_waves_data()
                    else:
                        self.waves_done = True


    def find_optimal_lane(self, weight):
        lanes = [ 1, 2, 3, 4, 5 ]
        
        inverse_weights_alt = (np.max(self.lanes_weights) + np.min(self.lanes_weights)) - self.lanes_weights # alternative
        self.lanes_weights_inverse = inverse_weights_alt

        result = choices(lanes, weights=self.lanes_weights_inverse , k=1)
        lane = result[0] 
        return lane


    def get_zombie_lane_coordinate(self, lane):
        return ( SCREEN_WIDTH, BOARD_OFFSET_TOP + (BOARD_CELL_SIZE * (lane - 1)) - ZOMBIE_TOP_OVERLAP)



    def on_mouse_move(self, pos):
        if self.seeds_bank.current_dragging != None:
            self.board.handle_hover(pos, self.seeds_bank.current_dragging)
        self.seeds_bank.on_mouse_move(pos)


    def on_click(self, pos):
        self.seeds_bank.on_click(pos)
        response = self.board.on_click(pos, self.seeds_bank.current_dragging)
        
        if response: self.seeds_bank.stop_dragging()
        


    def update(self, pos):
        # self.visual_group.update()
        if (self.main_ref.is_paused == False):
            self.board.update(self)
            
            self.zombies.update(pos, self.board, self)
            
            self.seeds_bank.update()

            self.update_wave_timer()

            self.wavebar.update(self.zombies_took_damage / self.wave_damage_to_finish * 100)

            # FInishing level
            if ((self.zombies_took_damage / self.wave_damage_to_finish * 100) == 100):
                self.game_state_manager.set_state('won')


    def render(self):
        self.display_surface.blit(self.background, self.background_rect)
        
        self.board.render()
        
        self.zombies.draw()

        self.board.render_overlay()

        # self.visual_group.draw()
        
        self.seeds_bank.render()

        self.wavebar.render()

        debug(f'Level Data: ')
        debug(f'Score: {self.score.get_score()}', 30)



        
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
            debug(f'wave_damage_to_finish: {self.wave_damage_to_finish}', 50 + 30)
            # debug(f'waves: {self.loaded['waves']}', 50 + 30)
            # debug(f'wave health: {self.wave_health}', 50 + 60)
            # debug(f'wave timer: {self.wave_timer}', 50 + 90)
            # debug(f'wave cooldown: {self.wave_cooldown}', 50 + 120)
            # debug(f'lanes_weights : {self.lanes_weights}', 50 + 150)
            # debug(f'lanes_weights_inverse : {self.lanes_weights_inverse}', 50 + 180)


    def handle_click_events(self, event):
        if event.button == 1:
            self.on_click(event.pos)
        
        if event.button == 3:
            if self.seeds_bank.current_dragging:
                self.seeds_bank.stop_dragging()
                self.board.showcase_image = None
                self.board.showcase_image_rect = None

    def handle_keydown_events(self, event):
        if event.key == pygame.K_ESCAPE:
            if self.seeds_bank.current_dragging:
                self.seeds_bank.stop_dragging()
                self.board.showcase_image = None
                self.board.showcase_image_rect = None

    def run(self):
        self.update(pygame.mouse.get_pos())
        self.render()
        self.on_mouse_move(pygame.mouse.get_pos())