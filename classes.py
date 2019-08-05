from procedural_generation import *
from non_original_work import *

class Player:
    def __init__(self, w, h, data):
        self.width = w
        self.height = h
        startcell = getSurfaceBlock(data.grid,data,1)
        self.row = startcell[0]-1
        self.col = startcell[1]
        self.fallSpd = 25
        self.maxCol = data.visibleCols//2 + 1
        self.minCol = 1
        self.y0 = self.row*self.height
        self.startRow = None
        self.jumping = False
        self.falling = True
        self.inDescent = True
        self.jumpSpd = 20

    def moveHorizontal(self, dx,grid,data):
        self.col += dx
        if self.checkForCollison(grid, data.firstVisibleCol):
                self.col -= dx
        self.scrollHorizontal(dx, data)
    

    def getBounds(self):
        x0 = self.col*self.width
        y0 = self.y0
        return x0, y0, x0+self.width, y0+self.height

    def checkForCollison(self, grid, col):
        if grid[self.row][self.col + col] == True:
            return True
        return False

    def getRow(self):
        row = divide_round_up(self.y0,self.height)
        self.row = row

    def scrollHorizontal(self, dx, data):
        if self.col < self.minCol and data.firstVisibleCol > 0:
            self.col -= dx
            data.firstVisibleCol -= 1
        elif self.col < self.minCol:
            self.col -= dx
        elif self.col > self.maxCol:
            self.col -= dx
            data.firstVisibleCol += 2
    

    def moveVertical(self,data, dy):
        self.y0 += dy
        self.getRow()
        if self.checkForCollison(data.grid, data.firstVisibleCol):
            self.startRow = None
            self.y0 -= dy
            self.getRow()
            if self.inDescent == True:
                self.inDescent = False
                self.y0 = self.row*self.height
    
    def getMaxJumpRow(self, grid,data):
        if self.startRow == None:
            self.startRow = 1000
        return self.startRow - 3

    def startJump(self):
        self.startRow = self.row
        self.jumping = True    
        self.falling = False

    def jump(self, data):
        self.moveVertical(data, -self.jumpSpd)
        if self.row <= self.getMaxJumpRow(data.grid, data) or self.falling == True:
            self.jumping = False
            self.falling = True
            self.inDescent = True
    
    def fall(self, data):
        self.inDescent = True
        if self.jumping == False:
            self.moveVertical(data, self.fallSpd)


    #     if self.y0 >= self.jumpStartY - self.jumpHeight:
    #         self.y1 -= dy
    #         self.y0 -= dy     


    # def falling(self, data):
    #     self.y1 += self.fallSpd
    #     self.y0 += self.fallSpd
    #     playerCells = self.getCellAll(data.cellHeight, data.cellWidth)
    #     for tup in playerCells:
    #         if data.grid[tup[0]][tup[1]] == True:
    #             self.x0 -= self.fallSpd
    #             self.x1 -= self.fallSpd
    #             break
            
    # def getCellAll(self, cellHeight, cellWidth):
    #     tup = self.getCellX0Y0(cellHeight, cellWidth, self.x0+self.scrollX, self.y0)
    #     # if inCell == 0:
    #     return [tup, (tup[0]+1, tup[1])]
    #     # elif inCell == 1:
    #     #     return  [tup, (tup[0]+1, tup[1]), (tup[0], tup[1]+1), (tup[0]+1, tup[1]+1)]
    #     # else:
    #     #     return [tup,(tup[0]+1, tup(1)), (tup[0], tup[1]+1), (tup[0]+1, tup[1]+1), (tup[0]+2, tup[1]), (tup[0]+2, tup[1]+1)]

    # # def getCellX0Y0(self, cellHeight, cellWidth, x, y):
    # #     col = x//cellWidth
    # #     row = y//cellHeight
    # #     if x % cellWidth == 0 and y % cellHeight == 0:
    # #         return (row, col), 0
    # #     elif y % cellHeight == 0 and x % cellWidth != 0:
    # #         return (row, col), 1
    # #     return (row, col), 2

    # def getCellX0Y0(self, cellHeight, cellWidth, x, y):
    #     col = x//cellWidth
    #     row = y//cellHeight
    #     print(col)
    #     return (row, col)