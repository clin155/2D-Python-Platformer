from procedural_generation import *
import copy


def popFirstBlock(data):
	if len(data.grid[0]) <= data.visibleCols: return None
	newGrid = []
	for row in data.grid:
		newGrid.append(row[data.visibleCols:])
	data.grid = copy.deepcopy(newGrid)
	data.firstVisibleCol -= data.visibleCols
def addBlocktoGrid(data, blockType = None, start=False):
	#0 is right 1 is up
	if blockType == None:
		#blockType = 1
		blockType = random.randint(0,1)
		# blockType = 0
	if start == False:
		if blockType == 1: 
			print("AddedUp")
			data.player.inUpDownBlock = True
			data.firstVisibleCol = len(data.grid[0])-data.visibleCols
			data.player.falling = True
			# data.player.maxJump = data.player.baseMaxJump
		if blockType == 0:
			# data.player.maxJump = data.player.baseMaxJump+1

			if data.player.inUpDownBlock == True:
				data.player.inUpLeft = True
			else:
				data.player.inUpLeft = False


	returnBlock(blockType, data)

def shiftGridDown(data, blockLen, emptyRow):
	for i in range(blockLen):
		data.grid = [copy.copy(emptyRow)] + copy.deepcopy(data.grid[:])

def createStartBlock(data):
	numRows = data.visibleRows
	numCols = data.visibleCols
	baseTerrain = 2
	for col in range(numCols):
		data.grid[0][col] = "gravel"
		data.grid[1][col] = True
		data.grid[numRows-1][col] = "gravel"
		data.grid[numRows-baseTerrain][col] = True


def createEmptyRow(leng):
	listt = []
	for i in range(leng):
		listt.append(False)
	return listt


def addUpBlock(data, block, typee):
	if typee == "Upleft":
		addceilingLadder(data, block)
	emptyRow = createEmptyRow(len(data.grid[0]))
	shiftGridDown(data, len(block), emptyRow)
	for row in range(len(block)):
		for col in range(len(block[0])):
			data.grid[row][len(data.grid[0])-data.visibleCols + col] = block[row][col]
	data.player.row += len(block)
	data.firstVisibleRow += len(block)
	data.player.jumping = False


def addceilingLadder(data, block):
	for row in range(0, len(block)//2):
		col = 3
		data.grid[row][len(data.grid[row]) - col] = False

	for row in range(0, len(block)):
			data.grid[row][len(data.grid[0])-1] = True
			if data.grid[row][len(data.grid[0])-3] == False:
				data.grid[row][len(data.grid[0])-3] = "ladder"

def returnBlock(blockType, data):
	if blockType == 0:
		block = createLeftRightBlock(data)
		for row in range(len(block)):
			data.grid[row] += block[row]
		data.numBlocks += 1

	elif blockType == 1:
		block = createUpLeftBlock(data)
		addUpBlock(data,block, "Upleft")
		data.numBlocks += 1
		block = createUpRightBlock(data)
		addUpBlock(data,block, "UpRight")
		data.numBlocks += 1




def getVerticalScrollBounds(data):
	row = data.firstVisibleRow
	checking = True
	while checking:
		row -= 1
		row = max(row, 0)
		for col in range(len(data.grid[row])-data.visibleCols, len(data.grid[row])):	
			if row == data.firstVisibleRow -1 :continue		
			if data.grid[row][col] == "gravel":
				
				checking = False	
	lowerBound = row
	checking = True
	row = data.firstVisibleRow
	while checking:
		row += 1
		for col in range(len(data.grid[row])-data.visibleCols, len(data.grid[row])):
			try:	
				if data.grid[row][col] == "gravel":
					checking = False	
			except IndexError:
				print(IndexError)
	upperBound = row
	return lowerBound, upperBound


def drawGameOver(data,canvas):
	canvas.create_rectangle(0, 0, data.width,data.height, fill="light green")
	canvas.create_text(data.width//2, data.height//2, text="GAME OVER", font="Arial 75")
	canvas.create_text(data.width//2, data.height*(3/4), text="Press r to restart", font="Arial 50")

def drawGameOverShift(data,canvas):
	canvas.create_rectangle(data.shiftAmount, 0, data.width+data.shiftAmount,data.height, fill="light green")
	canvas.create_text(data.width//2+data.shiftAmount, data.height//2, text="GAME OVER", font="Arial 50")
	canvas.create_text(data.width//2+data.shiftAmount, data.height*(3/4), text="Press r to restart", font="Arial 25")

def drawImage(img, data, i, j, canvas):
	j = j - data.firstVisibleCol
	i = i - data.firstVisibleRow
	cx = ((j * data.cellWidth) + data.cellWidth//2)
	cy = (i * data.cellHeight) + data.cellHeight//2
	canvas.create_image(cx, cy, image=img)

def drawImageShift(img, data, i, j, canvas):
	j = j - data.firstVisibleCol
	i = i - data.firstVisibleRow
	cx = ((j * data.cellWidth) + data.cellWidth//2) + data.shiftAmount
	cy = (i * data.cellHeight) + data.cellHeight//2
	canvas.create_image(cx, cy, image=img)


def drawGrid(data, grid, canvas):
	for i in range(data.firstVisibleRow,data.visibleRows+data.firstVisibleRow):
		for j in range(data.firstVisibleCol,data.visibleCols+data.firstVisibleCol):
			if i < 0 or j < 0: continue
			elif i >= len(grid) or j >= len(grid[0]): continue
			try:
				if grid[i][j] == True:
					drawImage(data.block, data, i, j, canvas)
				elif grid[i][j] == "ladder":
					drawImage(data.ladder, data, i, j, canvas)
				elif grid[i][j] == "gravel":
					drawImage(data.gravel, data, i, j, canvas)
				elif grid[i][j] == "jumpPower":
					drawImage(data.jumpPower, data, i, j, canvas)
				elif grid[i][j] == "obstacle":
					drawImage(data.obstacle, data, i, j, canvas)
				elif grid[i][j] == "flag":
					drawImage(data.flag, data, i, j, canvas)
				elif grid[i][j] == "shield":
					drawImage(data.shield, data, i, j, canvas)
			except IndexError:
				pass    

def drawGridShift(data, grid, canvas):
	for i in range(data.firstVisibleRow,data.visibleRows+data.firstVisibleRow):
		for j in range(data.firstVisibleCol,data.visibleCols+data.firstVisibleCol):
			if i < 0 or j < 0: continue
			elif i >= len(grid) or j >= len(grid[0]): continue
			try:
				if grid[i][j] == True:
					drawImageShift(data.block, data, i, j, canvas)
				elif grid[i][j] == "ladder":
					drawImageShift(data.ladder, data, i, j, canvas)
				elif grid[i][j] == "gravel":
					drawImageShift(data.gravel, data, i, j, canvas)
				elif grid[i][j] == "jumpPower":
					drawImageShift(data.jumpPower, data, i, j, canvas)
				elif grid[i][j] == "obstacle":
					drawImageShift(data.obstacle, data, i, j, canvas)
				elif grid[i][j] == "flag":
					drawImageShift(data.flag, data, i, j, canvas)
				elif grid[i][j] == "shield":
					drawImageShift(data.shield, data, i, j, canvas)
			except IndexError:
				pass  

def drawPlayer(data, player, canvas):
	x0, y0, x1, y1 = player.canvasGetBounds(data)
	cx = (x0 +x1) / 2
	cy = (y0+y1) / 2
	canvas.create_image(cx, cy, image=data.playerImage)
	if player.invincible == True: canvas.create_oval(x0, y0, x1, y1, width=1)

def drawPlayerShift(data, player, canvas):
	x0, y0, x1, y1 = player.canvasGetBounds(data)
	x0 += data.shiftAmount
	x1 += data.shiftAmount
	cx = (x0 +x1) / 2 
	cy = (y0+y1) / 2
	canvas.create_image(cx, cy, image=data.playerImage)
	if player.invincible == True: canvas.create_oval(x0, y0, x1, y1, width=1)

#FIX THIS
def drawPowerUp(data, canvas):
	if data.player.hasPowerUp == "jump":
		canvas.create_image(data.cellWidth//2, data.cellHeight//2, image=data.jumpPower)

	if data.player.hasPowerUp == "shield":
		canvas.create_image(data.cellWidth//2, data.cellHeight//2, image=data.shield)
def drawPowerUpShift(data, canvas):
	if data.player.hasPowerUp == "jump":
		canvas.create_image(data.cellWidth//2+data.shiftAmount, data.cellHeight//2, image=data.jumpPower)

	if data.player.hasPowerUp == "shield":
		canvas.create_image(data.cellWidth//2+data.shiftAmount, data.cellHeight//2, image=data.shield)


def getSurfaceBlockGroundEnemies(block, data, col):
	for row in range(data.visibleRows//2,data.visibleRows):
		if block[row][col] == True:
			return (row, col)
	return (data.visibleRows//2, col)

def setLevelValues(data):
	data.numGhosts += data.level
	data.maxNumObstacles += data.level*2
	data.gameLength += (data.level*5)
	data.numFlyingObjects += data.level
	data.objSpd += (data.level*3)

	if data.level == 0:
		data.backgroundImage = "background.png"
		data.backgrounds.append(Background(data.backgroundImage, data, data.width//2, data.height//2, data.width))
		data.block = createImage(data, data.cellWidth, data.cellHeight, "grassBlock.png")
		data.flyingObjectImage = createImage(data, int(data.cellWidth*1.5), int(data.cellHeight*1.5), "fireball.png")
	if data.level == 1:
		data.backgroundImage = "caveBackground.jpg"
		data.backgrounds.append(Background(data.backgroundImage, data, data.width, data.height//2, data.width*2))
		data.block = createImage(data, data.cellWidth, data.cellHeight, "rockBlock.png")
		data.flyingObjectImage = createImage(data, int(data.cellWidth*1.5), int(data.cellHeight*1.5), "boulder.png")
	if data.level == 2:
		data.backgroundImage = "lake.png"
		data.backgrounds.append(Background(data.backgroundImage, data, data.width, data.height//2, data.width*2))
		data.block = createImage(data, data.cellWidth, data.cellHeight, "ice.png")
		data.flyingObjectImage = createImage(data, int(data.cellWidth*1.5), int(data.cellHeight*1.5), "waterBall.png")
	if data.level == 3:	
		data.backgroundImage = "nightTime.png"
		data.backgrounds.append(Background(data.backgroundImage, data, data.width, data.height//2, data.width*2))
		data.block = createImage(data, data.cellWidth, data.cellHeight, "rockBlock.png")
		data.flyingObjectImage =  createImage(data, int(data.cellWidth*1.5), int(data.cellHeight*1.5), "boulder.png")
	if data.level == 4:	
		data.backgroundImage = "mountains.png"
		data.backgrounds.append(Background(data.backgroundImage, data, data.width, data.height//2, data.width*2))
		data.block = createImage(data, data.cellWidth, data.cellHeight, "rockBlock.png")
		data.flyingObjectImage = createImage(data, int(data.cellWidth*1.5), int(data.cellHeight*1.5), "fireball.png")

	if data.level > 4:
		data.backgroundImage = "background.png"
		data.backgrounds.append(Background(data.backgroundImage, data, data.width//2, data.height//2, data.width))
		data.block = createImage(data, data.cellWidth, data.cellHeight, "grassBlock.png")
		data.flyingObjectImage = createImage(data, int(data.cellWidth*1.5), int(data.cellHeight*1.5), "fireball.png")


def setLevelValuesM(data):
	data.numGhosts += data.level
	data.maxNumObstacles += data.level*2
	data.gameLength += (data.level*5)
	data.numFlyingObjects += data.level
	data.objSpd += (data.level*3)

	if data.level == 0:
		data.backgroundImage = "background.png"
		data.block = createImage(data, data.cellWidth, data.cellHeight, "grassBlock.png")
		data.flyingObjectImage = createImage(data, int(data.cellWidth*1.5), int(data.cellHeight*1.5), "fireball.png")
	if data.level == 1:
		data.backgroundImage = "caveBackground.jpg"
		data.block = createImage(data, data.cellWidth, data.cellHeight, "rockBlock.png")
		data.flyingObjectImage = createImage(data, int(data.cellWidth*1.5), int(data.cellHeight*1.5), "boulder.png")
	if data.level == 2:
		data.backgroundImage = "lake.png"
		data.block = createImage(data, data.cellWidth, data.cellHeight, "ice.png")
		data.flyingObjectImage = createImage(data, int(data.cellWidth*1.5), int(data.cellHeight*1.5), "waterBall.png")
	if data.level == 3:	
		data.backgroundImage = "nightTime.png"
		data.block = createImage(data, data.cellWidth, data.cellHeight, "rockBlock.png")
		data.flyingObjectImage =  createImage(data, int(data.cellWidth*1.5), int(data.cellHeight*1.5), "boulder.png")

	if data.level == 4:	
		data.backgroundImage = "mountains.png"
		data.block = createImage(data, data.cellWidth, data.cellHeight, "rockBlock.png")
		data.flyingObjectImage = createImage(data, int(data.cellWidth*1.5), int(data.cellHeight*1.5), "fireball.png")
	if data.level > 4:
		data.backgroundImage = "background.png"
		data.block = createImage(data, data.cellWidth, data.cellHeight, "grassBlock.png")
		data.flyingObjectImage = createImage(data, int(data.cellWidth*1.5), int(data.cellHeight*1.5), "fireball.png")
	data.backgrounds.append(Background(data.backgroundImage, data, data.width//2, data.height//2, data.width))

def addEndBlock(data):
	block = copy.deepcopy(data.emptyBlock)
	numRows = data.visibleRows
	numCols = data.visibleCols
	baseTerrain = 2
	for col in range(numCols):
		block[0][col] = "gravel"
		block[1][col] = True
		block[numRows-1][col] = "gravel"
		block[numRows-baseTerrain][col] = True
	for row in range(len(block)):
		data.grid[row] += block[row]

def addVictoryFlag(data):
	for row in range(len(data.grid)):
		try:
			data.grid[row][-1] = True
		except IndexError:
			pass
	for row in range(data.player.row-4, data.player.row+15):
		if data.player.inUpDownBlock == True: break
		try:
			if data.grid[row][-4] == True:
				data.grid[row-1][-4] = "flag"
				return None
			if row == data.player.row + 14:
				data.grid[row-2][-4] = "flag"
				data.grid[row-1][-4] = True
				return None
		except IndexError:
			continue
	for row in range(data.visibleRows//2, data.visibleRows):
		if data.grid[row][-4] == True:
			data.grid[row-1][-4] = "flag"
			break
		if row == data.visibleRows-1:
			data.grid[row-2][-4] = "flag"
			data.grid[row-1][-4] = True
			break

def drawLevel(data, canvas):
	canvas.create_rectangle(data.width-(data.cellWidth*2), 0, data.width, data.cellHeight*2, fill="light blue")
	canvas.create_text(data.width-data.cellWidth, data.cellHeight, text=str(data.level+1))

def drawLevelShift(data, canvas):
	canvas.create_rectangle(data.width-(data.cellWidth*2)+data.shiftAmount, 0, data.width+data.shiftAmount,\
		data.cellHeight*2, fill="light blue")
	canvas.create_text(data.width-data.cellWidth+data.shiftAmount, data.cellHeight, text=str(data.level+1))