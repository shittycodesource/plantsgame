import pygame, sys, json
import globalvariables
from settings import *
from debug import *
from level import Level

class Game:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_caption("Vegetables Vs Cats")
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.level = Level(1, self) 

        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(60) / 1000


    def update_dt(self):
        self.dt = self.clock.tick(60) / 1000
        globalvariables.dt = self.dt


    def run(self):
        while True:
            self.update_dt()
            
            self.screen.fill((0, 0, 0))

            self.level.update(pygame.mouse.get_pos())
            self.level.render()

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()    

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.level.on_click(event.pos)
                    if event.button == 3:
                        if self.level.seeds_bank.current_dragging:
                            self.level.seeds_bank.stop_dragging()
                            self.level.board.showcase_image = None
                            self.level.board.showcase_image_rect = None

                # if event.type == pygame.MOUSEMOTION:
                #     self.level.on_mouse_move(event.pos)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.level.seeds_bank.current_dragging:
                            self.level.seeds_bank.stop_dragging()
                            self.level.board.showcase_image = None
                            self.level.board.showcase_image_rect = None

            self.level.on_mouse_move(pygame.mouse.get_pos())

            debug(int(self.clock.get_fps()), -180, 1250, SHOW_FPS)

            pygame.display.flip()


game = Game()
game.run()