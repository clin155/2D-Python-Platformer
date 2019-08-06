from procedural_generation import *
from non_original_work import *
from other import *
import math
class Player:
    def __init__(self, w, h, data):
        self.width = w
        self.height = h
        startcell = getStartCell(data,1)
        self.row = startcell[0]-1
        self.col = startcell[1]
        self.fallSpd = 25
        self.maxCol = data.visibleCols//2 + 1
        self.minCol = 1
        self.minRow = 5
        self.maxRow = data.visibleRows - 5
        self.y0 = self.row*self.height
        self.startRow = None
        self.jumping = False
        self.falling = True
        self.inDescent = False
        self.jumpSpd = 20
        self.climbing = False
        self.inUpDownBlock = False
        self.lowerBound = None
        self.upperBound = None
        self.inBounds = False
        self.maxJump = 3
        self.hasPowerUp = None
        self.inUpLeft = False



    def resetY0(self):
        self.y0 = self.row*self.height

    def moveHorizontal(self, dx,grid,data):
        self.col += dx
        if self.checkForCollison(grid, data.firstVisibleCol, data):
                self.col -= dx
        if self.inUpDownBlock != True and self.inUpLeft != True:
            return self.scrollHorizontal(dx, data)
    
    def getBounds(self):
        x0 = self.col*self.width
        y0 = self.y0
        return x0, y0, x0+self.width, y0+self.height

    def checkForCollison(self, grid, col, data):
       # print(self.col, self.row)
        try:
            if grid[self.row][self.col + col] == True or grid[self.row][self.col + col] == "gravel":
                return True
            elif grid[self.row][self.col + col] == "ladder":
                self.falling = False
                self.climbing = True
            #prevents player from escaping the ladder upwards
            elif self.jumping == False:
                self.falling = True
                self.climbing = False
            if grid[self.row][self.col + col] == "jumpPower":
                grid[self.row][self.col+col] = False
                self.hasPowerUp = "jump"
                self.maxJump += 1
            return False
        except IndexError:
            data.gameOver = True
    def getRow(self):
        row = divide_round_up(self.y0,self.height)
        self.row = row

    def scrollHorizontal(self, dx, data):
        if self.col < self.minCol and data.firstVisibleCol > 0:
            self.col -= dx
            data.firstVisibleCol -= 1
            return True
        elif self.col < self.minCol:
            self.col -= dx
        elif self.col > self.maxCol:
            self.col -= dx
            data.firstVisibleCol += 1
            return True
        return False
    
    def moveVertical(self,data, dy):
        self.y0 += dy
        self.getRow()
        if self.checkForCollison(data.grid, data.firstVisibleCol, data):
            self.inBounds = False
            self.startRow = None
            self.y0 -= dy
            self.getRow()
            if self.inDescent == True:
                self.inDescent = False
                self.y0 = self.row*self.height
    
    def moveUpDownRow(self, data, dy):
        self.row += dy
        if self.climbing:
            self.scrollVertical(dy, data)

    def scrollVertical(self, dy, data):
        data.firstVisibleRow += dy
        if data.firstVisibleRow < self.lowerBound:
            data.firstVisibleRow -= dy
            print("fuck", data.firstVisibleRow, self.lowerBound)
            if data.firstVisibleRow % 23 == 0:
                self.climbing = False
                self.falling = False
        self.row += dy
        self.resetY0()


    def getMaxJumpRow(self, grid,data):
        if self.startRow == None:
            self.startRow = 1000
        return self.startRow - self.maxJump

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

    def checkForGravel(self, data):
        for i in range(4):
            if not self.climbing:
                try:
                    if data.grid[self.row][self.col + i] == "gravel":
                        return True
                    elif data.grid[self.row][self.col - i] == "gravel":
                        return True
                except IndexError:
                    continue
    def canvasGetBounds(self, data):
        x0, y0, x1,y1 = self.getBounds()
        y0 = y0 - (data.firstVisibleRow * data.cellHeight)
        y1 = y0 + self.height 
        return x0, y0, x1, y1

    def getCanvasCenter(self,data):
        x0, y0, x1,y1 = self.canvasGetBounds(data)
        cx = (x0+x1)/2
        cy = (y0+y1)/2
        return cx, cy

    def reversePowerUp(self):
        if self.hasPowerUp == "jump":
            self.maxJump -= 1


    def isOnLand(self, data):
        try:
            if data.grid[self.row+1][self.col+data.firstVisibleCol] == True:
                return True

        except IndexError:
            data.gameOver = True
        return False


