import math

from PIL import Image
import numpy as np
from pathlib import Path
import os
import asyncio
import concurrent.futures
from pokemontcgsdk import RestClient

RestClient.configure('12345678-1234-1234-1234-123456789ABC')


class BACard:
    def __init__(self, a):
        self.card_id = Path(a).stem
        self.card_pixels = np.asarray(Image.open(a))

    def geturl(self):
        return 'full cards' + self.card_id + '.png'

    def compare(self, i):
        pixels = []
        for y in range(2):
            for x in range(2):
                temp_avg = 0
                for rgb in range(3):
                    if rgb == 0: mod = 0.3
                    if rgb == 1: mod = 0.59
                    if rgb == 2: mod = 0.11
                    temp_avg += math.pow((int(self.card_pixels[y][x][rgb]) - int(i[y][x][rgb]))*mod, 2)
                pixels.append(temp_avg)
        return pixels[0] + pixels[1] + pixels[2] + pixels[3]
        #return math.sqrt(math.pow(pixels[0], 2) + math.pow(pixels[1], 2) + math.pow(pixels[2], 2) + math.pow(pixels[3], 2))


class Frame:
    def __init__(self, a):
        self.full_frame = a

    def getarray(self, x, y):
        assert x * 2 <= len(self.full_frame[1]) and x >= 0
        assert y * 2 <= len(self.full_frame) and y >= 0
        return self.full_frame[y * 2:y * 2 + 2, x * 2:x * 2 + 2]


cards = []
for card in os.listdir('pokemon cards'):
    cards.append(BACard('pokemon cards/' + card))


def find(x, y, cardpool, frame):
    distance = 881023
    curcard = None
    for card in cardpool:
        compare = card.compare(frame.getarray(x, y))
        if distance > compare:
            distance = compare
            curcard = card
    return curcard


def run(url):
    image = Image.open(url)
    frame = Frame(np.asarray(image))
    curframe = [[], [], [], [], [], [], [], [], []]
    cardpool = cards
    for y in range(9):
        for x in range(16):
            curcard = find(x, y, cardpool, frame)
            cardpool.remove(curcard)
            image = np.asarray(Image.open('full cards/' + curcard.card_id + '.png').convert("RGBA").resize((200, 275)))
            curframe[y].append(image)
    yframe = []
    for y in range(9):
        yframe.append(curframe[y][0])
        for x in range(15):
            yframe[y] = (np.concatenate((yframe[y], curframe[y][x+1]), axis=1))
    out = yframe[0]
    for y in range(8):
        out = (np.concatenate((out, yframe[y+1]), axis=0))
    imgs_comb = Image.fromarray(out)
    print("saving " + Path(url).stem)
    imgs_comb.save('renderedFrames/' + Path(url).stem + '.png')


if __name__ == "__main__":
    frames = ["resizedFrames/frame0001.bmp", "resizedFrames/frame0073.bmp", "resizedFrames/frame0084.bmp", "resizedFrames/frame2245.bmp"]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(run, frames)

#os.listdir('resizedFrames')