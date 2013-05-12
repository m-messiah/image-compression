#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import math
import operator
from Tkinter import *
from PIL import Image
from PIL import ImageTk
from tkFileDialog import askopenfilename, asksaveasfilename
import tkSimpleDialog
import tkMessageBox


# DEFINE GLOBAL VARIABLES
MAX_COLORS2 = float(255 * 255 * 3)


class Window(Tk):
    def __init__(self, title="Converter", imagePath=None):
        Tk.__init__(self)
        self.title(title)
        self.geometry("%dx%d+200+200" % (256 * 2 + 140, 256 + 80))
        self.image = [None, None]
        self.tempImage = None
        self.label = [None, None]
        self.photo = [None, None]
        self.createMenu()
        self.openImage(imagePath, 0)
        self.openImage(imagePath, 1)
        self.PSNR = Label(self, text="Undef")
        self.PSNR.place(x=300, y=300)
        self.CALCPSNR = Button(self, text="Recalculate PSNR",
                               command=self.recalculatePSNR)
        self.CALCPSNR.place(x=150, y=290)

    def createMenu(self):
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
        self.menu = Menu(self)
        self.fileMenuL = Menu(self.menu)
        self.menu.add_cascade(label="Left panel", menu=self.fileMenuL)
        self.fileMenuL.add_command(label="Open...",
                                   command=self.openFileL)
        self.fileMenuL.add_command(label="Save...",
                                   command=self.saveImageL)
        self.toolMenu = Menu(self.menu)
        self.menu.add_cascade(label="Tools", menu=self.toolMenu)
        self.colorTools = Menu(self.toolMenu)
        self.toolMenu.add_cascade(label="Color Tools", menu=self.colorTools)
        self.colorTools.add_command(label="Convert RGB to BIN (B/W)",
                                    command=self.convertBIN)
        self.colorTools.add_command(label="Convert RGB to Grayscale",
                                    command=self.convertL)
        self.colorTools.add_command(label="Convert RGB to YUV",
                                    command=self.convertYUV)
        self.colorTools.add_command(label="Convert YUV to RGB",
                                    command=self.convertRGB)
        self.toolMenu.add_command(label="DCT",
                                  command=self.DCT)
        self.toolMenu.add_command(label="JPEG", command=self.JPEG)
        self.fileMenuR = Menu(self.menu)
        self.menu.add_cascade(label="Right panel", menu=self.fileMenuR)
        self.fileMenuR.add_command(label="Open...",
                                   command=self.openFileR)
        self.fileMenuR.add_command(label="Save...",
                                   command=self.saveImageR)

        self.config(menu=self.menu)

    def openFile(self):
        filename = askopenfilename(filetypes=[("PNG Images", "*.png")])
        return filename

    def openFileL(self):
        self.openImage(self.openFile(), 0)

    def openFileR(self):
        self.openImage(self.openFile(), 1)

    def openImage(self, imagePath, i):
        if not imagePath:
            return
        try:
            self.image[i] = Image.open(imagePath)
        except IOError:
            sys.stderr.write("Image not found\n")
            sys.exit(1)
        self.photo[i] = ImageTk.PhotoImage(self.image[i])
        self.label[i] = Label(self, image=self.photo[i])
        self.label[i].image = self.photo[i]
        self.label[i].place(x=20 + i * (self.image[i].size[0] + 40),
                            y=20,
                            width=self.image[i].size[0],
                            height=self.image[i].size[1])

    def saveImage(self, side):
        filename = asksaveasfilename(filetypes=[("PNG Images", "*.png")])
        if filename:
            self.image[side].save(filename)

    def saveImageL(self):
        self.saveImage(0)

    def saveImageR(self):
        self.saveImage(1)

    def recalculatePSNR(self):
        psnR = self.psnr()
        if psnR or psnR == 0:
            self.PSNR.configure(text="%.2f" % psnR)
        else:
            self.PSNR.configure(text="Undef")

    def pixels(self, side):
        colorSpace = len(self.image[side].getbands())
        pixels = self.image[side].load()
        all_pixels = []
        for x in range(self.image[side].size[0]):
            for y in range(self.image[side].size[1]):
                coloredPixel = pixels[x, y]
                if colorSpace < 2:
                    for i in range(3):
                        all_pixels.append(coloredPixel)
                    continue
                for i in range(colorSpace):
                    all_pixels.append(coloredPixel[i])
        return all_pixels

    def psnr(self):
        img1 = self.pixels(0)
        img2 = self.pixels(1)
        mse = float(reduce(operator.add,
                           map(lambda a, b: (a - b) ** 2,
                               img1, img2)) * 3.0 / len(img1))
        if mse == 0.0:
            return None
        return 10.0 * math.log10(MAX_COLORS2 / mse)

    def ConvertTo(self, colorSpace, matrix=None):
        if matrix:
            self.image[1] = self.image[0].convert(colorSpace, matrix)
        else:
            self.image[1] = self.image[0].convert(colorSpace)
        self.photo[1] = ImageTk.PhotoImage(self.image[1])
        self.label[1].configure(image=self.photo[1])
        self.label[1].image = self.photo[0]
        self.recalculatePSNR()

    def convertBIN(self):
        self.ConvertTo("1")

    def convertL(self):
        self.choosY = tkSimpleDialog.Tk()

        def stdgrayscale():
            self.ConvertTo("L")
            self.choosY.destroy()

        self.choosY.title("B/W weights")
        self.choosY.geometry("300x100+300+300")
        self.R = Label(self.choosY, text="Red * ")
        self.R.grid(row=1, column=1)
        self.RED2Y = Entry(self.choosY, justify=CENTER, width=5)
        self.RED2Y.grid(row=1, column=2)
        self.G = Label(self.choosY, text="Green * ")
        self.G.grid(row=1, column=3)
        self.GREEN2Y = Entry(self.choosY, justify=CENTER, width=5)
        self.GREEN2Y.grid(row=1, column=4)
        self.B = Label(self.choosY, text="Blue * ")
        self.B.grid(row=1, column=5)
        self.BLUE2Y = Entry(self.choosY, justify=CENTER, width=5)
        self.BLUE2Y.grid(row=1, column=6)

        def grayscale():
            try:
                redC = float(self.RED2Y.get())
                greenC = float(self.GREEN2Y.get())
                blueC = float(self.BLUE2Y.get())
            except ValueError:
                tkMessageBox.showerror("Error",
                                       "Bad input", parent=self.choosY)
            else:
                if redC + greenC + blueC > 1:
                    tkMessageBox.showinfo("Warning",
                                          "Coefficient sum is more than 1",
                                          parent=self.choosY)
                matrix = (redC, greenC, blueC, 0,
                          0, 0, 0, 0,
                          0, 0, 0, 0)
                self.ConvertTo("L", matrix)
                self.choosY.destroy()

        self.CONVERT = Button(self.choosY, text="Grayscale!",
                              command=grayscale)
        self.CONVERT.grid(row=3, column=1, columnspan=4)
        self.blank = Label(self.choosY, text=" ")
        self.blank.grid(row=2, column=1, columnspan=6)
        self.STDCONVERT = Button(self.choosY, text="Std Grayscale",
                                 command=stdgrayscale)
        self.STDCONVERT.grid(row=3, column=5, columnspan=4)
        self.choosY.mainloop()

    def convertYUV(self):
        self.image[1] = self.image[0].copy()
        pix = self.image[1].load()
        width, height = self.image[1].size
        for x in range(width):
            for y in range(height):
                R, G, B = pix[x, y]
                Y = R * 0.299 + G * 0.587 + B * 0.114
                U = - R * 0.169 - G * 0.332 + B * 0.500 + 128
                V = R * 0.500 + - G * 0.419 + - B * 0.0813 + 128
                pix[x, y] = int(Y), int(U), int(V)

        self.photo[1] = ImageTk.PhotoImage(self.image[1])
        self.label[1].configure(image=self.photo[1])
        self.label[1].image = self.photo[0]
        self.recalculatePSNR()

    def convertRGB(self):
        self.image[1] = self.image[0].copy()
        pix = self.image[1].load()
        width, height = self.image[1].size
        for x in range(width):
            for y in range(height):
                Y, U, V = pix[x, y]
                R = Y + 1.140 * (V - 128)
                G = Y - 0.394 * (U - 128) - 0.581 * (V - 128)
                B = Y + 2.032 * (U - 128)
                pix[x, y] = int(R), int(G), int(B)

        self.photo[1] = ImageTk.PhotoImage(self.image[1])
        self.label[1].configure(image=self.photo[1])
        self.label[1].image = self.photo[0]
        self.recalculatePSNR()

    def DCT(self):
        self.chooseSize = tkSimpleDialog.Tk()
        self.chooseSize.title("DCT window size")
        self.chooseSize.geometry("200x100+300+300")
        self.N = Label(self.chooseSize, text="N = ")
        self.N.grid(row=1, column=1)
        self.NValue = Entry(self.chooseSize, justify=CENTER, width=4)
        self.NValue.grid(row=1, column=3)

        def dct():
            print float(self.NValue.get())
            self.chooseSize.destroy()

        self.CONVERT = Button(self.chooseSize, text="DCT", command=dct)
        self.CONVERT.grid(row=2, column=2)
        self.chooseSize.mainloop()

    def JPEG(self):
        def Matrix(N):
                return [[0 for i in range(N)] for j in range(N)]

        def NormColor(C):
            return 0 if C < 0 else 255 if C > 255 else C

        def convertJPG():
            def colorConvert():
                self.tempImage = self.image[0].copy().convert("RGB")
                pix = self.tempImage.load()
                width, height = self.tempImage.size
                for x in range(width):
                    for y in range(height):
                        try:
                            R, G, B = pix[x, y]
                        except TypeError:
                            R = pix[x, y]
                            G = B = R
                        Y = R * 0.299 + G * 0.587 + B * 0.114
                        Cb = - R * 0.169 - G * 0.332 + B * 0.500 + 128
                        Cr = R * 0.500 + - G * 0.419 + - B * 0.0813 + 128
                        pix[x, y] = int(Y), int(Cb), int(Cr)

            def colorDeConvert():
                pix = self.tempImage.load()
                width, height = self.tempImage.size
                for x in range(width):
                    for y in range(height):
                        Y, Cb, Cr = pix[x, y]
                        R = Y + 1.402 * (Cr - 128)
                        G = Y - 0.34414 * (Cb - 128) - 0.71414 * (Cr - 128)
                        B = Y + 1.772 * (Cb - 128)
                        R = NormColor(R)
                        G = NormColor(G)
                        B = NormColor(B)
                        pix[x, y] = int(R), int(G), int(B)

            def subsampling(type):
                sampledImage = self.tempImage.copy()
                if type == 0:
                    #None
                    pass
                elif type == 1:
                    #All
                    pix = sampledImage.load()
                    width, height = sampledImage.size
                    for x in range(0, width, 2):
                        for y in range(0, height, 2):
                            Cb, Cr = 0, 0
                            for i in range(2):
                                for j in range(2):
                                    Y, cb, cr = pix[x + i, y + j]
                                    Cb += cb
                                    Cr += cr
                            Cb /= 4
                            Cr /= 4
                            for i in range(2):
                                for j in range(2):
                                    pix[x + i,
                                        y + j] = (int(pix[x + i, y + j][0]),
                                                  int(Cb),
                                                  int(Cr))

                elif type == 2:
                    #Horiz
                    pix = sampledImage.load()
                    width, height = sampledImage.size
                    for x in range(0, width, 2):
                        for y in range(0, height):
                            Cb, Cr = 0, 0
                            for i in range(2):
                                Y, cb, cr = pix[x + i, y]
                                Cb += cb
                                Cr += cr
                            Cb /= 2
                            Cr /= 2
                            for i in range(2):
                                pix[x + i, y] = (int(pix[x + i, y][0]),
                                                 int(Cb),
                                                 int(Cr))

                elif type == 3:
                    #Vert
                    pix = sampledImage.load()
                    width, height = sampledImage.size
                    for x in range(width):
                        for y in range(0, height, 2):
                            Cb, Cr = 0, 0
                            for j in range(2):
                                Y, cb, cr = pix[x, y + j]
                                Cb += cb
                                Cr += cr
                            Cb /= 2
                            Cr /= 2
                            for j in range(2):
                                pix[x, y + j] = (int(pix[x, y + j][0]),
                                                 int(Cb),
                                                 int(Cr))

                self.tempImage = sampledImage

            def matrixMult(A, B, N):
                C = Matrix(N)
                for i in range(N):
                    for j in range(N):
                        C[i][j] = sum([A[i][x] * B[x][j] for x in range(N)])
                return C

            def dct(N=8, direction=0):
                DCTMatrix = Matrix(N)
                for j in range(N):
                    DCTMatrix[0][j] = 1.0 / math.sqrt(N)
                for i in range(1, N):
                    for j in range(N):
                        DCTMatrix[i][j] = math.sqrt(2.0 / N) * math.cos(
                            (2 * j + 1) * i * math.pi / 2 / N)
                DCTMatrixT = Matrix(N)
                for i in range(N):
                    for j in range(N):
                        DCTMatrixT[i][j] = DCTMatrix[j][i]
                if direction > 0:
                    DCTMatrix, DCTMatrixT = DCTMatrixT, DCTMatrix
                pix = self.tempImage.load()
                width, height = self.tempImage.size
                for x in range(0, width, N):
                    for y in range(0, height, N):
                        Y = Matrix(N)
                        Cb = Matrix(N)
                        Cr = Matrix(N)
                        for i in range(N):
                            for j in range(N):
                                try:
                                    Y[i][j], Cb[i][j], Cr[i][j] = pix[x + i,
                                                                      y + j]
                                except IndexError:
                                    (Y[i][j],
                                     Cb[i][j],
                                     Cr[i][j]) = (Y[i - 1][j - 1],
                                                  Cb[i - 1][j - 1],
                                                  Cr[i - 1][j - 1])
                        tempMatrix = matrixMult(Y, DCTMatrixT, N)
                        Y = matrixMult(DCTMatrix, tempMatrix, N)
                        for i in range(N):
                            for j in range(N):
                                try:
                                    pix[x + i, y + j] = (int(Y[i][j]),
                                                         int(Cb[i][j]),
                                                         int(Cr[i][j]))
                                except IndexError:
                                    pass

            def quantise(coef, N=8):
                Q = Matrix(N)
                for i in range(N):
                    for j in range(N):
                        Q[i][j] = int(1 + ((1 + i + j) * coef))

                pix = self.tempImage.load()
                width, height = self.tempImage.size
                for x in range(0, width, N):
                    for y in range(0, height, N):
                        for i in range(N):
                            for j in range(N):
                                try:
                                    pix[x + i,
                                        y + j] = (pix[x + i,
                                                      y + j][0] / Q[i][j],
                                                  pix[x + i, y + j][1],
                                                  pix[x + i, y + j][2])
                                except IndexError:
                                    pass

            def normalize():
                pix = self.tempImage.load()
                width, height = self.tempImage.size
                YMax = 0
                for x in range(width):
                    for y in range(height):
                        if pix[x, y][0] > YMax:
                            YMax = pix[x, y][0]
                coef = 255.0 / YMax
                for x in range(width):
                    for y in range(height):
                        pix[x, y] = (int(pix[x, y][0] * coef),
                                     pix[x, y][1],
                                     pix[x, y][2])

            colorConvert()
            subsampling(subsample.get())
            N = renderWindow.get()
            dct(N, direction=0)
            quantise(coefQuant.get(), N)
            dct(N, direction=1)
            normalize()
            colorDeConvert()
            self.image[1] = self.tempImage.copy()
            self.photo[1] = ImageTk.PhotoImage(self.image[1])
            self.label[1].configure(image=self.photo[1])
            self.label[1].image = self.photo[0]
            self.recalculatePSNR()
            #self.configJpeg.destroy()

        self.configJpeg = tkSimpleDialog.Tk()
        self.configJpeg.title("JPEG configure")
        self.configJpeg.geometry("300x400+200+200")
        self.SUBSAMPLING = Label(self.configJpeg, text="Subsampling Cb,Cr")
        self.SUBSAMPLING.pack()
        subsample = IntVar(self.configJpeg)
        self.R0 = Radiobutton(self.configJpeg, text="None",
                              variable=subsample, value=0)
        self.R0.pack(anchor=W)
        self.R1 = Radiobutton(self.configJpeg, text="ALL",
                              variable=subsample, value=1)
        self.R1.pack(anchor=W)
        self.R2 = Radiobutton(self.configJpeg, text="Horizontal",
                              variable=subsample, value=2)
        self.R2.pack(anchor=W)
        self.R3 = Radiobutton(self.configJpeg, text="Vertical",
                              variable=subsample, value=3)
        self.R3.pack(anchor=W)
        coefQuant = DoubleVar(self.configJpeg)
        self.CoQuant = Scale(self.configJpeg, label="Quantum coefficient",
                             variable=coefQuant, orient=HORIZONTAL, length=150,
                             from_=0, to=25)
        self.CoQuant.pack()
        renderWindow = IntVar(self.configJpeg)
        self.rWSize = Scale(self.configJpeg, label="Render window size",
                            variable=renderWindow, orient=HORIZONTAL,
                            length=150, from_=1, to=15)
        self.rWSize.pack()
        self.ButtonJPEG = Button(self.configJpeg, text="Convert!",
                                 command=convertJPG)
        self.ButtonJPEG.pack()
        self.configJpeg.mainloop()


def main():
    imagePath = "images/House_rgb.png"
    converter = Window(title="Converter", imagePath=imagePath)
    converter.mainloop()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        main()
    else:
        if sys.argv[1] == "test":
            import doctest

            doctest.testmod()
