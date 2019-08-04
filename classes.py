from procedural_generation import *
class Player:
    def __init__(self, w, h, cellHeight, cols):
        self.width = w
        self.height = h
        self.x0 = 0
        self.x1 = self.width
        self.y1 = cellHeight * (cols-4)
        self.y0 = self.y1 - self.height
        self.jumpStartY = self.y0
        self.jumpHeight = cellHeight * 4
    
    def moveHorizontal(self, dx):
        self.x0 += dx
        self.x1 += dx
    
    def jump(self, dy):
        if self.y0 <= self.jumpHeight + self.jumpStartY:
            self.y1 += dy
            self.y0 += dy
        else:
            self.y1 -= dy
            self.y0 -= dy
        

