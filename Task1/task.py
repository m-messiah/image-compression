#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import math
import operator
import Tkinter as Tk
from PIL import Image
from PIL import ImageTk


def pixels(image):
    pixels = image.load()
    width, height = image.size
    all_pixels = []
    for x in range(width):
        for y in range(height):
            cpixel = pixels[x, y]
            all_pixels.append(cpixel)
    return all_pixels


def psnr(image1, image2):
    img1 = pixels(image1)
    img2 = pixels(image2)
    mse = math.sqrt(reduce(operator.add,
                           map(lambda a, b: (a[1] - b) ** 2, img1, img2)) / len(img1))
    log10 = math.log10
    return 10.0 * log10(float(256 * 256) / float(mse))


def main(imagePath):
    try:
        image1 = Image.open(imagePath)
    except IOError:
        sys.stderr.write("Image not found\n")
        sys.exit(1)

    root = Tk.Tk()
    root.title("Test")
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
        image2 = image1.convert("L")
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