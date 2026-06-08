import pygame, sys, os
# from typing import Optional, List, tuple

sys.path.insert(0, os.path.abspath('../'))
from settings import *

# Board Class start
class Board:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.board = [ [0] * width for _ in range(height) ]

        self.cellSize = 70

        # Offset of the board
        self.left = (screenWidth  - self.width  * self.cellSize) // 2
        self.top  = (screenHeight - self.height * self.cellSize) // 2


    """Returns coordinates of a cell in self.board array"""
    def getCellIndexes(self, pos: tuple[float, float]) -> tuple[int, int] | tuple[None, None]:
        mouse_x, mouse_y = pos

        if (self.left < mouse_x) and (self.top < mouse_y):
            column = (mouse_x - self.left) // self.cellSize
            row    = (mouse_y - self.top)  // self.cellSize

            if (row < self.height) and (column < self.width):
                return column, row
        return None, None
    

    """ Returns cell style based on it's value in array"""
    def getCellStyle(self, column: int, row: int) -> tuple[str, int]:
        cellValue = self.board[row][column]

        if cellValue == 0: return "#ffffff", 1 # Empty cell
        else:              return plantsMap[cellValue]["color"], 0 # Not Empty


    """Not Used at the moment"""
    def onClick(self, column: int, row: int):
        if x != None and y != None:
            pass
            # self.board[y][x] = not self.board[y][x]


    """Executes if dragging plant from Manager.py and clicking on a cell"""
    def placePlant(self, column: int, row: int, id: int) -> bool:

        if (column != None) and (row != None):
            if self.board[row][column] == 0:
                self.board[row][column] = id
               
                return True

        return False


    """Main render function"""
    def render(self, screen):
        
        for i in range(self.width):
            for j in range(self.height):

                cellRect = pygame.Rect(
                    (i * self.cellSize) + self.left, 
                    (j * self.cellSize) + self.top, 
                    self.cellSize, self.cellSize
                )

                color, border = self.getCellStyle(i, j)
                pygame.draw.rect(screen, pygame.Color(color), cellRect, border)
                
# Board Class end