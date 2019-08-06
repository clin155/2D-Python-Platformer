
    
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
		# blockType = 1
		blockType = random.randint(0,1)
	if start == False:
		if blockType == 1: 
			print("AddedUp")
			data.player.inUpDownBlock = True
			data.firstVisibleCol = len(data.grid[0])-data.visibleCols
			data.player.falling = True
			# data.player.col = data.visibleCols//2
			# data.player.row = len(data.grid) - data.visibleRows//2
		if blockType == 0:
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


def getStartCell(data, col):
	for row in range(data.firstVisibleRow + data.visibleRows//2,\
		data.firstVisibleRow+data.visibleRows):
		if data.grid[row][col] == True:
			return (row, col)
	return(12, 12)

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
	data.player.resetY0()
	data.firstVisibleRow += len(block)
	data.player.jumping = False


def addceilingLadder(data, block):
	for row in range(0, len(block)//2):
		for col in range(len(block[0])-6, len(block[0])):
			try:
				data.grid[row][len(data.grid[0])-data.visibleCols + col] = False
			except:
				pass

	for row in range(0, len(block)):
			data.grid[row][len(data.grid[0])-1] = True
			if data.grid[row][len(data.grid[0])-4] == False:
				data.grid[row][len(data.grid[0])-4] = "ladder"

def returnBlock(blockType, data):
	if blockType == 0:
		block = createLeftRightBlock(data)
		for row in range(len(block)):
			data.grid[row] += block[row]
	elif blockType == 1:
		block = createUpLeftBlock(data)
		addUpBlock(data,block, "Upleft")
		print("done!")
		block = createUpRightBlock(data)
		addUpBlock(data,block, "UpRight")
		print("done!")



def getVerticalScrollBounds(data):
	row = data.firstVisibleRow
	checking = True
	while checking:
		row -= 1
		for col in range(len(data.grid[0])-data.visibleCols, len(data.grid[0])):	
			if row == data.firstVisibleRow -1 :continue		
			if data.grid[row][col] == "gravel":
				checking = False	
	lowerBound = row
	return lowerBound


def drawGameOver(data,canvas):
    canvas.create_rectangle(0, 0, data.width,data.height, fill="light green")
    canvas.create_text(data.width//2, data.height//2, text="GAME OVER", font="Arial 75")
    canvas.create_text(data.width//2, data.height*(3/4), text="Press r to restart", font="Arial 50")

def drawImage(img, data, i, j, canvas):
    j = j - data.firstVisibleCol
    i = i - data.firstVisibleRow
    cx = ((j * data.cellWidth) + data.cellWidth//2)
    cy = (i * data.cellHeight) + data.cellHeight//2
    canvas.create_image(cx, cy, image=img)

def drawGrid(data, grid, canvas):
    for i in range(data.firstVisibleRow,data.visibleRows+data.firstVisibleRow):
        for j in range(data.firstVisibleCol,data.visibleCols+data.firstVisibleCol):
            if i < 0 or j < 0: continue
            elif i >= len(grid) or j >= len(grid[0]): continue
            try:
                if grid[i][j] == True:
                    drawImage(data.grassBlock, data, i, j, canvas)
                elif grid[i][j] == "ladder":
                    drawImage(data.ladder, data, i, j, canvas)
                elif grid[i][j] == "gravel":
                    drawImage(data.gravel, data, i, j, canvas)
               	elif grid[i][j] == "jumpPower":
               		drawImage(data.jumpPower, data, i, j, canvas)
            except IndexError:
                pass    


def drawPlayer(data, player, canvas):
    x0, y0, x1, y1 = player.canvasGetBounds(data)
    cx = (x0 +x1) / 2
    cy = (y0+y1) / 2
    canvas.create_image(cx, cy, image=data.playerImage)

def drawPowerUp(data, canvas):
	if data.player.hasPowerUp == "jump":
		canvas.create_image(data.cellWidth//2, data.cellHeight//2, image=data.jumpPower)


