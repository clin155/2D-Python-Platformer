#I got this code from https://www.daniweb.com/programming/software-development/threads/369823/resizing-image
#I got the grassBlock image from https://www.pinterest.com/pin/25051341650800513/
	#I got the player Image from https://minecraft.gamepedia.com/index.php?title=file:ladder.png&section=1
	#I got the Image from https://www.reddit.com/r/Minecraft/comments/4e4cdz/who_remembers_the_old_gravel_texture/
	#I got the Image fromhttp://pngimg.com/imgs/fantasy/ghost/
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