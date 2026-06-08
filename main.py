import pygame, sys
import random
from settings import *

from modules.Board import *
from modules.Manager import *

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))

board = Board(8, 5)
manager = Manager()

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()    

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                manager.handleClick(event.pos, board)

        if event.type == pygame.MOUSEMOTION:
            if manager.dragging != None:
                mouseX, mouseY = event.pos
                manager.dragPosX = mouseX
                manager.dragPosY = mouseY

    screen.fill((0, 0, 0))
    
    board.render(screen)
    manager.render(screen)

    pygame.display.flip()