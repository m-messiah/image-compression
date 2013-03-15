#!/usr/bin/python
import os
import sys
import Tkinter
from PIL import Image


def button_exit():
    sys.exit(1)

root = Tkinter.Tk()
root.bind("<Button>", button_exit)
root.geometry('+%d+%d' % (400, 400))
try:
    image = Image.open("../Test_Images/image_House256rgb.png")
    tkpi = Tkinter.PhotoImage(image)
    label_image = Tkinter.Label(root, image=tkpi)
    label_image.place(x=0, y=0, width=image.size[0], height=image.size[1])
    root.title("Test")
    root.mainloop()
except Exception as e:
    pass