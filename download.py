from pokemontcgsdk import Card
from PIL import Image
import requests
from io import BytesIO
from multiprocessing.dummy import Pool as ThreadPool
i = 1


while True:
    cards = Card.where(q='types:Darkness', page=i, pageSize=50)
    print(i)
    if len(cards) == 0:
        break
    urls = []
    for card in cards:
        urls.append(card.images.small)
    with ThreadPool(50) as pool:
        img_data = list(pool.map(requests.get, urls))
    r = 0
    for card in img_data:
        image = Image.open(BytesIO(card.content))
        new_image = image.resize((2, 2))
        image.save('full cards/' + cards[r].id + ".png")
        new_image.save('pokemon cards/' + cards[r].id + ".png")
        r += 1
    i += 1
    print("page finished")
