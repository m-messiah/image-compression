#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import math
import operator
import Tkinter as Tk
from PIL import Image
from PIL import ImageTk


# DEFINE GLOBAL VARIABLES
MAX_COLORS2 = float(256 * 256 * 3)


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


def psnr(image1, image2):
    img1 = pixels(image1)
    img2 = pixels(image2)
    mse = float(math.sqrt(reduce(operator.add,
                                 map(lambda a, b: (a - b) ** 2, img1, img2)) / len(img1)))
    return 10.0 * math.log10(MAX_COLORS2 / mse)


def main(imagePath):
    try:
        image1 = Image.open(imagePath)
    except IOError:
        sys.stderr.write("Image not found\n")
        sys.exit(1)

    root = Tk.Tk()
    root.title("PSNR after B/W")
    root.geometry("%dx%d+200+200" % (image1.size[0] * 2 + 100, image1.size[1] + 80))

    photo1 = ImageTk.PhotoImage(image1)
    label1 = Tk.Label(root, image=photo1)
    label1.image = photo1
    label1.place(x=20, y=20, width=image1.size[0], height=image1.size[1])

    label2 = Tk.Label(root, image=photo1)
    label2.image = photo1
    label2.place(x=image1.size[0] + 60, y=20, width=image1.size[0], height=image1.size[1])

    def Convert():
        global photo2
        colorSpace = "L"
        image2 = image1.convert(colorSpace)
        photo2 = ImageTk.PhotoImage(image2)
        label2.configure(image=photo2)
        label2.image = photo1
        PSNR.configure(text="%.2f" % psnr(image1, image2))

    PSNR = Tk.Label(root, text="00.0")
    PSNR.place(x=300, y=image1.size[1] + 40)

    CONVERT = Tk.Button(root, text="Convert")
    CONVERT["command"] = Convert
    CONVERT.place(x=100, y=image1.size[1] + 40)

    root.mainloop()


if __name__ == "__main__":
    #if len(sys.argv) < 2:
    #    print "Usage: %s /path/to/image.png" % sys.argv[0]
    #    sys.exit(1)
    #imagepath = sys.argv[1]
    imagePath = "../Test_Images/image_House256rgb.png"
    main(imagePath)