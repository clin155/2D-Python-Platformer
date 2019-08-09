	
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
		self.spd = 13

	def move(self, player, data):
		cx, cy = player.getCanvasCenter(data)
		theta = math.atan2((cy - self.cy), (cx-self.cx))
		self.cx += math.cos(theta)*self.spd
		self.cy += math.sin(theta)*self.spd
		self.collision(player, data)

	def draw(self, canvas, img):
		canvas.create_image(self.cx, self.cy, image=img)

	def drawShift(self, canvas, img, data):
		canvas.create_image(self.cx + data.shiftAmount, self.cy, image=img)
	
	def collision(self,player,data):
		cx, cy = player.getCanvasCenter(data)
		if abs(self.cx - cx) <= self.width//2 and abs(self.cy-cy) <= self.width//2:
			if not player.invincible:
				data.gameOver = True


