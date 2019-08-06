from non_original_work import *
from tkinter import *
from other import *
from procedural_generation import *
from classes import *
from enemies import *
import copy



def init(data):
    #data stuff for procedural generation
    data.visibleCols = 32
    data.visibleRows = 24
    data.firstVisibleCol = 0
    data.firstVisibleRow = 0
    data.emptyBlock = [[False]*data.visibleCols for i in range(data.visibleRows)]
    data.grid = copy.deepcopy(data.emptyBlock)
    createStartBlock(data)
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
    data.playerImage = createImage(data,data.player.width, data.player.height, "player.png")
    data.grassBlock = createImage(data, data.cellWidth, data.cellHeight, "grassBlock.png")
    data.gravel = createImage(data, data.cellWidth, data.cellHeight, "gravel.jpg")
    data.ladder = createImage(data, data.cellWidth, data.cellHeight, "ladder.png")
    data.ghost = createImage(data, int(data.cellWidth*1.5), int(data.cellHeight*1.5), "ghost.png")
    data.jumpPower = createImage(data, data.cellWidth, data.cellHeight, "jumpPower.png")
    data.gameOver = False
    data.ghosts = []
    data.numGhosts = 3
    createNewGhosts(data)
    data.timeElapsed = 0
    data.level = 0
    data.powerUpTime = 0

 
def mousePressed(event, data):
    # use event.x and event.y
    pass
def keyPressed(event, data):
    # use event.char and event.keysym
    if not data.gameOver:
        if event.keysym == "Right" and not data.player.climbing:
            if data.player.moveHorizontal(1, data.grid, data):
                moveEnemies(-2, 0,data)
        if event.keysym == "Left" and not data.player.climbing:
            if data.player.moveHorizontal(-1, data.grid, data):
                moveEnemies(2,0,data)
        if event.keysym == "space":
            if data.player.jumping == False and data.player.inDescent == False: 
                data.player.startJump()
            if data.player.climbing:
                data.player.startJump()
        if event.keysym == "Up" and data.player.climbing:
            data.player.moveUpDownRow(data, -1)
            moveEnemies(0,1,data)
        if event.keysym == "Down":
            data.player.moveUpDownRow(data, 1)
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
    data.timeElapsed += 1
    if data.player.row >= data.firstVisibleRow + data.visibleRows-1: data.gameOver = True
    try:
        if data.player.checkForGravel(data): data.gameOver = True
    except IndexError:
        data.gameOver = True
    if not data.gameOver:
        if data.player.isOnLand(data) and not data.player.jumping: data.player.falling = True
        if data.player.falling:
            data.player.fall(data)
        if data.player.jumping:
            data.player.jump(data)
        if data.player.inUpDownBlock == True:
            if data.firstVisibleRow <= data.visibleRows and not data.player.climbing and data.player.isOnLand(data):
                data.player.lowerBound = getVerticalScrollBounds(data)
                data.player.inUpDownBlock = False
            elif data.firstVisibleRow <= data.visibleRows*2 and not data.player.climbing and data.player.isOnLand(data):
                data.player.lowerBound = getVerticalScrollBounds(data)

        if data.player.inUpLeft == True:
            if data.player.row < data.visibleRows -4:
                data.player.inUpLeft = False
                data.player.inUpDownBlock = False

        #enemies
        for ghost in data.ghosts:
            ghost.move(data.player, data)
        removeGhosts(data)
        # #spawns the enemies ##################
        # if data.timeElapsed % 50 == 0 and len(data.ghosts) == 0:
        #     createNewGhosts(data)
        # ##################
        if data.player.hasPowerUp != None:
            data.powerUpTime += 1
            if data.powerUpTime % 100 == 0:
                data.powerUpTime = 0
                data.player.reversePowerUp()
                data.player.hasPowerUp = None 
        #removes extrablocks
        if len(data.grid) >= 2*data.visibleRows:
            data.grid = data.grid[:len(data.grid)]
        if len(data.grid[0]) - data.firstVisibleCol <= data.visibleCols and data.player.inUpDownBlock == False:
            data.player.inUpDownBlock = True
            popFirstBlock(data)
            addBlocktoGrid(data)
            data.player.lowerBound = getVerticalScrollBounds(data)
        

def redrawAll(canvas, data):
    # draw in canvas
    if not data.gameOver:
        drawGrid(data, data.grid, canvas)
        drawPowerUp(data, canvas)
        drawPlayer(data, data.player, canvas)
        for ghost in data.ghosts:
            ghost.draw(canvas,data.ghost)

    else:
        drawGameOver(data,canvas)


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