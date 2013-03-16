#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Tkinter as Tk
from PIL import Image
from ImageTk import PhotoImage


class Images(Tk.Frame):
    def __init__(self, master, image1):
        Tk.Frame.__init__(self, master)
        self.pack()
        self.label1 = Tk.Label(self)
        image1 = Image.open("../Test_Images/image_House256rgb.png")
        self.label1["image"] = PhotoImage(image1)
        self.label1.place(x=20, y=20, width=image1.size[0], height=image1.size[1])
        self.label1.pack({'side': 'left'})
        #self.CONVERT = Tk.Button(self)
        #self.CONVERT["text"] = "Convert"
        #self.CONVERT["command"] = self.Convert(image1)
        #self.CONVERT.pack({"side": "bottom"})

    def Convert(self, image1):
        image2 = image1.convert("L")
        self.label2 = Tk.Label(self, image=PhotoImage(image2))
        self.label2.place(x=image1.size[0] + 60, y=20, width=image2.size[0], height=image2.size[1])
        self.label2.pack({"side": "right"})


def main(imagePath):
    try:
        image1 = Image.open(imagePath)
    except IOError:
        sys.stderr.write("Image not found\n")
        sys.exit(1)

    root = Tk.Tk()
    root.title("Test")
    root.geometry("%dx%d+200+200" % (image1.size[0] * 2 + 100, image1.size[1] + 80))
    images = Images(master=root, image1=image1)
    images.mainloop()


if __name__ == "__main__":
    #if len(sys.argv) < 2:
    #    print "Usage: %s /path/to/image.png" % sys.argv[0]
    #    sys.exit(1)
    #imagepath = sys.argv[1]
    imagePath = "../Test_Images/image_House256rgb.png"
    main(imagePath)