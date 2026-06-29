import pygame, json, time
import globalvariables
from settings import *
from debug import *

from gamestatemanager import GameStateManager
from start import Start
from level import Level
from lost import Lost
from won import Won

from pause import Pause

class Game:

    def __init__(self):

        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_caption("Plants N Zombies 16x")
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(60) / 1000

        self.game_state_manager = GameStateManager('start')
        self.start = Start(self.screen, self.game_state_manager)        
        self.level = Level(self.screen, self.game_state_manager, 1, self)
        self.lost = Lost(self.screen, self.game_state_manager)
        self.won = Won(self.screen, self.game_state_manager)

        bg_music = pygame.mixer.Sound("../assets/background_music.mp3")
        bg_music.set_volume(0.2)
        bg_music.play(loops=-1)

        # self.level = Level(1, self, self.game_state_manager) 

        self.states = { 'start': self.start, 'level': self.level, 'lost': self.lost, 'won': self.won }

        self.paused = Pause(self.screen, self.game_state_manager, self)
        self.is_paused = False
        self.pause_dt = 0

        self.level_initialized = False
        self.current_state = self.game_state_manager.get_state()

        globalvariables.game_start_time = time.time()

        with open('score.txt', 'r') as file:
            globalvariables.score = int(file.readline())

    def update_dt(self):
        if self.is_paused == False:
            self.dt = (self.clock.tick(60) / 1000)
            self.pause_dt = 0
            globalvariables.dt = self.dt
            globalvariables.pause_time_delta = 0
            # print("Going", self.dt, self.pause_dt, self.dt - self.pause_dt)
        else:
            self.pause_dt += self.clock.tick(60) / 1000
            self.dt = 0
            globalvariables.dt = 0


    def run(self):
        while True:
            self.update_dt()

            state = self.game_state_manager.get_state()

            if self.current_state != state and state == 'level':
                number = 0
                with open('level.txt', 'r') as file:
                    number = int(file.readline())

                self.level.reset(number)
                self.level_initialized = True

            self.current_state = state

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
                                    globalvariables.pause_time_start = time.time()
                                    globalvariables.pause_time_end = time.time()
                                    self.is_paused = True
                                    self.paused.render()  
                                else:    
                                    globalvariables.pause_time_end = time.time()
                                    globalvariables.pause_time_delta = globalvariables.pause_time_end - globalvariables.pause_time_start
                                    self.is_paused = False


                    self.states[self.game_state_manager.get_state()].handle_keydown_events(event)

            debug(int(self.clock.get_fps()), -180, 1250, SHOW_FPS)
            pygame.display.flip()

game = Game()
game.run()