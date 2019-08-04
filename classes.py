from procedural_generation import *
from other import *

class Player:
    def __init__(self, w, h, cellHeight, rows, data):
        self.width = w
        self.height = h
        self.x0 = data.scrollMarginLeft
        self.x1 = self.width
        startcell = getSurfaceBlock(data.grid,data,0)
        self.y1 = cellHeight * startcell[0]
        self.y0 = self.y1 - self.height
        self.jumpStartY = self.y0
        self.jumpHeight = cellHeight * 4
        self.jumping = False
        self.fallSpd = 10
    
    def moveHorizontal(self, dx, cellHeight, cellWidth, grid, data):
        self.x0 += dx
        self.x1 += dx
        playerCells = self.getCellAll(cellHeight, cellWidth)
        for tup in playerCells:
            if data.grid[tup[0]][tup[1]] == True:
                self.x0 -= self.fallSpd
                self.x1 -= self.fallSpd
                break
        self.scrollHorizontal(dx, data)
            
    def scrollHorizontal(self, dx, data):
        if self.x0 < data.scrollMarginLeft:
            self.x0 -= dx
            self.x1 -= dx
            data.scrollX += dx
            moveGridLeft(data)
        if self.x1 > data.width - data.scrollMarginRight:
            self.x0 -= dx
            self.x1 -= dx
            data.scrollX += dx
            moveGridRight(data)
    def jump(self, dy, data):
        if self.y0 >= self.jumpStartY - self.jumpHeight:
            self.y1 -= dy
            self.y0 -= dy     


    def falling(self, data):
        self.y1 += self.fallSpd
        self.y0 += self.fallSpd
        playerCells = self.getCellAll(data.cellHeight, data.cellWidth)
        for tup in playerCells:
            if data.grid[tup[0]][tup[1]] == True:
                self.x0 -= self.fallSpd
                self.x1 -= self.fallSpd
                break
            
    def getCellAll(self, cellHeight, cellWidth):
        tup, inCell = self.getCellX0Y0(cellHeight, cellWidth, self.x0, self.y0)
        if inCell == 0:
            return [tup, (tup[0]+1, tup[1])]
        elif inCell == 1:
            return  [tup, (tup[0]+1, tup[1]), (tup[0], tup[1]+1), (tup[0]+1, tup[1]+1)]
        else:
            return [tup,(tup[0]+1, tup(1)), (tup[0], tup[1]+1), (tup[0]+1, tup[1]+1), (tup[0]+2, tup[1]), (tup[0]+2, tup[1]+1)]

    def getCellX0Y0(self, cellHeight, cellWidth, x, y):
        col = x//cellWidth
        row = y//cellHeight
        if x % cellWidth == 0 and y % cellHeight == 0:
            return (row, col), 0
        elif y % cellHeight == 0 and x % cellWidth != 0:
            return (row, col), 1
        return (row, col), 2
