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

    screen.fill((0, 0, 0))
    board.render(screen)
    manager.render(screen)

    # Events Loops
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()    

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                manager.handleClick(event.pos, board)

        if event.type == pygame.MOUSEMOTION:
            if manager.dragging != None:
                manager.setDraggingPos(event.pos)


    # Handle board hover effect while dragging
    mousePos = pygame.mouse.get_pos()
    if manager.dragging != None:
        board.handleHover(mousePos, manager.dragging)


    pygame.display.flip()