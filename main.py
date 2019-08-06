from non_original_work import *
from tkinter import *
from other import *
from procedural_generation import *
from classes import *
import copy



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
            except IndexError:
                pass    

def init(data):
    #data stuff for procedural generation
    data.visibleCols = 32
    data.visibleRows = 24
    data.firstVisibleCol = 0
    data.firstVisibleRow = 0
    data.emptyBlock = [[False]*data.visibleCols for i in range(data.visibleRows)]
    data.grid = copy.deepcopy(data.emptyBlock)
    createStartBlock(data)
    #2
    for i in range(2):
        addBlocktoGrid(data, 0, True)
    # data.previousCols = []
    # data.nextCols = []
    # data.nextBlocks = createNextBlocks(data)
    data.cellWidth = int(data.width / data.visibleCols)
    data.cellHeight = int(data.height /data.visibleRows)
    #scroll data
    data.scrollMarginLeft = 30
    data.scrollMarginRight = data.width//2 + 60
    data.player = Player(data.cellWidth, data.cellHeight,data)
    #load Images
    data.playerImage = createPlayer(data,data.player.width, data.player.height)
    data.grassBlock = createGrassBlock(data, data.cellWidth, data.cellHeight)
    data.ladder = createLadder(data, data.cellWidth, data.cellHeight)
    data.gravel = createGravel(data, data.cellWidth, data.cellHeight)
    data.gameOver = False

 
def mousePressed(event, data):
    # use event.x and event.y
    pass
def keyPressed(event, data):
    # use event.char and event.keysym
    if not data.gameOver:
        if event.keysym == "Right" and not data.player.climbing:
            data.player.moveHorizontal(1, data.grid, data)
        if event.keysym == "Left" and not data.player.climbing:
            data.player.moveHorizontal(-1, data.grid, data)
        if event.keysym == "space":
            if data.player.jumping == False and data.player.inDescent == False: 
                data.player.startJump()
            if data.player.climbing:
                data.player.startJump()
        if event.keysym == "Up" and data.player.climbing:
            data.player.moveUpDownRow(data, -1)
        # if event.keysym == "Down":
        #     data.player.moveUpDownRow(data, 1)
        if event.keysym == "j":
            data.firstVisibleCol -= 1
        if event.keysym == "i":
            data.firstVisibleRow -= 1
        if event.keysym == "k":
            data.firstVisibleRow += 1
        if event.keysym == "l":
            data.firstVisibleCol += 1
        #prevents phasing into a block if user spams right or left
        while data.player.checkForCollison(data.grid, data.firstVisibleCol, data):
            if event.keysym == "Right":
                data.player.col -= 1
            if event.keysym == "Left":
                data.player.col += 1
    if event.keysym == "r":
        init(data)

def timerFired(data):
    if data.player.row >= data.firstVisibleRow + data.visibleRows-1:
        data.gameOver = True
    if not data.gameOver:
        if data.player.falling:
            data.player.fall(data)
        if data.player.jumping:
            data.player.jump(data)
        if data.player.inUpDownBlock == True:
            if data.firstVisibleRow < data.visibleRows:
                data.player.inUpDownBlock = False
    #removes extrablocks
    if len(data.grid) >= 2*data.visibleRows:
        data.grid = data.grid[:len(data.grid)]
    if len(data.grid[0]) - data.firstVisibleCol <= data.visibleCols and data.player.inUpDownBlock == False: 
                popFirstBlock(data)
                addBlocktoGrid(data)
                data.player.lowerBound, data.player.upperBound =getVerticalScrollBounds(data)

def redrawAll(canvas, data):
    # draw in canvas
    drawGrid(data, data.grid, canvas)
    x0, y0, x1,y1 = data.player.getBounds()
    y0 = y0 - (data.firstVisibleRow * data.cellHeight)
    y1 = y0 + data.player.height 
    cx = (x0 +x1) / 2
    cy = (y0+y1) / 2
    canvas.create_image(cx, cy, image=data.playerImage)


#this is not my orginal code
def run(width, height):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds/10
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("quitted")




run(768,576)
