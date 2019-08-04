from procedural_generation import *
import copy

def moveGridRight(data):
    colFromGrid, newGrid = shiftGridLeft(data, data.grid)
    data.previousCols.append(colFromGrid)   
    data.grid = copy.deepcopy(newGrid)
    colFrom1, newBlock1 = shiftGridLeft(data, data.nextBlocks[0])
    colFrom2, newBlock2 = shiftGridLeft(data, data.nextBlocks[1])
    data.nextBlocks[0] = copy.deepcopy(newBlock1)
    data.nextBlocks[1] = copy.deepcopy(newBlock2)
    if data.nextCols != []:
        col3 = data.nextCols.pop(0)
        addtoEndOfBlock(data.nextBlocks[1, col3], data)
    addtoEndOfBlock(data.nextBlocks[0], colFrom2, data)
    for row in range(data.rows):
        data.grid[row][data.cols-1] = colFrom1[row]
    if checkIfBlockNeeded(data):
        data.nextBlocks[1] = legalLeftRightBlock(data)

def addtoEndOfBlock(block, cols,data):
    for col in range(data.cols):
        #look for a col of all zeros
        if block[0][col] == 0:
            for row in range(data.rows):
                block[row][col] = cols[row]

def checkIfBlockNeeded(data):
    for col in range(len(data.nextBlocks[1][0])):
        if data.nextBlocks[1][0][col] != 0:
            return False
    return True
def shiftGridLeft(data, block):
    col = []
    newGrid = []
    for row in range(data.rows):
        col.append(block[row][0])
        newGrid.append(block[row][1:]+[0])
    return col, newGrid

def shiftGridRight(data, block):
    col = []
    newGrid = []
    for row in range(data.rows):
        if type(block[row][len(block[0])-1]) == bool:
            col.append(block[row][len(block[0])-1])
        newGrid.append([0]+block[row][:-1])
    return col, newGrid

def moveGridLeft(data):
    if len(data.previousCols) == data.cols or len(data.previousCols) == 0:
        return None
    colFromPrev = data.previousCols.pop(0)
    colFromGrid, newDataGrid = shiftGridRight(data, data.grid)
    colFromBlock1, newNextBlock1 = shiftGridRight(data, data.nextBlocks[0])
    colFromBlock2, newNextBlock2 = shiftGridRight(data, data.nextBlocks[1])
    data.nextBlocks[0] = copy.deepcopy(newNextBlock1)
    data.nextBlocks[1] = copy.deepcopy(newNextBlock2)
    data.grid = copy.deepcopy(newDataGrid)
    #inserts col into front of data.nextBlock
    addtoStartOfBlock(data, colFromPrev, data.grid)
    addtoStartOfBlock(data, colFromGrid, data.nextBlocks[0])
    addtoStartOfBlock(data, colFromBlock1, data.nextBlocks[1])
    if checkifNotEmptyCol(colFromBlock2):
        data.nextCols.append(colFromBlock2)


def addtoStartOfBlock(data, col, block):
    for row in range(data.rows):
        block[row][0] = col[row] 
def checkifNotEmptyCol(col):
    for value in col:
        if value != 0:
            return True
    return False