import random
import copy
def createBlock(data):
	grid = copy.deepcopy(data.emptyBlock)
	numRows = data.visibleRows
	numCols = data.visibleCols
	#create top terrain
	baseTerrain = 2
	for i in range(baseTerrain):
		for col in range(numCols):
			if i == 0: 
				grid[i][col] = "gravel"
			else:
				grid[i][col] = True
	for col in range(numCols):
		length = random.randint(0,8)
		for i in range(length+1):
			grid[i+baseTerrain][col] = True
	for col in range(numCols):
		if col == 0 or col == numCols-1:
			length = 2
		else:
			length = random.randint(0,5)
		for i in range(numRows-1, numRows-(length+1), -1):
			i = i - baseTerrain
			grid[i][col] = True
	#creates base terrain for the bottom
	for col in range(numCols):
		if grid[numRows-1-baseTerrain][col] == True:
			grid[numRows-1][col] = "gravel"
			grid[numRows-2][col] = True

	return grid

def legalBlock(data):
	block = None 
	while block == None or not isLegal(block, data):
		block = createBlock(data)
	print("Legal!")
	return block
def isLegal(block, data):
	for row in range(data.visibleRows//2, data.visibleRows):
		for col in range(data.visibleCols):
			if col != 0:
				if checkForImpossibleJumps(block, data, row, col) != True:
					return False

	if isLegalHoles(block, data) and hasHoles(block, data):
		return True
	return False

def hasHoles(block, data):
	for col in range(data.visibleCols):
		if block[data.visibleRows-1][col] == False:
			return True

def checkForImpossibleJumps(block, data, row, col):
	if block[row][col] != True:
		return True
	if block[data.visibleRows-1][col] != True:
		return True
	if checkJump(block, data, row, col, 5, 1):
		return True
	return False

def checkJump(block, data, row, col, parm,dCol):
	if parm == 0:
		return False
	for i in range(row-parm, row+parm):
		try:
			if block[i][col-1] == True:
				return True
		except IndexError:
			return True
	return checkJump(block, data, row, col, parm-1,dCol+1)
 

def getListofHoles(block, data):
	inHole = False
	listOFHoles = []
	startPt = None
	for col in range(data.visibleCols):
		if block[data.visibleRows-1][col] == True and inHole == False:
			continue
		elif inHole == False:
			startPt = getSurfaceBlock(block, data, col-1)
			inHole = True
		elif block[data.visibleRows-1][col] == True and inHole == True:
			endPt = getSurfaceBlock(block, data, col)
			listOFHoles.append([startPt, endPt])
			inHole = False
	return listOFHoles

def isLegalHoles(block,data):
	holeList = getListofHoles(block, data)
	for listt in holeList:
		hDifference = listt[1][0] - listt[0][0]
		if hDifference <= 0: continue
		holeLength = (listt[1][1] - listt[0][1]) - 1
		if holeLength > 4:
			return False
		if 4 - holeLength < hDifference:
			return False
	return True
		
def getSurfaceBlock(block, data, col):
	for row in range(data.visibleRows//2,data.visibleRows):
		if block[row][col] == True:
			return (row, col)

def createStartBlock(data):
	numRows = data.visibleRows
	numCols = data.visibleCols
	baseTerrain = 2
	for i in range(baseTerrain):
		for col in range(numCols):
			data.grid[i][col] = True
	for base in range((baseTerrain-1), -1, -1):
		row = numRows -1 - base
		for col in range(numCols):
			data.grid[row][col] = True


def createLeftRightBlock(data):
	return legalBlock(data)

def createUpLeftBlock(data):
	block = legalBlock(data)
	for row in range(data.visibleRows//2+4,data.visibleRows):
		for col in range(data.visibleCols-6, data.visibleCols-1):
			block[row][col] = False
			if col == data.visibleCols-4:
				block[row][col] = "ladder"
	for row in range(0, data.visibleRows//2):
		for col in range(1, 6):
			block[row][col] = False
	for row in range(len(block)):
		block[row][0] = True
		block[row][data.visibleCols-1] = True
		if block[row][3] == False:
				block[row][3] = "ladder"
	return block

def createUpRightBlock(data):
	block = legalBlock(data)
	for row in range(data.visibleRows//2+4,data.visibleRows):
		for col in range(1, 6):
			block[row][col] = False
			if col == 3:
				block[row][col] = "ladder"
	for row in range(len(block)):
		block[row][0] = True
	return block





# # def createDownBlock()