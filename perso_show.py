
## test module for displaying nice characters
## on the screen

from PIL import Image
im = Image.open("8x8perso.gif")

print(im.mode)

# reading pixels
topx = 36
topy = 36

sizex = 8
sizey = 8

spacex = 4
spacey = 4

res = 6

s = ""
def readPixelsLed(tilex, tiley):
    global s
    s = ""
    def f(color):
        global s
        (r,g,b) = pixelRgb(color)
        s = s + (chr(g) + chr(r) + chr(b))


    readPixelsLedFn(tilex, tiley, f)
    return s

def readPixelsPrint(tilex, tiley):

    def f(color):
        print(str.format("{:02}",color), end=" ")

    readPixelsLedFn(tilex, tiley, f)

#
# Pixels are sent by columns, in reverse order
# y is not inverted 
#

def readPixelsLedFn(tilex, tiley, f):
    global topx,topy,sizex,sizey,spacex,spacey,res
    for i in range(sizex,0,-1):
        for j in range(0,sizey):
            x = topx + ((sizex + spacex) * tilex + i) * res + res/2
            y = topy + ((sizey + spacey) * tiley + j) * res + res/2
            f(im.getpixel((x,y)))

lum = 30
def pixelRgb(color):
    global lum
    p = im.getpalette()
    r = int(p[color * 3] / lum)
    g = int(p[color * 3 + 1] /lum)
    b = int(p[color * 3 + 2] /lum)
    return (r,g,b)

if __name__ == "__main__":

    readPixelsPrint(0,0)
    r = readPixelsLed(0,0)

    print()
    print(pixelRgb(5))

