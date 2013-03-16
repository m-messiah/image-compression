#!/usr/bin/python
import sys
from Tkinter import *
from PIL import Image


def button_exit():
    sys.exit(1)


root = Tk()
root.title("Test")
canv = Canvas(root,
              width=800, height=500,
              bg="lightgray")
canv.pack()
try:
    image = Image.open("../Test_Images/image_House256rgb.png")
    tkpi = PhotoImage(image)
    label_image = Label(root, image=tkpi)
    label_image.place(x=0, y=0, width=image.size[0], height=image.size[1])
except Exception as e:
    pass
finally:
    root.mainloop()