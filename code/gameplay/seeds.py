import pygame, time
from utils.jsondata import *

from settings.const import SEEDS_BANK_WIDTH, SEEDS_BANK_OFFSET_TOP, SEEDS_BANK_OFFSET_LEFT, SEEDS_BANK_HEIGHT, SEED_CARD_WIDTH, SEED_CARD_HEIGHT, SEEDS_CARDS_LEFT_OFFSET
from settings.paths import FONT_PATH

from plants.sunbloom import Sunbloom
from plants.peashooter import Peashooter
from plants.wallnut import Wallnut, Susnut, Sus

class SeedsBank:

    def __init__(self, level):
        self.display_surface = pygame.display.get_surface()

        self.level_ref = level

        self.seeds = level.seeds
        self.balance = level.balance
        self.balance_font = pygame.font.Font(FONT_PATH, 40)

        self.spriteWidth = SEEDS_BANK_WIDTH
        self.spriteHeight = SEEDS_BANK_HEIGHT

        self.offsetX = SEEDS_BANK_OFFSET_LEFT
        self.offsetY = SEEDS_BANK_OFFSET_TOP

        self.background = pygame.image.load('../assets/manager.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.spriteWidth * 4, self.spriteHeight * 4)) # Redo without * 4
        self.background_rect = self.background.get_rect()
        self.background_rect.x = self.offsetX
        self.background_rect.y = self.offsetY

        self.cards_offset = SEEDS_CARDS_LEFT_OFFSET 
        self.card_height = SEED_CARD_HEIGHT
        self.card_width = SEED_CARD_WIDTH
        self.card_font = pygame.font.Font(FONT_PATH, 30)

        self.card_half_height = self.card_height // 2
        self.card_half_width = self.card_width // 2

        self.cards_sprites = {
            "Sunbloom":   pygame.image.load('../assets/cards/Sunbloom.png').convert_alpha(),
            "Peashooter": pygame.image.load('../assets/cards/Peashooter.png').convert_alpha(),
            "Wallnut":    pygame.image.load('../assets/cards/Wallnut.png').convert_alpha(),
            # "Susnut":    pygame.image.load('../assets/cards/Susnut.png').convert_alpha(),
            # "Sus":    pygame.image.load('../assets/cards/Sus.png').convert_alpha()
        }

        self.cards_rectangles = [ None for i in range(len(self.cards_sprites)) ]
        self.cards_start_x = self.offsetX + self.cards_offset + 15
        self.resize_card_sprites()

        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.drag_pos_x = 0
        self.drag_pos_y = 0
        self.current_dragging = None # Tuple (cardIndex, plantName, rectangle, class)
        self.dragging_class = None
        self.dragging_group = pygame.sprite.Group()

        self.cooldown_shit   = [ None for i in range(len(self.cards_sprites)) ]
        self.cooldown_timers = [ 0 for i in range(len(self.cards_sprites)) ]
        self.cooldown_mask = pygame.image.load('../assets/cards/Sunbloom.png').convert_alpha()
            

    def resize_card_sprites(self):
        for card in self.cards_sprites: 
            image = self.cards_sprites[card]
            image = pygame.transform.scale(image, (self.card_width, self.card_height))
            self.cards_sprites[card] = image

    def get_balance(self):
        self.balance = self.level_ref.balance
        return self.level_ref.balance
        

    def check_click(self, pos):
        if self.background_rect.collidepoint(pos):
            return True
        return False


    def on_click(self, pos):
        if self.check_click(pos):
            for i, rect in enumerate(self.cards_rectangles):
                if rect.collidepoint(pos):
                    print(f"Plant {self.seeds[i]} clicked")

                    self.drag_plant(i, self.seeds[i], pos)


    def on_mouse_move(self, pos):
        if self.current_dragging != None:
            self.update_dragging_position(pos)
            

    def get_plant_cost(self, plant):
        global global_plants_data
        data = global_plants_data[plant]
        return data['cost']
    

    def is_plant_affordable(self, plant):
        cost = self.get_plant_cost(plant)

        if self.balance >= cost:
            return True
        return False


    def drag_plant(self, index, plant, pos):
        if self.is_plant_affordable(plant) and self.cooldown_shit[index] == None:
            self.stop_dragging()

            rectangle = self.cards_rectangles[index]

            mouse_x, mouse_y = pos
            self.drag_offset_x = rectangle.x - mouse_x
            self.drag_offset_y = rectangle.y - mouse_y

            self.drag_pos_x = rectangle.x + self.card_half_width
            self.drag_pos_y = rectangle.y + self.card_half_height

            cls = eval(plant)
            self.dragging_class = cls(self.dragging_group, [], [], [], interact=False, defeat_callback=None)
            self.current_dragging = (index, plant, rectangle, self.dragging_class)
        # else:
        #     self.jiggle_animation(index)


    def update_dragging_position(self, pos):
        mouse_x, mouse_y = pos
        self.drag_pos_x = mouse_x + self.drag_offset_x + self.card_half_width
        self.drag_pos_y = mouse_y + self.drag_offset_y + self.card_half_height


    def stop_dragging(self):
        if self.current_dragging != None:
            for sprite in self.dragging_group.copy(): sprite.kill()
            self.dragging_group.empty()

            self.cards_sprites[self.current_dragging[1]].set_alpha(255)
            self.current_dragging = None

    
    def start_cooldown(self, index, rectangle, name):
        surf = pygame.Surface((rectangle.width, 0), pygame.SRCALPHA)
        surf.fill((0, 0, 0))
        surf.set_alpha(180)

        surf = self.apply_mask(surf)

        pair = [ surf, rectangle, name ] 
        self.cooldown_shit[index] = pair


    def apply_mask(self, target_surface):
        return target_surface
        #what the fuck is this
        colored_mask = pygame.mask.from_surface(self.cooldown_mask)
        colored_mask.blit(target_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return colored_mask


    def render_cooldowns(self):
        for shit in self.cooldown_shit:
            if shit != None:
                
                surf = shit[0]
                rect = shit[1]

                self.display_surface.blit(surf, rect)


    def update(self, dt):
        self.get_balance()
        self.update_cooldowns(dt)



    def update_cooldowns(self, dt):
        for index, shit in enumerate(self.cooldown_shit):
            if shit != None:
                self.cooldown_timers[index] += dt

                if self.cooldown_timers[index] >= 7.5:
                    self.cooldown_shit[index] = None
                    self.cooldown_timers[index] = 0
                    return
                # fuck this shit i fucking hate this cooldown system its ugly and buggy
                surf = shit[0]
                rect = shit[1]
                name = shit[2]

                global global_plants_data
                data = global_plants_data[name]
                
                new_height = ((self.cooldown_timers[index] / data['cooldown']) * SEED_CARD_HEIGHT) + 1
                modified_surf = pygame.transform.scale(surf, (rect.width, new_height))
                # rect.y = rect.y + (SEED_CARD_HEIGHT - new_height)

                rect.y = self.offsetY + 17 + (SEED_CARD_HEIGHT - new_height) + 1

                modified_surf.fill((0, 0, 0))
                modified_surf.set_alpha(180)
                
                modified_surf = self.apply_mask(modified_surf)


                self.cooldown_shit[index] = [ modified_surf, rect, name ]


    def render_drag(self):
        # current_dragging = Tuple[cardIndex, plantName, rectangle]
        if self.current_dragging != None:
            image = self.dragging_class.image
            image_rect = image.get_rect(center=(self.drag_pos_x , self.drag_pos_y))

            self.display_surface.blit(image, image_rect)


    def render_balance(self):
        target_rect = pygame.Rect(26, 120, 112, 34)
        # pygame.draw.rect(self.display_surface, 'Black', target_rect, 1)

        text_surf = self.balance_font.render(str(self.get_balance()), True, (117, 85, 29))
        text_rect = text_surf.get_rect(center=target_rect.center)
        # pygame.draw.rect(self.display_surface, 'Gray', text_rect, 1)

        self.display_surface.blit(text_surf, text_rect)


    def render_seeds_cards(self):
        for i, seed in enumerate(self.seeds):
            image = self.cards_sprites[seed]
            image_rect = image.get_rect()

            image_rect.width = self.card_width
            image_rect.height = self.card_height
            image_rect.x += self.cards_start_x + (i * (self.card_width + 10))
            image_rect.y = self.offsetY + 17

            is_affordable = self.is_plant_affordable(seed)

            if is_affordable == False: image.set_alpha(80)
            elif self.cooldown_shit[i] != None: image.set_alpha(120)
            else:                      image.set_alpha(255)

            if self.current_dragging != None:
                if self.current_dragging[0] == i:
                    image.set_alpha(180)

            self.cards_rectangles[i] = image_rect
            self.display_surface.blit(image, image_rect)

            # Cost
            target_rect = pygame.Rect(image_rect.x, image_rect.y + 42, 66, 26)
            text_surf = self.card_font.render(str(self.get_plant_cost(seed)), True, (152, 138, 102) if is_affordable else (71, 66, 54))
            text_rect = text_surf.get_rect(center=target_rect.center)
            self.display_surface.blit(text_surf, text_rect)


    def render(self):
        self.display_surface.blit(self.background, self.background_rect)
        self.render_seeds_cards()
        self.render_balance()
        self.render_cooldowns()
        self.render_drag()