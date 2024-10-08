# this file was created by Ethan Cheung

# import all necessary modules and libraries
import pygame as pg

from tilemap import *
from settings import *
from sprites import *
from os import path
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
    
    # loads all the data such as audio and level design by reading text file
    def load_data(self):
        # creates game_folder
        self.game_folder = path.dirname(__file__)
        # join the game_folder
        self.map = Map(path.join(self.game_folder, 'level1.txt'))


    def new(self):
        self.load_data()
        # creates all_sprites group so we can batch update and render
        # defines properties that can be seen in the game system
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group
        self.all_powerups = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        # makes new mobs and walls using a for loop
        
        # takes map.data and parses it using enumerate so that we can assign x y values to each object instance
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                # If there is a 1, it creates a wall there with the x and y value being the column and row
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'U':
                    Powerup(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                    
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

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font("arial")
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)

        # output
    # covers the whole screen with black, then paints the new, updated sprites back on
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.dt*1000), 24, WHITE, WIDTH / 24, HEIGHT / 24)
        self.draw_text(self.screen, "Coins collected: " + str(self.player.coins), 24, WHITE, WIDTH / 2, HEIGHT / 24)
        self.draw_text(self.screen, "Game Name", 24, WHITE, WIDTH / 2, HEIGHT / 192)
        pg.display.flip()



# checks the file name and creates a game object based on the Game() class.
if __name__ == "__main__":
    g = Game()
    # create all game elements with the new method (not function)
    g.new()
    # run the game
    g.run()