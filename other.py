from procedural_generation import *
import copy


def popFirstBlock(data):
	newGrid = []
	for row in data.grid:
		newGrid.append(row[data.visibleCols:])
	data.grid = copy.deepcopy(newGrid)
	data.firstVisibleCol -= data.visibleCols
def addBlocktoGrid(data, blockType = None, start=False):
	#0 is right 1 is up 2 is down 3 is left
	if blockType == None:
		blockType = 1
		# blockType = random.randint(0,1)
	if start == False:
		if blockType == 1 or blockType == 2: 
			print("AddedUp")
			data.player.inUpDownBlock = True
			# data.player.col = data.visibleCols//2
			# data.player.row = len(data.grid) - data.visibleRows//2

		else:
			data.player.inUpDownBlock = False
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
			data.grid[row][col+data.firstVisibleCol] = block[row][col]
	data.player.row += len(block)
	data.player.resetY0()
	data.firstVisibleRow += len(block)
	data.player.jumping = False


def addceilingLadder(data, block):
	print("cock")
	for row in range(0, len(block)//2):
		for col in range(len(block[0])-6, len(block[0])):
			try:
				data.grid[row][col+data.firstVisibleCol] = False
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
		row += 1
		for col in range(len(data.grid[0])-data.visibleCols, len(data.grid[0])):
			if data.grid[row][col] == "gravel":
				checking = False
	upperBound = row
	row = data.firstVisibleRow - 1
	checking = True
	while checking:
		row -= 1
		if data.grid[row][len(data.grid[0])-10] == "gravel":
			checking = False
	lowerBound = row
	return lowerBound, upperBound