import pygame, json, time

from settings.const import SCREEN_WIDTH, SCREEN_HEIGHT, SHOW_DEBUG, SHOW_FPS
from settings.paths import read_txt, LEVEL_PATH

from managers.gamestatemanager import GameStateManager
from managers.score import Score

from screens.start import Start
from screens.won import Won
from screens.lost import Lost
from screens.pause import Pause

from gameplay.level import Level
from utils.debug import *

class Game:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_caption("Plants N Zombies 16x")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(60) / 1000

        # Score
        self.score = Score()    
        
        # Game States
        self.game_state_manager = GameStateManager('start')

        self.start = Start(self.screen, self.game_state_manager, self.score)        
        self.level = Level(self.screen, self.game_state_manager, self.score, 1, self)
        self.lost  = Lost(self.screen, self.game_state_manager, self.score)
        self.won   = Won(self.screen, self.game_state_manager, self.score)

        self.states = { 'start': self.start, 'level': self.level, 'lost': self.lost, 'won': self.won }
        self.current_state = self.game_state_manager.get_state()
        self.level_initialized = False

        # Puase
        self.paused = Pause(self.screen, self.game_state_manager, self)
        self.is_paused = False
        self.pause_dt = 0


    def update_dt(self):
        if self.is_paused == False:
            self.dt = (self.clock.tick(60) / 1000)
            self.pause_dt = 0
        else:
            self.pause_dt += self.clock.tick(60) / 1000
            self.dt = 0


    def run(self):
        while True:
            self.update_dt()

            # Handle states
            state = self.game_state_manager.get_state()

            if self.current_state != state and state == 'level':
                number = int(read_txt(LEVEL_PATH))
                self.level.reset(number)
                self.level_initialized = True
            self.current_state = state


            # Pause
            if self.is_paused == False:
                self.states[self.game_state_manager.get_state()].run()       
            else:
                self.paused.render_buttons()       


            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state_manager.exit()  

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.states[self.game_state_manager.get_state()].handle_click_events(event)

                    if self.is_paused:
                        self.paused.handle_click(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if not self.level.seeds_bank.current_dragging:
                            
                            if self.game_state_manager.get_state() != 'start':

                                if self.is_paused == False:
                                    self.is_paused = True
                                    self.paused.render()  
                                else:    
                                    self.is_paused = False

                    self.states[self.game_state_manager.get_state()].handle_keydown_events(event)

            debug(int(self.clock.get_fps()), -180, 1250, SHOW_FPS)
            pygame.display.flip()

game = Game()
game.run()