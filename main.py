# this file was created by Ethan Cheung

# import all necessary modules and libraries
import pygame as pg
from settings import *
from sprites import *
from random import randint

# created a game class to instantiate later
# it will have all the neccessary parts to run the game
# game class is used to organize parts used to create the game
class Game:
    # __init__ method: initlaizes all the necessary components for the game, including audio and video
    def __init__(self):
        # initializes the ability to use pygame
        pg.init()
        # used for sound
        pg.mixer.init()
        # sets how big the window is in pixels
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # names the game "Ethan's Game"
        pg.display.set_caption("Ethan's Game")
        # creates a clock so we can set the framerate
        self.clock = pg.time.Clock()
        # is the game running or not? Yes
        self.running = True

    def new(self):
        # creates all_sprites group so we can batch update and render
        # defines properties that can be seen in the game system
        self.all_sprites = pg.sprite.Group()
        # instantiated a mob and a player at x and y
        self.player = Player(self, 1,1)
        self.mob = Mob(self, 100, 100)
        # makes new mobs and walls using a for loop
        for i in range(10):
            Mob(self, i*randint(0, 200), i * randint (0, 200))
            Wall(self, i*TILESIZE, i*TILESIZE)
    
    # if the game is running (self.running = TRUE), the methods are called. events() lists out any 
    # events that happen at that time. update() updates everything about the game once per tick. draw() actually
    # draws out the new updated screen
    def run(self):
        while self.running: 
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    
        # input
    
    # looks for any events, specifically looks for closing the game with 'x'
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                
        # process
    def update(self):
        # a list of all the sprites in the game, updates all of them at once
        self.all_sprites.update()

        # output
        print(self.player.rect.colliderect(self.mob))
        pass

        # output
    # covers the whole screen with black, then paints the new, updated sprites back on
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()



# checks the file name and creates a game object based on the Game() class.
if __name__ == "__main__":
    g = Game()
    # create all game elements with the new method (not function)
    g.new()
    # run the game
    g.run()