# this file was created by Ethan Cheung

import pygame as pg
from pygame.sprite import Sprite
from settings import *
import random

class Player(Sprite):
    def __init__(self, game, x, y):
        # Links up self.groups and main through game.all_sprites
        self.groups = game.all_sprites
        # Initializes the sprite in the group of all the players
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 10
        self.vx, self.vy = 0, 0
    
    def get_keys(self):
        # Load anything pressed on the keyboard into the variable "keys"
        # Checks if any of the keys pressed = A S W or D. If so, it makes the if True.
        # constantly listening to see if keys are pressed
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.vy -= self.speed
        if keys[pg.K_a]:
            self.vx -= self.speed
        if keys[pg.K_s]:
            self.vy += self.speed
        if keys[pg.K_d]:
            self.vx += self.speed
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        self.rect.x = self.x
        self.rect.y = self.y
        
class Mob(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(GREEN)
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        self.category = random.choice([0,1])
    def update(self):
        self.rect.x += self.speed
        # moving towards the side of the screen
        if self.rect.right > WIDTH or self.rect.left < 0:
            print("off the screen...")
            self.speed *= -1
            self.rect.y += 32

        # When it hits the end of the screen, it moves down
        # turns around and goes the other way
        # if it hits the bottom of the screen, it moves to the top of the screen
        # display logic in the terminal
        pass

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass