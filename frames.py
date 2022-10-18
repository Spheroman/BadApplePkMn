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

    async def geturl(self):
        cur = Card.find(self.card_id)
        return cur.images.small

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
        assert x * 2 < len(self.full_frame[1]) and x >= 0
        assert y * 2 < len(self.full_frame) and y >= 0
        return self.full_frame[y * 2:y * 2 + 2, x * 2:x * 2 + 2]


image = Image.open('resizedFrames/frame0895.bmp')
frame = Frame(np.asarray(image))

cards = []


async def main():
    for card in os.listdir('pokemon cards'):
        cards.append(BACard('pokemon cards/' + card))

    distance = 881023
    curcard = None
    for card in cards:
        compare = card.compare(frame.getarray(4, 3))
        if distance > compare:
            distance = compare
            curcard = card
    print(curcard.card_id)
    print((Card.find(curcard.card_id)).images.large)
    print('done')


if __name__ == "__main__":
    asyncio.run(main())
