from non_original_work import *
from tkinter import *
from other import *
from procedural_generation import *
from classes import *
import copy


def drawGrid(data, grid, canvas):
    for i in range(data.rows):
    	for j in range(data.firstVisibleCol,data.visibleCols+data.firstVisibleCol):
            if grid[i][j] == True:
                j = j - data.firstVisibleCol
                cx = ((j * data.cellWidth) + data.cellWidth//2)
                cy = (i * data.cellHeight) + data.cellHeight//2
                canvas.create_image(cx, cy, image=data.grassBlock)

def init(data):
    #data stuff for procedural generation
    data.rows = 24
    data.visibleCols = 32
    data.emptyBlock = [[False]*data.visibleCols for i in range(data.rows)]
    data.grid = copy.deepcopy(data.emptyBlock)
    createStartBlock(data)
    for i in range(5):
        addBlocktoGrid(data)
    # data.previousCols = []
    # data.nextCols = []
    # data.nextBlocks = createNextBlocks(data)
    data.cellWidth = int(data.width / data.visibleCols)
    data.cellHeight = int(data.height /data.rows)
    #scroll data
    data.scrollMarginLeft = 30
    data.scrollMarginRight = data.width//2 + 60
    data.player = Player(data.cellWidth, data.cellHeight,data)
    data.playerImage = createPlayer(data,data.player.width, data.player.height)
    data.grassBlock = createGrassBlock(data, data.cellWidth, data.cellHeight)
    data.firstVisibleCol = 0
    data.gameOver = True

def mousePressed(event, data):
    # use event.x and event.y
    pass
def keyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym == "Right":
        data.player.moveHorizontal(1, data.grid, data)
    if event.keysym == "Left":
        data.player.moveHorizontal(-1, data.grid, data)
    if event.keysym == "space" and data.player.jumping == False and data.player.inDescent == False: 
        data.player.startJump()
    if event.keysym == "r":
        init(data)
    if len(data.grid[0]) - data.firstVisibleCol <= data.visibleCols: 
        popFirstBlock(data)
        addBlocktoGrid(data)
    #prevents phasing into a block if user spams right or left
    while data.player.checkForCollison(data.grid, data.firstVisibleCol):
        if event.keysym == "Right":
            data.player.col -= 1
        if event.keysym == "Left":
            data.player.col += 1
            

def timerFired(data):
    # print(data.player.faling, data.player.jumping)
    if data.player.falling:
        data.player.fall(data)
    if data.player.jumping:
        data.player.jump(data)
def redrawAll(canvas, data):
    # draw in canvas
    drawGrid(data, data.grid, canvas)
    x0, y0, x1,y1 = data.player.getBounds()
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
