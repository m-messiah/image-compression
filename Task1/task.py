#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import math
import operator
import Tkinter as Tk
from PIL import Image
from PIL import ImageTk
from tkFileDialog import askopenfilename, asksaveasfilename
import tkSimpleDialog
import tkMessageBox


# DEFINE GLOBAL VARIABLES
MAX_COLORS2 = float(255 * 255 * 3)


def pixels(image):
    """
    >>> len(pixels(Image.new("1", (10, 10))))
    300

    >>> len(pixels(Image.new("L", (20, 20))))
    1200

    >>> len(pixels(Image.new("RGB", (30, 30))))
    2700
    """
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
    """
    >>> psnr((Image.new("1", (10, 10)), Image.new("1", (10, 10))))

    >>> round(psnr((Image.new("1", (10, 10)), Image.new("1", (10, 10)).point(lambda i: 255))), 2)
    0.00
    """
    img1 = pixels(image[0])
    img2 = pixels(image[1])
    mse = float(reduce(operator.add,
                       map(lambda a, b: (a - b) ** 2, img1, img2)) * 3.0 / len(img1))
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
        if not imagePath:
            return
        try:
            image[i] = Image.open(imagePath)
        except IOError:
            sys.stderr.write("Image not found\n")
            sys.exit(1)
        photo[i] = ImageTk.PhotoImage(image[i])
        label[i] = Tk.Label(root, image=photo[i])
        label[i].image = photo[i]
        label[i].place(x=20 + i * (image[i].size[0] + 40), y=20,
                       width=image[i].size[0], height=image[i].size[1])

    openImage(imagePath, 0)
    openImage(imagePath, 1)

    def recalculatePSNR():
        psnR = psnr(image)
        if psnR or psnR == 0:
            PSNR.configure(text="%.2f" % psnR)
        else:
            PSNR.configure(text="Undef")

    def ConvertTo(colorSpace, matrix=None):
        if matrix:
            image[1] = image[0].convert(colorSpace, matrix)
        else:
            image[1] = image[0].convert(colorSpace)
        photo[1] = ImageTk.PhotoImage(image[1])
        label[1].configure(image=photo[1])
        label[1].image = photo[0]
        recalculatePSNR()

    def convertBIN():
        ConvertTo("1")

    def convertL():

        def stdgrayscale():
            ConvertTo("L")
            choosY.destroy()

        choosY = tkSimpleDialog.Tk()
        choosY.title("B/W weights")
        choosY.geometry("300x100+300+300")
        R = Tk.Label(choosY, text="Red * ")
        R.grid(row=1, column=1)
        RED2Y = Tk.Entry(choosY, justify=Tk.CENTER, width=5)
        RED2Y.grid(row=1, column=2)
        G = Tk.Label(choosY, text="Green * ")
        G.grid(row=1, column=3)
        GREEN2Y = Tk.Entry(choosY, justify=Tk.CENTER, width=5)
        GREEN2Y.grid(row=1, column=4)
        B = Tk.Label(choosY, text="Blue * ")
        B.grid(row=1, column=5)
        BLUE2Y = Tk.Entry(choosY, justify=Tk.CENTER, width=5)
        BLUE2Y.grid(row=1, column=6)

        def grayscale():
            try:
                redC = float(RED2Y.get())
                greenC = float(GREEN2Y.get())
                blueC = float(BLUE2Y.get())
            except ValueError:
                tkMessageBox.showerror("Error", "Bad input", parent=choosY)
            else:
                if redC + greenC + blueC > 1:
                    tkMessageBox.showinfo("Warning", "Coefficient sum is more than 1", parent=choosY)
                matrix = (redC, greenC, blueC, 0,
                          0, 0, 0, 0,
                          0, 0, 0, 0)
                ConvertTo("L", matrix)
                choosY.destroy()

        CONVERT = Tk.Button(choosY, text="Grayscale!", command=grayscale)
        CONVERT.grid(row=3, column=1, columnspan=4)
        blank = Tk.Label(choosY, text=" ")
        blank.grid(row=2, column=1, columnspan=6)
        STDCONVERT = Tk.Button(choosY, text="Std Grayscale", command=stdgrayscale)
        STDCONVERT.grid(row=3, column=5, columnspan=4)
        choosY.mainloop()

    def convertYUV():
        image[1] = image[0].copy()
        pix = image[1].load()
        width, height = image[1].size
        for x in range(width):
            for y in range(height):
                R, G, B = pix[x, y]
                Y = R * 0.299 + G * 0.587 + B * 0.114
                U = R * -0.169 + G * -0.332 + B * 0.500
                V = R * 0.500 + G * -0.419 + B * -0.0813
                pix[x, y] = int(Y), int(U), int(V)

        photo[1] = ImageTk.PhotoImage(image[1])
        label[1].configure(image=photo[1])
        label[1].image = photo[0]
        recalculatePSNR()

    def convertRGB():
        image[1] = image[0].copy()
        pix = image[1].load()
        width, height = image[1].size
        for x in range(width):
            for y in range(height):
                Y, U, V = pix[x, y]
                R = Y + 1.140 * V
                G = Y - 0.394 * U - 0.581 * V
                B = Y + 2.032 * U
                pix[x, y] = int(R), int(G), int(B)

        photo[1] = ImageTk.PhotoImage(image[1])
        label[1].configure(image=photo[1])
        label[1].image = photo[0]
        recalculatePSNR()

    def DCT():
        chooseSize = tkSimpleDialog.Tk()
        chooseSize.title("DCT window size")
        chooseSize.geometry("200x100+300+300")
        N = Tk.Label(chooseSize, text="N = ")
        N.grid(row=1, column=1)
        NValue = Tk.Entry(chooseSize, justify=Tk.CENTER, width=4)
        NValue.grid(row=1, column=3)

        def dct():
            print float(NValue.get())
            chooseSize.destroy()

        CONVERT = Tk.Button(chooseSize, text="DCT", command=dct)
        CONVERT.grid(row=2, column=2)
        chooseSize.mainloop()

    PSNR = Tk.Label(root, text="Undef")
    PSNR.place(x=300, y=300)

    CALCPSNR = Tk.Button(root, text="Recalculate PSNR", command=recalculatePSNR)
    CALCPSNR.place(x=150, y=290)

    def saveImage(img):
        filename = asksaveasfilename(filetypes=[("PNG Images", "*.png")])
        if filename:
            img.save(filename)

    def saveImageL():
        saveImage(image[0])

    def saveImageR():
        saveImage(image[1])

    def createMenu():
        """Create menu

        Left:
            Open
            Save
        Tools:
            Color Tools:
                RGB2BIN
                RGB2L
                RGB2YUV
                YUV2RGB
            DCT
        Right:
            Open
            Save

        """
        menu = Tk.Menu(root)
        fileMenuL = Tk.Menu(menu)
        menu.add_cascade(label="Left panel", menu=fileMenuL)
        fileMenuL.add_command(label="Open...", command=openFileL)
        fileMenuL.add_command(label="Save...", command=saveImageL)
        toolMenu = Tk.Menu(menu)
        menu.add_cascade(label="Tools", menu=toolMenu)
        colorTools = Tk.Menu(toolMenu)
        toolMenu.add_cascade(label="Color Tools", menu=colorTools)
        colorTools.add_command(label="Convert RGB to BIN (B/W)", command=convertBIN)
        colorTools.add_command(label="Convert RGB to Grayscale", command=convertL)
        colorTools.add_command(label="Convert RGB to YUV", command=convertYUV)
        colorTools.add_command(label="Convert YUV to RGB", command=convertRGB)
        toolMenu.add_command(label="DCT", command=DCT)
        fileMenuR = Tk.Menu(menu)
        menu.add_cascade(label="Right panel", menu=fileMenuR)
        fileMenuR.add_command(label="Open...", command=openFileR)
        fileMenuR.add_command(label="Save...", command=saveImageR)
        return menu

    menu = createMenu()
    root.config(menu=menu)
    root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        imagePath = "../Test_Images/image_House256rgb.png"
        main(imagePath)
    else:
        if sys.argv[1] == "test":
            import doctest

            doctest.testmod()
