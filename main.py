from non_original_work import *
from tkinter import *
from other import *
from procedural_generation import *
from classes import *
import copy

def createNextBlocks(data):
    listt = []
    for i in range(2):
        listt.append(legalLeftRightBlock(data))
    return listt

def drawGrid(data, num, grid, canvas):
    for i in range(len(grid)):
    	for j in range(len(grid[0])):
            cx = ((j * data.cellWidth) + data.cellWidth//2) + (data.width*num) - data.scrollX
            cy = (i * data.cellHeight) + data.cellHeight//2
            if grid[i][j] == True:
                canvas.create_image(cx, cy, image=data.grassBlock)
def init(data):
    #data stuff for procedural generation
    data.rows = 24
    data.cols = 32
    data.emptyGrid = [[False]*data.cols for i in range(data.rows)]
    data.grid = copy.deepcopy(data.emptyGrid)
    createStartGrid(data)
    data.previousCols = []
    data.nextCols = []
    data.nextBlocks = createNextBlocks(data)
    data.cellWidth = int(data.width / data.cols)
    data.cellHeight = int(data.height /data.rows)
    #scroll data
    data.scrollMarginLeft = 30
    data.scrollMarginRight = data.width//2 + 60
    data.scrollX = 0
    data.player = Player(data.cellWidth, data.cellHeight*2, data.cellHeight, data.rows, data)
    data.playerImage = createPlayer(data,data.player.width, data.player.height)
    data.grassBlock = createGrassBlock(data, data.cellWidth, data.cellHeight)
    data.falling = True

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym == "Right":
        data.player.moveHorizontal(10, data.cellHeight, data.cellWidth, data.grid, data)

    if event.keysym == "Left":
        data.player.moveHorizontal(-10, data.cellHeight, data.cellWidth, data.grid, data)
    if event.keysym == "Up":    
        data.player.jump(10, data)
        data.falling = False


def timerFired(data):
    # if data.falling:
    #     data.player.falling(data)
    pass
def redrawAll(canvas, data):
    # draw in canvas
    drawGrid(data, 0, data.grid, canvas)
    drawGrid(data, 1, data.nextBlocks[0], canvas)
    cx = (data.player.x0 + data.player.x1) / 2
    cy = (data.player.y0 + data.player.y1) / 2
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
