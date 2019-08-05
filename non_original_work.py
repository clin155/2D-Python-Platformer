#I got this code from https://www.daniweb.com/programming/software-development/threads/369823/resizing-image
from PIL import Image
import tkinter as tk
from PIL import ImageTk
def createGrassBlock(data, width,height):
	#I got the grassBlock image from https://www.pinterest.com/pin/25051341650800513/
	grassBlock = Image.open("grassBlock.png")
	grassBlock = grassBlock.resize((width,height), Image.ANTIALIAS)
	return ImageTk.PhotoImage(grassBlock)
def createPlayer(data,width,height):
	#I got the player Image from http://8bitmmo.net/presskit/character%20art/
	grassBlock = Image.open("player.png")
	grassBlock = grassBlock.resize((width, height), Image.ANTIALIAS)
	return ImageTk.PhotoImage(grassBlock)

#I got this code from https://www.mbeckler.org/blog/?p=120
def divide_round_up(n, d):
    return int((n + (d - 1))/d)