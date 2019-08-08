#I got this code from https://www.daniweb.com/programming/software-development/threads/369823/resizing-image
#I got the grassBlock image from https://www.pinterest.com/pin/25051341650800513/
	#I got the player Image from https://minecraft.gamepedia.com/index.php?title=file:ladder.png&section=1
	#I got the Image from https://www.reddit.com/r/Minecraft/comments/4e4cdz/who_remembers_the_old_gravel_texture/
	#I got the Image fromhttp://pngimg.com/imgs/fantasy/ghost/
	#I got the enemy image from https://opengameart.org/content/zombie-and-skeleton-32x48
	#i got background from https://www.brusheezy.com/textures/43311-blue-sky-texture
from tkinter import *
from PIL import Image
import tkinter as tk
from PIL import ImageTk

def createImage(data, width,height, img):
	grassBlock = Image.open(img)
	grassBlock = grassBlock.resize((width,height), Image.ANTIALIAS)
	return ImageTk.PhotoImage(grassBlock)

#I got this code from https://www.mbeckler.org/blog/?p=120
def divide_round_up(n, d):
    return int((n + (d - 1))/d)


# got this code form https://stackoverflow.com/questions/17140886/how-to-search-and-replace-text-in-a-file
import fileinput

def replaceText(search, replacement, filename):
	with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
	    for line in file:
	        print(line.replace(search, replacement))