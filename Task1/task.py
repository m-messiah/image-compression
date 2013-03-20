#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import math
import operator
import Tkinter as Tk
from PIL import Image
from PIL import ImageTk
from tkFileDialog import askopenfilename, asksaveasfilename


# DEFINE GLOBAL VARIABLES
MAX_COLORS2 = float(255 * 255 * 3)


def pixels(image):
    colorSpace = len(image.getbands())
    pixels = image.load()
    all_pixels = []
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            coloredPixel = pixels[x, y]
            if colorSpace < 2:
                for i in range(3):
                    all_pixels.append(coloredPixel)
                continue
            for i in range(colorSpace):
                all_pixels.append(coloredPixel[i])
    return all_pixels


def psnr(image):
    img1 = pixels(image[0])
    img2 = pixels(image[1])
    mse = float(math.sqrt(reduce(operator.add,
                                 map(lambda a, b: (a - b) ** 2, img1, img2)) / len(img1)))
    if mse == 0.0:
        return None
    return 10.0 * math.log10(MAX_COLORS2 / mse)


def main(imagePath):
    root = Tk.Tk()
    root.title("Comparator")
    root.geometry("%dx%d+200+200" % (256 * 2 + 140, 256 + 80))
    image, photo, label = [None, None], [None, None], [None, None]

    def openFile():
        filename = askopenfilename(filetypes=[("PNG Images", "*.png")])
        return filename

    def openFileL():
        openImage(openFile(), 0)

    def openFileR():
        openImage(openFile(), 1)

    def openImage(imagePath, i):
        try:
            image[i] = Image.open(imagePath)
        except IOError:
            sys.stderr.write("Image not found\n")
            sys.exit(1)
        #global photo
        photo[i] = ImageTk.PhotoImage(image[i])
        #global label
        label[i] = Tk.Label(root, image=photo[i])
        label[i].image = photo[i]
        label[i].place(x=20 + i * (image[i].size[0] + 40), y=20,
                       width=image[i].size[0], height=image[i].size[1])

    openImage(imagePath, 0)
    openImage(imagePath, 1)

    def recalculatePSNR():
        psnR = psnr(image)
        if psnR:
            PSNR.configure(text="%.2f" % psnR)
        else:
            PSNR.configure(text="Undef")

    def ConvertTo(colorSpace):
        image[1] = image[0].convert(colorSpace)
        photo[1] = ImageTk.PhotoImage(image[1])
        label[1].configure(image=photo[1])
        label[1].image = photo[0]
        recalculatePSNR()

    def convertBIN():
        ConvertTo("1")

    def convertL():
        ConvertTo("L")

    PSNR = Tk.Label(root, text="00.0")
    PSNR.place(x=300, y=300)

    CALCPSNR = Tk.Button(root, text="Recalculate PSNR", command=recalculatePSNR)
    CALCPSNR.place(x=150, y=290)

    def saveImage(img):
        filename = asksaveasfilename(filetypes=[("PNG Images", "*.png")])
        img.save(filename)

    def saveImageL():
        saveImage(image[0])

    def saveImageR():
        saveImage(image[1])

    def createMenu():
        """Create menu"""
        menu = Tk.Menu(root)
        fileMenuL = Tk.Menu(menu)
        menu.add_cascade(label="Left panel", menu=fileMenuL)
        fileMenuL.add_command(label="Open...", command=openFileL)
        fileMenuL.add_command(label="Save...", command=saveImageL)
        toolMenu = Tk.Menu(menu)
        menu.add_cascade(label="Tools", menu=toolMenu)
        toolMenu.add_command(label="Convert to BIN (B/W)", command=convertBIN)
        toolMenu.add_command(label="Convert to Grayscale", command=convertL)
        fileMenuR = Tk.Menu(menu)
        menu.add_cascade(label="Right panel", menu=fileMenuR)
        fileMenuR.add_command(label="Open...", command=openFileR)
        fileMenuR.add_command(label="Save...", command=saveImageR)
        return menu

    menu = createMenu()
    root.config(menu=menu)
    root.mainloop()


if __name__ == "__main__":
    imagePath = "../Test_Images/image_House256rgb.png"
    main(imagePath)