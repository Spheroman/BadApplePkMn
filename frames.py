from PIL import Image
import numpy as np
from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype
from pokemontcgsdk import Rarity
from pathlib import Path
import os
import asyncio
from pokemontcgsdk import RestClient

RestClient.configure('12345678-1234-1234-1234-123456789ABC')


class BACard:
    def __init__(self, a):
        self.card_id = Path(a).stem
        self.card_pixels = np.asarray(Image.open(a))

    def geturl(self):
        return 'full cards' + self.card_id + '.png'

    def compare(self, i):
        total_avg = 0
        for y in range(2):
            for x in range(2):
                for rgb in range(3):
                    total_avg += abs(int(self.card_pixels[y][x][rgb]) - int(i[y][x][rgb]))
        return total_avg


class Frame:
    def __init__(self, a):
        self.full_frame = a

    def getarray(self, x, y):
        assert x * 2 <= len(self.full_frame[1]) and x >= 0
        assert y * 2 <= len(self.full_frame) and y >= 0
        return self.full_frame[y * 2:y * 2 + 2, x * 2:x * 2 + 2]


image = Image.open('resizedFrames/frame0117.bmp')
frame = Frame(np.asarray(image))

cards = []
for card in os.listdir('pokemon cards'):
    cards.append(BACard('pokemon cards/' + card))


def find(x, y, list):
    distance = 881023
    curcard = None
    for card in list:
        compare = card.compare(frame.getarray(x, y))
        if distance > compare:
            distance = compare
            curcard = card
    return curcard


def main():
    curframe = [[], [], [], [], [], [], [], [], []]
    list = cards
    for y in range(9):
        for x in range(16):
            curcard = find(x, y, list)
            #list.remove(curcard)
            image = np.asarray(Image.open('full cards/' + curcard.card_id + '.png').convert("RGB").resize((240, 330)))
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
    imgs_comb.save('frame.png')



if __name__ == "__main__":
    main()
