

# Animation Starter Code, Focus on timerFired

from tkinter import *

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.a = [[True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True,
True, True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True, True, True, True,
True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True], [True, True,
True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False], [True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False], [True, True, True, True, True, False, True, True, True, True, False, True, True, True, True, False, True, True, False, True, False, True, True, False, True, True, True, True, True, True, False, False], [True, True, True, True, True, False, True, True, True, True, False, False, True, True, True, False, True, True, False, True, False, True, True, False, True, True, True, True, True, True, False, False], [True, True, True, True, True, False, False, True, True, True, False, False, True, False, True, False, False, True, False, True, False, True, True, False, True, True, True, True, True, True, False, False], [True, True, False, False, True, False, False, True, True, False, False, False, True, False, False, False, False, True, False, True, False, False, True, False, True, False, True, True, True, True, False, False], [False, True, False, False, True, False, False, False, True, False, False, False, True, False, False, False, False, False, False, True, False, False, True, False, True, False, True, True, True, True, False, False], [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, True, True, True, False, False, True, False, False, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, False], [False, False, False, False, False, False, True, False, True, True, True, False, False, True, False, True, False, True, False, False, False, False, True, False, False, True, False, False, False, True, False, False], [False, True, False, True, False, False, True, False, True, True, True, False, False, True, False, True, False, True, False,
False, True, False, True, True, False, True, False, False, True, True, False, False], [True, True, False, True, False, True, True, True, True, True, True, False, False, True, True, True, True, True, False, False, True, False, True, True, True, True, True, False, True, True, False, True], [True, True, False, True, True, True, True, True, True, True, True, False, False, True, True, True, True, True, True, False, True, False, True, True, True, True, True, False, True, True, False, True], [True, True, False, True, True, True, True, True, True, True, True, False, False, True, True, True, True, True, True, False, True, False, True, True, True, True, True, False, True, True, False, True], [True, True, False, True, True, True, True, True, True, True, True, False, False, True, True, True, True, True, True, False, True, False, True, True, True, True, True, False, True, True, False, True]]
    data.rows = 24
    data.cols = 32
    data.cellWidth = data.width // data.cols
    data.cellHeight = data.height // data.rows


def mousePressed(event, data):
    # use event.x and event.y
    data

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    # draw in canvas
    for i in range(data.rows):
        for j in range(data.cols):
            value = data.a[i][j]
            x0 = (j * data.cellWidth) + data.cellWidth//2
            y0 = (i * data.cellHeight) + data.cellHeight//2
            canvas.create_text(x0, y0, text=str(value), font="Arial 5")

####################################
# use the run function as-is
####################################

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
    print("bye!")

run(800, 600)