from procedural_generation import *
from non_original_work import *
from other import *
import math
class Player:
	def __init__(self, w, h, data):
		self.width = w
		self.height = h
		startcell = self.getStartCell(data,1)
		self.row = startcell[0]-1
		self.col = startcell[1]
		self.fallSpd = 20
		self.maxCol = data.visibleCols//2 + 1
		self.minCol = 1
		self.minRow = 5
		self.maxRow = data.visibleRows - 5
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
		self.maxJump = 4
		self.baseMaxJump = 3
		self.hasPowerUp = None
		self.inUpLeft = False
		self.onTopOfLadder = False
		self.invincible = False

	def getStartCell(self, data, col):
		for row in range(data.firstVisibleRow + data.visibleRows//2,\
			data.firstVisibleRow+data.visibleRows):
			if data.grid[row][col] == True:
				return (row, col)
		return(12, 12)



	def moveHorizontal(self, dx,grid,data):
		self.col += dx
		if self.checkForCollison(grid, data.firstVisibleCol, data):
				self.col -= dx
		if self.inUpDownBlock != True and self.inUpLeft != True and data.scroll==True:
			return self.scrollHorizontal(dx, data)
	
	def getBounds(self):
		x0 = self.col*self.width
		y0 = self.row*self.height
		return x0, y0, x0+self.width, y0+self.height

	def checkForCollison(self, grid, col, data):
		try:
			if grid[self.row][self.col + col] == True or grid[self.row][self.col + col] == "gravel":
				self.inDescent = False
				return True
			elif grid[self.row][self.col + col] == "ladder":
				self.falling = False
				self.climbing = True
			#prevents player from escaping the ladder upwards
			elif grid[self.row+1][self.col + col] == "ladder" and data.firstVisibleRow % 24 == 0:
				self.onTopOfLadder = True
				print("kachow")
				# self.climbing = True
				self.inDescent = False


			#jumpPowerUp
			if grid[self.row][self.col + col] == "jumpPower":
				grid[self.row][self.col+col] = False
				self.hasPowerUp = "jump"
				self.maxJump += 1

			#shield
			if grid[self.row][self.col + col] == "shield":
				grid[self.row][self.col+col] = False
				self.hasPowerUp = "shield"
				self.invincible = True
			return False
		except IndexError:
			data.gameOver = True


	def scrollHorizontal(self, dx, data):
		if self.col < self.minCol and data.firstVisibleCol > 0:
			self.col -= dx
			data.firstVisibleCol -= 1
			for background in data.backgrounds:

				background.scroll(data, -1, 0)
			return True
		elif self.col < self.minCol:
			self.col -= dx
		elif self.col > self.maxCol:
			self.col -= dx
			data.firstVisibleCol += 1
			for background in data.backgrounds:
				background.scroll(data, 1, 0)
			for obj in data.flyingObjects:
				obj.move(data)
			return True
		return False
	

	def moveVertical(self,data,dy):
		self.row += dy
		if self.checkForCollison(data.grid, data.firstVisibleCol, data):
			self.row -= dy
	
	def moveUpDownRow(self, data, dy):
		if data.grid[self.row+1][self.col+data.firstVisibleCol] == True or\
			data.grid[self.row+2][self.col+data.firstVisibleCol] == True:
			if dy == 1: return None
		self.row += dy
		if self.climbing:
			self.scrollVertical(dy, data)

	def scrollVertical(self, dy, data):
		data.firstVisibleRow += dy
		if data.firstVisibleRow < self.lowerBound or\
			data.firstVisibleRow+data.visibleRows > self.upperBound:
			data.firstVisibleRow -= dy



	def getMaxJumpRow(self, grid,data):
		if self.startRow == None:
			self.startRow = 1000
		return self.startRow - self.maxJump

	def startJump(self):
		self.startRow = self.row
		self.jumping = True    
		self.falling = False
		self.climbing = False

	def jump(self, data):
		self.moveVertical(data, -1)
		if self.row <= self.getMaxJumpRow(data.grid, data) or self.falling == True:
			self.jumping = False
			self.falling = True
			self.inDescent = True
	
	def fall(self, data):
		if self.jumping == False:
			self.moveVertical(data, 1)

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
		if self.hasPowerUp == "shield":
			self.invincible = False


	def isOnLand(self, data):
		if data.grid[self.row+1][self.col+data.firstVisibleCol] == True:
			return True
		return False

	def checkForObstacle(self, data):
		try:
			if data.grid[self.row][self.col + data.firstVisibleCol] == "obstacle":
				if not self.invincible:
					data.gameOver = True					

		except IndexError:
			data.gameOver = True

	def checkIfWon(self, data):
		if data.grid[self.row][self.col+data.firstVisibleCol] == "flag":
			data.won = True


class Background:

	def __init__(self, img, data, cx, cy, width):
		self.width =  width
		self.height = int(data.height)
		self.img = img
		self.background = self.createImage(data)
		self.cx = cx
		self.cy = cy


	def createImage(self,data):
		return createImage(data, self.width, self.height, self.img)

	def draw(self, canvas):
		canvas.create_image(self.cx, self.cy, image=self.background)

	def drawShift(self, canvas, data):
		canvas.create_image(self.cx+data.shiftAmount, self.cy, image=self.background)

	def scroll(self, data, dx, dy):
		self.cx += ((data.firstVisibleCol*data.cellWidth)/50)*dx*-1
		self.cy += ((data.firstVisibleRow*data.cellHeight)/50)*dy*-1


	def needNewBackground(self, data):
		if self.cx + self.width/2 < self.width:
			cx = self.cx + self.width
			cy = self.cy
			data.backgrounds.insert(0, Background(data.backgroundImage, data, cx, cy, self.width))




class FlyingObject:

	def __init__(self,data, player):
		self.width = int(data.cellWidth*1.5)
		self.height = int(data.cellHeight*1.5)
		self.cx = data.width + self.width
		self.cy = random.randint(self.height//2, data.height-(self.height//2))
		self.speed = data.objSpd
		self.player = player


	def draw(self, canvas,data):
		canvas.create_image(self.cx, self.cy, image=data.flyingObjectImage)

	def drawShift(self, canvas, data):
		canvas.create_image(self.cx+data.shiftAmount, self.cy, image=data.flyingObjectImage)

	def move(self, data):
		self.cx -= self.speed
		self.collision(self.player, data)

	def collision(self,player,data):
		cx, cy = player.getCanvasCenter(data)
		if abs(self.cx - cx) <= self.width//2 and abs(self.cy-cy) <= self.width//2:
			if not player.invincible:
				data.gameOver = True