from non_original_work import *
from tkinter import *
from other import *
from procedural_generation import *
from classes import *
from enemies import *
import copy, string, os

def getLevel(data):
	file = open(data.textFile, "r")
	for line in file.readlines():
		if line.startswith("multiLevel:"):
			file.close()
			linestr = line.replace("multiLevel:","")
			return int(linestr[0])


def createButton(data, x,y, canvas, Text):
	width = 60
	height = 40
	canvas.create_rectangle(x-width, y-height, x+width, y+ height, fill="yellow")
	canvas.create_text(x, y, text=Text, font = "Arial 15")
	return (x-width, y-height, x+width, y+ height)

def createflyingObjects(data):
	for i in range(data.numFlyingObjects):
		data.flyingObjects.append(FlyingObject(data, data.player))




def init(data, grid=None):
	#data stuff for procedural generation
	data.visibleCols = 32
	data.visibleRows = 24
	data.firstVisibleCol = 0
	data.firstVisibleRow = 0
	data.cellWidth = int(data.width / data.visibleCols)
	data.cellHeight = int(data.height /data.visibleRows)
	data.emptyBlock = [[False]*data.visibleCols for i in range(data.visibleRows)]
	#values to be changed by level #CHANGE GAME LEVEL BEFORE SUBMITTING
	data.backgrounds = []
	data.numGhosts = 1
	data.gameLength = 10
	data.textFile = "data.txt"
	data.backgroundImage = None
	data.flyingObjectImage = None
	data.block = None
	data.numFlyingObjects = 2
	data.objSpd = 10
	data.maxNumObstacles = 3
	data.level = getLevel(data)
	setLevelValues(data)
	data.numBlocks = 4

	if grid == None:
		data.grid = copy.deepcopy(data.emptyBlock)
		createStartBlock(data)
		for i in range(2):
			addBlocktoGrid(data, 0, True)
	
	else:
		data.grid = grid


	#scroll data
	data.scrollMarginLeft = 30
	data.scrollMarginRight = data.width//2 + 60
	data.player = Player(data.cellWidth, data.cellHeight,data)
	#load Images
	data.playerImage = createImage(data,data.player.width, data.player.height, "player.png")
	data.gravel = createImage(data, data.cellWidth, data.cellHeight, "gravel.jpg")
	data.ladder = createImage(data, data.cellWidth, data.cellHeight, "ladder.png")
	data.ghost = createImage(data, int(data.cellWidth*1.5), int(data.cellHeight*1.5), "ghost.png")
	data.jumpPower = createImage(data, data.cellWidth, data.cellHeight, "jumpPower.png")
	data.obstacle = createImage(data, data.cellWidth, data.cellHeight, "spike.png")
	data.flag = createImage(data, data.cellWidth, data.cellHeight, "flag.png")
	data.shield = createImage(data,data.cellWidth, data.cellHeight, "basicShield.png")



	data.timeElapsed = 0
	data.powerUpTime = 0
	data.addObjTime = 0
	#ghost enemies

	data.ghosts = []
	data.flyingObjects = []



	#UNCOMMENT THESE

	# createNewGhosts(data)
	# createflyingObjects(data)



	data.gameOver = False
	data.won = False
	data.createBlocks = True
	data.scroll = True

	data.quitButton = []
	data.playButtonCoords = []
	data.singleButton = []
	data.multiButton = []
	data.backButton = []


def mousePressed(event, data):
	pass	
def keyPressedHelper(event, data):
	if not data.won:
		# use event.char and event.keysym
		if not data.gameOver:
			if event.keysym == "Right" and not data.player.climbing:
				if data.player.moveHorizontal(1, data.grid, data):
					moveEnemies(-1, 0,data)
			if event.keysym == "Left" and not data.player.climbing:
					if data.player.moveHorizontal(-1, data.grid, data):
						moveEnemies(1,0,data)
			if event.keysym == "space":
				if data.player.jumping == False and data.player.inDescent == False: 
					data.player.startJump()
				if data.player.climbing:
					data.player.startJump()
			if event.keysym == "Up" and data.player.climbing and not data.player.onTopOfLadder:
				data.player.moveUpDownRow(data, -1)
				moveEnemies(0,1,data)
			if event.keysym == "Down":
				data.player.moveUpDownRow(data, 1)

			#prevents phasing into a block if user spams right or left
			while data.player.checkForCollison(data.grid, data.firstVisibleCol, data):
				if event.keysym == "Right":
					data.player.col -= 1
				if event.keysym == "Left":
					data.player.col += 1
		if event.keysym == "l":
			init(data, data.grid)
	# if data.won:
	# 	if event.keysym == "n":
	# 			replaceText("level:"+str(data.level), "level:"+str(data.level+1), data.textFile)
	# 			init(data)
	# 			data.won = False
	if event.keysym == "i":
		replaceText("level:"+str(data.level), "level:0", data.textFile)

def keyPressedHelper2(event, data):
	if not data.won:
		# use event.char and event.keysym
		if not data.gameOver:
			if event.keysym == "d" and not data.player.climbing:
				if data.player.moveHorizontal(1, data.grid, data):
					moveEnemies(-1, 0,data)
			if event.keysym == "a" and not data.player.climbing:
				if data.player.moveHorizontal(-1, data.grid, data):
					moveEnemies(1,0,data)
			if event.keysym == "g":
				if data.player.jumping == False and data.player.inDescent == False: 
					data.player.startJump()
				if data.player.climbing:
					data.player.startJump()
			if event.keysym == "w" and data.player.climbing and not data.player.onTopOfLadder:
				data.player.moveUpDownRow(data, -1)
				moveEnemies(0,1,data)
			if event.keysym == "s"and not data.player.onTopOfLadder:
				data.player.moveUpDownRow(data, 1)

			#prevents phasing into a block if user spams right or left
			while data.player.checkForCollison(data.grid, data.firstVisibleCol, data):
				if event.keysym == "d":
					data.player.col -= 1
				if event.keysym == "a":
					data.player.col += 1
		if event.keysym == "r":
			init(data, data.grid)
	# if data.won:
	# 	if event.keysym == "n":
	# 			replaceText("level:"+str(data.level), "level:"+str(data.level+1), data.textFile)
	# 			init(data)
	# 			data.won = False
	if event.keysym == "i":
		replaceText("level:"+str(data.level), "level:0", data.textFile)
def timerFiredHelper(data):
	if not data.won:
		data.timeElapsed += 1
		if data.player.row >= data.firstVisibleRow + data.visibleRows-1: 
			data.gameOver = True
		try:
			if data.player.checkForGravel(data): 
				data.gameOver = True
		except IndexError:
			data.gameOver = True
		if not data.gameOver:
			if data.player.isOnLand(data) and not data.player.jumping: data.player.falling = True
			if data.player.falling:
				data.player.fall(data)
			if data.player.jumping:
				data.player.jump(data)
			#get vertical scroll bounds
			if data.player.inUpDownBlock == True:
				if data.firstVisibleRow <= data.visibleRows and not data.player.climbing and data.player.isOnLand(data):
					data.player.lowerBound, data.player.upperBound = getVerticalScrollBounds(data)
					data.player.inUpDownBlock = False
				elif data.firstVisibleRow <= data.visibleRows*2 and not data.player.climbing and data.player.isOnLand(data):
					data.player.lowerBound, data.player.upperBound = getVerticalScrollBounds(data)

			#prevents error when in upLeft
			if data.player.inUpLeft == True:
				if data.player.row < data.visibleRows -4:
					data.player.inUpLeft = False
					data.player.inUpDownBlock = False


			#enemies
			for ghost in data.ghosts:
				ghost.move(data.player, data)

			for obj in data.flyingObjects:
				obj.move(data)
			removeGhosts(data)

			#prevents ghosts from spawning when climbing:
			if data.player.climbing == True:
				data.ghosts = []
			#CHANGE THIS
			# #spawns the enemies ##################
			# if data.timeElapsed % 50 == 0 and len(data.ghosts) == 0 and not data.player.climbing:
			#     createNewGhosts(data)
			# ##################



			if data.numBlocks >= data.gameLength:
				data.createBlocks = False
				addEndBlock(data)
				addVictoryFlag(data)
				data.numBlocks = 0

			if data.createBlocks == False:
				if data.player.inUpDownBlock == True:
					data.player.inUpLeft = True
				if data.firstVisibleCol + data.visibleCols >= len(data.grid[0]):
					data.firstVisibleCol = len(data.grid[0])-data.visibleCols
					data.scroll = False
				data.player.checkIfWon(data)

			data.backgrounds[0].needNewBackground(data)

			for background in data.backgrounds:
				if background.cx < (data.firstVisibleCol*data.cellWidth)-(data.width*3):
					data.backgrounds.remove(background)
					break

			for obj in data.flyingObjects:
				if obj.cx < -(data.width//2):
					data.flyingObjects.remove(obj)
					break

			if data.player.hasPowerUp != None:
				data.powerUpTime += 1
				if data.powerUpTime % 100 == 0 and data.player.hasPowerUp =="jumpPower":
					data.powerUpTime = 0
					data.player.reversePowerUp()
					data.player.hasPowerUp = None
				if data.powerUpTime % 50 == 0 and data.player.hasPowerUp =="shield":
					data.powerUpTime = 0
					data.player.reversePowerUp()
					data.player.hasPowerUp = None
			#UNCOMMENT THIS
			# if data.flyingObjects == []:
			# 	data.addObjTime += 1
			# 	if data.addObjTime % 50 == 0:
			# 		data.addObjTime = 0
			# 		createflyingObjects(data)

			data.player.checkForObstacle(data)
			#removes extrablocks
			if len(data.grid) >= 2*data.visibleRows:
				data.grid = data.grid[:len(data.grid)]
			if len(data.grid[0]) - data.firstVisibleCol <= data.visibleCols and data.player.inUpDownBlock == False and\
				data.createBlocks == True:
				data.player.inUpDownBlock = True
				popFirstBlock(data)
				addBlocktoGrid(data)
				data.player.lowerBound, data.player.upperBound = getVerticalScrollBounds(data)
			
			

def redrawAll1(canvas, data):
	if not data.gameOver:
		#background 
		for background in data.backgrounds:
			background.draw(canvas)
		# draw in canvas
		if not data.gameOver:
			drawGrid(data, data.grid, canvas)
			drawLevel(data,canvas)
			drawPowerUp(data, canvas)
			drawPlayer(data, data.player, canvas)
			for ghost in data.ghosts:
				ghost.draw(canvas,data.ghost)
			for obj in data.flyingObjects:
				obj.draw(canvas,data)
			if data.won:
				x0, y0 = data.width//4, data.height//4,
				canvas.create_rectangle(x0, y0, x0 + data.width//2, y0 + data.height//2, fill="light blue")
				canvas.create_text(data.width//2, data.height//3, text="You beat level" + str(data.level),\
					font="Arial 30")
				time = str(data.timeElapsed//10)
				canvas.create_text(data.width//2, data.height*(2/3), text="Time: "+time+" secs",\
					font="Arial 20")
	if data.gameOver:
		canvas.create_rectangle(0, 0, data.width,data.height, fill="light green")
		canvas.create_text(data.width//2, data.height//2, text="GAME OVER", font="Arial 50")
		canvas.create_text(data.width//2, data.height*(3/4), text="Press l to restart", font="Arial 25")


def redrawAll2(canvas, data):
	if not data.gameOver:
		for background in data.backgrounds:
			background.drawShift(canvas, data)
		# draw in canvas
	if not data.gameOver:
		drawGridShift(data, data.grid, canvas)
		drawLevelShift(data,canvas)
		drawPowerUpShift(data, canvas)
		drawPlayerShift(data, data.player, canvas)
		for ghost in data.ghosts:
			ghost.drawShift(canvas,data.ghost, data)
		for obj in data.flyingObjects:
			obj.drawShift(canvas, data)
		if data.won:
			x0, y0 = data.width//+data.shiftAmount, data.height//4,
			canvas.create_rectangle(x0, y0, x0 + data.width//2, y0 + data.height//2, fill="light blue")
			canvas.create_text(data.width//2, data.height//3, text="You beat level" + str(data.level),\
				font="Arial 30")
			time = str(data.timeElapsed//10)
			canvas.create_text(data.width//2+data.shiftAmount, data.height*(2/3), text="Time: "+time+" secs",\
				font="Arial 20")
	if data.gameOver:
		drawGameOverShift(data,canvas)


def keyPressed(event, data1, data2):
	keyPressedHelper(event, data1)
	keyPressedHelper2(event, data2)


def timerFired(data1, data2):
	timerFiredHelper(data1)
	timerFiredHelper(data2)


def redrawAll(canvas,data1, data2, data):
	if data1.won == True and data2.won == True:
		canvas.create_rectangle(0,0,data.width,data.height, fill="pink")
		if data1.timeElapsed > data2.timeElapsed:
			canvas.create_text(data1.width//2,data1.height//2 ,\
				text="You Won!")
			canvas.create_text(data.shiftAmount+data2.width//2, data2.height//2,\
				text="You Lost")
		if data1.timeElapsed < data2.timeElapsed:
			canvas.create_text(data1.width//2,data1.height//2 ,\
				text="You Lost")
			canvas.create_text(data.shiftAmount+data2.width//2, data2.height//2,\
				text="You Won!")		
	redrawAll1(canvas, data1)
	redrawAll2(canvas, data2)


#this is not my orginal code https://www.cs.cmu.edu/~112-n19/notes/notes-animations-part2.html
def run1(width, height):
	def redrawAllWrapper(canvas, data1, data2, data):
		canvas.delete(ALL)
		canvas.create_rectangle(0, 0, data.width, data.height,
								fill='white', width=0)
		redrawAll(canvas, data1, data2, data)
		canvas.update()

	def mousePressedWrapper(event, canvas, data):
		mousePressed(event, data)
		redrawAllWrapper(canvas, data1, data2, data)

	def keyPressedWrapper(event, canvas, data1, data2, data):
		keyPressed(event, data1, data2)
		redrawAllWrapper(canvas, data1, data2, data)

	def timerFiredWrapper(canvas, data1, data2, data):
		timerFired(data1, data2)
		redrawAllWrapper(canvas, data1, data2, data)
		# pause, then call timerFired again
		canvas.after(data.timerDelay, timerFiredWrapper, canvas, data1, data2, data)

	class Struct(object): pass
	data = Struct()
	data.winner = None
	data.width = width
	data.height = height
	data.timerDelay = 100 # milliseconds/10

	data1 = Struct()
	data1.width = width//2
	data1.height = height

	# data1.timerDelay = 100 # milliseconds/10
	data2 = Struct()
	data2.width = width//2
	data2.shiftAmount = width//2
	data2.height = height
	# data2.timerDelay = 100 # milliseconds/10
	root = Tk()
	init(data1)
	init(data2, data1.grid)

	# create the root and the canvas
	canvas = Canvas(root, width=data.width, height=data.height)
	canvas.configure(bd=0, highlightthickness=0)
	canvas.pack()
	# set up events
	root.bind("<Button-1>", lambda event:
							mousePressedWrapper(event, canvas, data))
	root.bind("<Key>", lambda event:
							keyPressedWrapper(event, canvas, data1, data2, data))
	timerFiredWrapper(canvas, data1, data2, data)
	# and launch the app
	root.mainloop()  # blocks until window is closed
	print("quitted")






run1(576*2, 432)
