import PIL.Image
import statistics
import numpy as np


def ImgToAscii(filename):
    drawChars = [
        '⠀', '░', '▒', '▓', '█',
    ]

    im = PIL.Image.open(filename)
    im = im.resize((256, 256))

    im = im.convert('LA')

    width, height = im.size
    passoX = float(width / 60)
    passoY = float(height / 30)
    if (((height // passoY) * (width // passoX)) > 4000):
        passoY += 1

    valorMax = 0
    valorMin = 255

    for i in np.arange(0, height, passoY):
        for j in np.arange(0, width, passoX):
            listColors = []
            for x in np.arange(0, passoX, 1):
                for y in np.arange(0, passoY, 1):
                    try:
                        black, a = im.getpixel((j + y, i + x))
                        listColors.append(black)
                    except Exception as e:
                        e
            valorMed = statistics.mean(listColors)
            valorMax = max(valorMed, valorMax)
            valorMin = min(valorMed, valorMin)

    ansFin = []
    ans = ''
    first = False
    for i in np.arange(0, height, passoY):
        line = ''
        for j in np.arange(0, width, passoX):
            listColorsLeft = []
            listColorsRight = []
            listColorsUp = []
            listColorsDown = []
            for y in np.arange(0, passoY // 2, 1):
                for x in np.arange(0, passoX, 1):
                    try:
                        black, a = im.getpixel((j + y, i + x))
                        listColorsLeft.append(black)
                    except Exception as e:
                        e
            for y in np.arange(passoY // 2, passoY, 1):
                for x in np.arange(0, passoX, 1):
                    try:
                        black, a = im.getpixel((j + y, i + x))
                        listColorsRight.append(black)
                    except Exception as e:
                        e
            for y in np.arange(0, passoY, 1):
                for x in np.arange(0, passoX // 2, 1):
                    try:
                        black, a = im.getpixel((j + y, i + x))
                        listColorsDown.append(black)
                    except Exception as e:
                        e
                for x in np.arange(passoX // 2, passoX, 1):
                    try:
                        black, a = im.getpixel((j + y, i + x))
                        listColorsUp.append(black)
                    except Exception as e:
                        e
            if (listColorsUp == []):
                listColorsUp = [0]
            if (listColorsDown == []):
                listColorsDown = [0]
            if (listColorsLeft == []):
                listColorsLeft = [0]
            if (listColorsRight == []):
                listColorsRight = [0]

            thresh = 88
            if (statistics.mean(listColorsLeft) - statistics.mean(listColorsRight) > thresh):
                line += '▌'
            elif (statistics.mean(listColorsLeft) - statistics.mean(listColorsRight) < -thresh):
                line += '▐'
            elif (statistics.mean(listColorsUp) - statistics.mean(listColorsDown) > thresh):
                line += '▄'
            elif (statistics.mean(listColorsUp) - statistics.mean(listColorsDown) < -thresh):
                line += '▀'
            else:
                valorMed = (statistics.mean(listColorsLeft) + statistics.mean(listColorsRight)) / 2
                count = -1
                while(valorMed > 0):
                    valorMed -= (valorMax - valorMin) / len(drawChars)
                    count += 1
                if (count >= len(drawChars)):
                    count = len(drawChars) - 1
                line += drawChars[count]
        if (len(ans) + len(line) > 1996 and first is False):
            ansFin.append(ans)
            ans = ''
            first = True
        ans += line + '\n'
    ansFin.append(ans)

    return ansFin


def ImgToAsciiCustom(filename):
    drawChars = [
        '⠀', '.', '*', '#',
        '░', '▒', '▓', '█',
    ]

    im = PIL.Image.open(filename)
    im = im.resize((256, 256))

    im = im.convert('LA')

    width, height = im.size
    passoX = float(width / 4)
    passoY = float(height / 4)
    if (((height // passoY) * (width // passoX)) > 4000):
        passoY += 1

    valorMax = 0
    valorMin = 255

    for i in np.arange(0, height, passoY):
        for j in np.arange(0, width, passoX):
            listColors = []
            for x in np.arange(0, passoX, 1):
                for y in np.arange(0, passoY, 1):
                    try:
                        black, a = im.getpixel((j + y, i + x))
                        listColors.append(black)
                    except Exception as e:
                        e
            if (listColors == []):
                listColors = [0]
            valorMed = statistics.mean(listColors)
            valorMax = max(valorMed, valorMax)
            valorMin = min(valorMed, valorMin)

    ansFin = []
    ans = ''
    first = False
    for i in np.arange(0, height, passoY):
        line = ''
        for j in np.arange(0, width, passoX):
            listColorsLeft = []
            listColorsRight = []
            listColorsUp = []
            listColorsDown = []
            for y in np.arange(0, passoY // 2, 1):
                for x in np.arange(0, passoX, 1):
                    try:
                        black, a = im.getpixel((j + y, i + x))
                        listColorsLeft.append(black)
                    except Exception as e:
                        e
            for y in np.arange(passoY // 2, passoY, 1):
                for x in np.arange(0, passoX, 1):
                    try:
                        black, a = im.getpixel((j + y, i + x))
                        listColorsRight.append(black)
                    except Exception as e:
                        e
            for y in np.arange(0, passoY, 1):
                for x in np.arange(0, passoX // 2, 1):
                    try:
                        black, a = im.getpixel((j + y, i + x))
                        listColorsDown.append(black)
                    except Exception as e:
                        e
                for x in np.arange(passoX // 2, passoX, 1):
                    try:
                        black, a = im.getpixel((j + y, i + x))
                        listColorsUp.append(black)
                    except Exception as e:
                        e
            if (listColorsUp == []):
                listColorsUp = [0]
            if (listColorsDown == []):
                listColorsDown = [0]
            if (listColorsLeft == []):
                listColorsLeft = [0]
            if (listColorsRight == []):
                listColorsRight = [0]

            thresh = 88
            if (statistics.mean(listColorsLeft) - statistics.mean(listColorsRight) > thresh):
                line += '▌'
            elif (statistics.mean(listColorsLeft) - statistics.mean(listColorsRight) < -thresh):
                line += '▐'
            elif (statistics.mean(listColorsUp) - statistics.mean(listColorsDown) > thresh):
                line += '▄'
            elif (statistics.mean(listColorsUp) - statistics.mean(listColorsDown) < -thresh):
                line += '▀'
            else:
                valorMed = (statistics.mean(listColorsLeft) + statistics.mean(listColorsRight)) / 2
                count = -1
                while(valorMed > 0):
                    valorMed -= (valorMax - valorMin) / len(drawChars)
                    count += 1
                if (count >= len(drawChars)):
                    count = len(drawChars) - 1
                line += drawChars[count]
        if (len(ans) + len(line) > 1994 and first is False):
            ansFin.append(ans)
            ans = ''
            first = True
        ans += line + '\n'
    ansFin.append(ans)

    return ansFin
