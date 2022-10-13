import numpy as np
from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from PIL import Image
import os
from pokemontcgsdk import RestClient
import requests
import asyncio
import threading
from io import BytesIO
from multiprocessing.dummy import Pool as ThreadPool

RestClient.configure('6797477a-7410-40ec-b0df-caf3050c4a3e')
i = 1
while True:
    cards = Card.where(q='types:Metal', page=i, pageSize=50)
    print(i)
    if len(cards) == 0:
        break
    urls = []
    for card in cards:
        print(card.id)
        print(card.images.small)
        urls.append(card.images.small)
    with ThreadPool(50) as pool:
        img_data = list(pool.map(requests.get, urls))
    r = 0
    for card in img_data:
        image = Image.open(BytesIO(card.content))
        new_image = image.resize((2, 2))
        print(cards[r].id)
        new_image.save('pokemon cards/' + cards[r].id + ".png")
        r+=1
    i += 1
    print("page finished")



# for filename in os.listdir('frames'):
#    image = Image.open(os.path.join('frames', filename))
#    new_image = image.resize((32, 18))
#    new_image.save(os.path.join('resizedFrames', filename))
