import random
import copy
def createLeftRightBlock(data):
	grid = copy.deepcopy(data.emptyGrid)
	numRows = len(grid)
	numCols = len(grid[0])
	#create top terrain
	baseTerrain = 2
	for i in range(baseTerrain):
		for col in range(numCols):
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
	for base in range((baseTerrain-1), -1, -1):
		row = numRows -1 - base
		for col in range(len(grid[0])):
			if grid[numRows-1-baseTerrain][col] == True:
				grid[row][col] = True

	return grid

def legalLeftRightBlock(data):
	block = None 
	while block == None or not isLegal(block, data):
		block = createLeftRightBlock(data)
	return block
def isLegal(block, data):
	for row in range(data.rows//2, data.rows):
		for col in range(data.cols):
			if col != 0:
				if checkForImpossibleJumps(block, data, row, col) != True:
					print('Bad')
					return False

	if isLegalHoles(block, data) and hasHoles(block, data):
		return True
	print('Also bad')
	return False

def hasHoles(block, data):
	for col in range(data.cols):
		if block[data.rows-1][col] == False:
			return True

def checkForImpossibleJumps(block, data, row, col):
	if block[row][col] != True:
		return True
	if block[data.rows-1][col] != True:
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
	for col in range(data.cols):
		if block[data.rows-1][col] == True and inHole == False:
			continue
		elif inHole == False:
			startPt = getSurfaceBlock(block, data, col-1)
			inHole = True
		elif block[data.rows-1][col] == True and inHole == True:
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
	for row in range(data.rows//2, data.rows):
		if block[row][col] == True:
			return (row, col)

# # def createUpBlock()

# # def createDownBlock()