from non_original_work import *
from tkinter import *
from other import *
from procedural_generation import *
from classes import *

def createNextBlocks(data):
    listt = []
    for i in range(2):
        listt.append(legalLeftRightBlock(data))
    return listt

def init(data):
    # load data.xyz as appropriate
    data.rows = 24
    data.cols = 32
    data.emptyGrid = [[False]*data.cols for i in range(data.rows)]
    data.grid = legalLeftRightBlock(data)
    data.previousCols = []
    data.nextCols = []
    data.nextBlocks = createNextBlocks(data)
    data.cellWidth = data.width // data.cols
    data.cellHeight = data.height // data.rows
    data.player = Player(data.cellWidth, data.cellHeight*2, data.cellHeight, data.cols)
    data.playerImage = createPlayer(data,data.player.width, data.player.height)
    data.grassBlock = createGrassBlock(data)

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym == "Right":
        moveGridRight(data)
    if event.keysym == "Left":
        moveGridLeft(data)
def timerFired(data):
    pass

def redrawAll(canvas, data):
    # draw in canvas
    for i in range(len(data.grid)):
    	for j in range(len(data.grid[0])):
            x0 = j * data.cellWidth
            x1 = x0 + data.cellWidth
            y0 = i * data.cellHeight
            y1 = y0 + data.cellHeight
            if data.grid[i][j] == True:
                canvas.create_image(x0, y0, image=data.grassBlock)
    canvas.create_image(data.player.x0, data.player.y0, image=data.playerImage)

#this is not my orginal code
def run(width=300, height=300):
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
    data.timerDelay = 100 # milliseconds
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




run(800,600)
