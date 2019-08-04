#I got this code from https://www.daniweb.com/programming/software-development/threads/369823/resizing-image
from PIL import Image
import tkinter as tk
from PIL import ImageTk
def createGrassBlock(data):
	grassBlock = Image.open("grassBlock.png")
	grassBlock = grassBlock.resize((data.cellWidth, data.cellHeight), Image.ANTIALIAS)
	return ImageTk.PhotoImage(grassBlock)

def createPlayer(data,width,height):
	grassBlock = Image.open("player.png")
	grassBlock = grassBlock.resize((width, height), Image.ANTIALIAS)
	return ImageTk.PhotoImage(grassBlock)

