import pygame, sys, os

sys.path.insert(0, os.path.abspath('../'))
from settings import *


# Manager Class start
class Manager:

    def __init__(self):
        self.cards = [ 1, 2, 3 ]
        self.cardsRects = [ ]

        # Drag Data
        self.dragging = None
        self.dragPosX = 0 
        self.dragPosY = 0
        self.dragOffsetX = 0
        self.dragOffsetY = 0

        # Cards Data
        self.cardWidth = 60
        self.cardHeight = 60
        self.gap = 10 # between plants's cards

        # Base Rect data
        self.left = 20
        self.top = 20
        self.width = screenWidth / 2
        self.height = 80
        self.managerRect = pygame.Rect(self.left, self.top, self.width, self.height)


    """Returns index of card's index by position"""
    def getCardIndexByPos(self, pos: tuple[float, float]) -> int:
        for cardRectIndex, cardRect in enumerate(self.cardsRects):
            if cardRect.collidepoint(pos):
                return cardRectIndex
        return None


    """ Returns plant data from map using array index """
    def getCardData(self, index: int) -> dict: 
        return plantsMap[self.cards[index]]


    """ Returns card rectangle by index """
    def getCardRect(self, index: int) -> pygame.Rect:
        return self.cardsRects[index]


    # For smooth dragging
    """ Set initial dragging position and dragging offset """ 
    def setDraggingOffset(self, index: int, pos: tuple[float, float]) -> None:
        cardRect = self.getCardRect(index)

        mouseX, mouseY = pos
        self.dragOffsetX = cardRect.x - mouseX
        self.dragOffsetY = cardRect.y - mouseY

        # set normal position so when you click at card, it doesnt appear in the other part of the screen
        self.dragPosX = cardRect.x - mouseX
        self.dragPosY = cardRect.y - mouseY


    """Sets position for dragged element"""
    def setDraggingPos(self, pos: tuple[float, float]) -> None:
        mouseX, mouseY = pos
        self.dragPosX = mouseX
        self.dragPosY = mouseY


    """ Handles everything related to clicks"""
    def handleClick(self, pos, board) -> None:
        if self.dragging != None: # If dragging something and clicked
            x, y = board.getCellIndexes(pos)

            if x != None and y != None:
                id = self.cards[self.dragging]
                board.placePlant(x, y, id)
            self.dragging = None

        else: # If nothing is being dragged
            cardIndex = self.getCardIndexByPos(pos) # returns None if clicked outside of Manager

            if cardIndex != None:
                self.dragging = cardIndex
                self.setDraggingOffset(cardIndex, pos)


    """ Render plant's cards in manager """
    def renderCards(self, screen) -> None:
        self.cardsRects = [  ] 
        
        offsetX = self.managerRect.x + 10
        offsetY = self.managerRect.y + (self.managerRect.height - self.cardHeight) // 2
        
        for idIndex, id in enumerate(self.cards):
            cardX = offsetX + idIndex * (self.cardWidth + self.gap)
            cardY = offsetY
            
            cardRect = pygame.Rect(cardX, cardY, self.cardWidth, self.cardHeight)
            self.cardsRects.append(cardRect)
            
            plant = plantsMap[id]
            color = plant["color"]
            pygame.draw.rect(screen, pygame.Color(color), cardRect)
            pygame.draw.rect(screen, pygame.Color("#000000"), cardRect, 2)


    """ Render moving rectangle """
    def renderDragging(self, screen) -> None:
        data = self.getCardData(self.dragging)

        posX = self.dragPosX + self.dragOffsetX
        posY = self.dragPosY + self.dragOffsetY

        pygame.draw.rect(
            screen, 
            pygame.Color(data["color"]), 
            ( (posX, posY), (self.cardWidth, self.cardHeight) )
        )


    """ Main render function. Calls cards and dragging rendering. """
    def render(self, screen) -> None:
        pygame.draw.rect(screen, pygame.Color("#2c2c2c"), self.managerRect)
        pygame.draw.rect(screen, pygame.Color("#ffffff"), self.managerRect, 2) # border cuz looks cool

        self.renderCards(screen)

        if self.dragging != None: self.renderDragging(screen)

# Manager Class end