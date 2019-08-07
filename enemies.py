	
from procedural_generation import *
import copy
from classes import *
def moveEnemies(dx,dy,data):
	for ghost in data.ghosts:
		ghost.cx += (dx*data.cellWidth)
		ghost.cy += (dy*data.cellHeight)


def removeGhosts(data):
	newGhostList = []
	for ghost in data.ghosts:
		if ghost.cx < 0 or ghost.cx > data.width or ghost.cy < 0 or ghost.cy > data.height:
			continue
		else:
			newGhostList.append(ghost)
	data.ghosts = copy.copy(newGhostList)


def createNewGhosts(data):
	for i in range(data.numGhosts):
		data.ghosts.append(Ghost(data))


#ghost class
class Ghost:
	def __init__(self, data):
		self.cx = random.randint(0,data.width)
		self.cy = 0
		self.width = data.cellWidth*2
		self.height = data.cellHeight *2
		self.direction = [0,0]
		self.spd = 12

	def move(self, player, data):
		cx, cy = player.getCanvasCenter(data)
		theta = math.atan2((cy - self.cy), (cx-self.cx))
		self.cx += math.cos(theta)*self.spd
		self.cy += math.sin(theta)*self.spd
		self.collision(player, data)

	def draw(self, canvas, img):
		canvas.create_image(self.cx, self.cy, image=img)
	
	def collision(self,player,data):
		cx, cy = player.getCanvasCenter(data)
		if abs(self.cx - cx) <= self.width//2 and abs(self.cy-cy) <= self.width//2:
			data.gameOver = True


# class GroundEnemy():
#     def __init__(self, row, col, data):
#         self.row = row
#         self.col = col
#         self.facingImage = data.rightFacingEnemy
#         self.width = data.cellWidth
#         self.height = data.cellHeight
#         self.direction = 0
#         self.ToRemove = False

#     def isOnLand(self, data):
#         try:
#             if data.grid[self.row+1][self.col+data.firstVisibleCol] == True:
#                 return True
#         except IndexError:
#             self.ToRemove = True
#     def pathFinding(self, data):
#         self.getDesiredDirection(data.player, data.firstVisibleCol)
#         if self.direction == 1:
#             self.moveRight(1,data.grid, data.rightFacingEnemy)
#             self.moveDown(1, data.grid, data.rightFacingEnemy)
#             if data.grid[self.row][self.col+1] == True:
#                 self.moveUp(1, data.grid, data.rightFacingEnemy)
#         elif self.direction == -1:
#             self.moveLeft(1, data.grid, data.leftFacingEnemy)
#             self.moveDown(1, data.grid, data.rightFacingEnemy)
#             if data.grid[self.row][self.col-1] == True:
#                 self.moveUp(1, data.grid, data.leftFacingEnemy)


#     def draw(self, canvas, data):
#         cx, cy = self.getCanvasCenter(data)
#         canvas.create_image(cx, cy, image=self.facingImage)

#     def getDesiredDirection(self, player, scrollAmount):
#         temp = player.col + scrollAmount
#         if temp> self.col:
#             self.direction = 1
#         elif temp < self.col:
#             self.direction = -1
#         elif temp == self.col:
#             self.direction = 0

#     def moveVertical(self, data, dy):
#         self.y0 += dy
#         self.getRow()
#         if self.checkForCollison(data.grid):
#             self.startRow = None
#             self.y0 -= dy
#             self.getRow()
#             if self.inDescent == True:
#                 self.inDescent = False
#                 self.y0 = self.row*self.height

#     def moveUp(self,dr,grid,img):
#         self.row -= dr
#         if self.checkForCollison(grid):
#             self.row += dr
#         else:
#             self.facingImage = img


#     def moveDown(self,dr,grid,img):
#         self.row += dr
#         if self.checkForCollison(grid):
#             self.row -= dr
#         else:
#             self.facingImage = img

#     def moveRight(self,dr,grid,img):
#         self.col += dr
#         if self.checkForCollison(grid):
#             self.col -= dr
#         else:
#             self.facingImage = img

#     def moveLeft(self,dr,grid, img):
#         self.col -= dr
#         if self.checkForCollison(grid):
#             self.col += dr
#         else:
#             self.facingImage = img


#     def checkForCollison(self,grid):
#         try:
#             if grid[self.row][self.col] == True:
#                 return True
#             return False
#         except IndexError:
#             self.ToRemove = True
#             return True


#     def checkPlayerCollision(self, player, scrollAmount):
#         if self.col == player.col + scrollAmount and \
#             self.row == player.row:
#             return True
#         return False

#     def getBounds(self):
#         x0 = self.col*self.width
#         y0 = self.row*self.width
#         return x0, y0, x0+self.width, y0+self.height
	
#     def inBounds(self, data):
#         if data.firstVisibleCol <= self.col and self.col <= data.firstVisibleCol+data.visibleCols*2:
#             if self.row >= data.firstVisibleRow and self.row <= data.firstVisibleRow + data.visibleRows*2:
#                 return True
#         return False
#     def canvasGetBounds(self, data):
#         x0, y0, x1,y1 = self.getBounds()
#         y0 = y0 - (data.firstVisibleRow * data.cellHeight)
#         y1 = y0 + self.height
#         x0 = x0 - (data.firstVisibleCol * data.cellWidth)
#         x1 = y0 + self.width
#         return x0, y0, x1, y1

#     def getCanvasCenter(self,data):
#         x0, y0, x1,y1 = self.canvasGetBounds(data)
#         cx = (x0+x1)/2
#         cy = (y0+y1)/2
#         return cx, cy