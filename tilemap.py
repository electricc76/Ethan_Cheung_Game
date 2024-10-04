# this file was created by Ethan Cheung

import pygame as pg
from settings import *

# turns the text file into a list
class Map:
    def __init__(self, filename):
        self.data = []
        # for every row in the level, removes white spaces then appends it to the list as a chunk. 
        # When that is done,it goes to the next line and adds it as another element
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE