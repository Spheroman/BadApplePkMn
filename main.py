import numpy as np
from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from PIL import Image
import os

for filename in os.listdir('frames'):
    image = Image.open(os.path.join('frames', filename))
    new_image = image.resize((24, 12))
    new_image.save(os.path.join('resizedFrames', filename))
