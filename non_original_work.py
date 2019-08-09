#I got the grassBlock image from https://www.pinterest.com/pin/25051341650800513/
	#I got the player Image from https://minecraft.gamepedia.com/index.php?title=file:ladder.png&section=1
	#I got the Image from https://www.reddit.com/r/Minecraft/comments/4e4cdz/who_remembers_the_old_gravel_texture/
	#I got the Image fromhttp://pngimg.com/imgs/fantasy/ghost/
	#I got the enemy image from https://opengameart.org/content/zombie-and-skeleton-32x48
	#i got backgrounds from https://www.brusheezy.com/textures/43311-blue-sky-texture, https://raventale.itch.io/parallax-background
	#https://assetstore.unity.com/packages/tools/sprite-management/2d-cave-parallax-background-149247, 
	#https://opengameart.org/sites/default/files/1_37.png, https://free-game-assets.itch.io/free-horizontal-game-backgrounds?download


	#i got the stone block image from http://i.imgur.com/lZIjk.png
	#i got the glass image from http://greyminecraftcoder.blogspot.com/2014/12/transparent-blocks-18.html

	# i got the shield from https://www.vectorunit.com/blog-posts/2019/5/21/bbr2-powerup-guide-defense-1
	# i got the boulder from https://ya-webdesign.com/explore/cartoon-boulder-png/

	#i got the fireball from https://www.kisspng.com/png-drawing-clip-art-fireball-733888/download-png.html
	#i got the ice texture from https://www.curseforge.com/minecraft/mc-mods/ice-mod
	#i got the waterBall texture from https://pixabay.com/illustrations/water-ball-deco-blue-mirroring-2438719/
	
from tkinter import *
from PIL import Image
import tkinter as tk
from PIL import ImageTk
#I got this code from https://www.daniweb.com/programming/software-development/threads/369823/resizing-image
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