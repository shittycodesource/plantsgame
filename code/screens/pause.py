import pygame

class Pause:
    def __init__(self, screen, game_state_manager, main_ref):
        self.display_surface = screen
        self.game_state_manager = game_state_manager
        self.main_ref = main_ref

        self.image = pygame.image.load('../assets/paused-overlay.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (1280, 720))
        self.image_rect = self.image.get_rect()

        self.window = pygame.image.load('../assets/paused-window.png').convert_alpha()
        self.window_rect = self.window.get_rect()
        self.window_rect.center = self.display_surface.get_rect().center

        self.buttons = [ { "state": "start", "name": "exit", "id": 0 }, { "state": 0, "name": "continue", "id": 1 } ] 
        self.button_surfs = [ pygame.transform.scale(pygame.image.load(f'../assets/paused-{btn['name']}.png').convert_alpha(), (161*2, 48*2)) for btn in self.buttons ]
        self.button_rects = [ btn.get_rect() for btn in self.button_surfs ]

        self.button_rects[0].center = self.display_surface.get_rect().center
        self.button_rects[1].center = self.display_surface.get_rect().center
        self.button_rects[0].y += 70
        self.button_rects[1].y -= 60

    def check_hovers(self, pos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        for i, rect in enumerate(self.button_rects):
            if rect.collidepoint(pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)


    def handle_click(self, event):
        if event.button == 1:
            for i, rect in enumerate(self.button_rects):
                if rect.collidepoint(event.pos):
                    if self.buttons[i]['state']:
                        self.main_ref.is_paused = False
                        self.game_state_manager.set_state(self.buttons[i]['state'])
                    else:
                        self.main_ref.is_paused = False
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


    def render_buttons(self):
        self.check_hovers(pygame.mouse.get_pos())
        for btn in self.buttons:
            self.display_surface.blit(self.button_surfs[btn['id']], self.button_rects[btn['id']])

    def render(self):
        self.display_surface.blit(self.image, self.image_rect)
        self.display_surface.blit(self.window, self.window_rect)
        self.render_buttons()