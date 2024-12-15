# this file was created by Ethan Cheung
# Mr. Cozort Said I had to

'''
Elevator Pitch: I want to create a game

GOALS: Go down into the Crypt, collect the crown of Mac Guffin, and get out alive
RULES: Player will die when hitting traps, player can stand on platforms, Player 
can jump and double jump to move around. Jump height fixed
FEEDBACK: Sound effects upon jumping, dashing, and dying. Death, coins collected,
and time counter at the top of the screen
FREEDOM: Player can move around as they wish, may be ways to complete levels in
different ways.

What sentence does your game make?

When the player collides with an spike, the player dies
When the player collides with a mob, the player dies

'''

'''
Sources:
Mr. Cozort for portal code

'''


# import all necessary modules and libraries
import pygame as pg
from settings import *
from sprites_sidescroller import *
from tilemap import *
from os import path
import sys
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
        self.level = 1
        self.score = 0
        self.highscore = 0
        self.death_counter = 0
        self.coins = 0
    
    # loads all the data such as audio and level design by reading text file
    def load_data(self):
        # creates game_folder
        self.game_folder = path.dirname(__file__)
        # Load high score file

        # from chatGPT - prompt: with open
        with open(path.join(self.game_folder, HS_FILE), 'w') as f:
            f.write(str(self.highscore))

        print("file created and written successfully")

        with open(path.join(self.game_folder, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        
        self.snd_folder = path.join(self.game_folder, 'sounds')
        # join the game_folder
        self.map = Map(path.join(self.game_folder, 'level'+str(self.level)+'.txt'))

        # load sounds
        self.double_jump_snd = pg.mixer.Sound(path.join(self.snd_folder, 'double_jump.wav'))
        self.jump_snd = pg.mixer.Sound(path.join(self.snd_folder, 'jump.mp3'))
        self.death_snd = pg.mixer.Sound(path.join(self.snd_folder, 'death.mp3'))
        self.powerup_snd = pg.mixer.Sound(path.join(self.snd_folder, 'powerup.wav'))
        self.coin_snd = pg.mixer.Sound(path.join(self.snd_folder, 'coin.mp3'))

    def death(self):
        # remove all existing sprites before redrawing them on
        for s in self.all_sprites:
            s.kill()
        self.player.jump_power = 13
        self.player.double_jump_power = 11
        self.map = Map(path.join(self.game_folder, 'level'+str(self.level)+'.txt'))
        self.death_counter += 1
        self.player.level_coins = 0
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
                if tile == 'S':
                    Spike(self, col, row)
                if tile == 'O':
                    Portal(self, col, row)
                if tile == 'B':
                    Boss(self, col, row)

    def next_level(self):
        # remove all existing sprites before redrawing them on
        for s in self.all_sprites:
            s.kill()
        self.player.jump_power = 13
        self.player.double_jump_power = 11
        self.level += 1
        self.map = Map(path.join(self.game_folder, 'level'+str(self.level)+'.txt'))
        self.coins += self.player.level_coins
        self.player.level_coins = 0
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
                if tile == 'S':
                    Spike(self, col, row)
                if tile == 'O':
                    Portal(self, col, row)
                if tile == 'B':
                    Boss(self, col, row)


    def new(self):
        self.load_data()
        # creates all_sprites group so we can batch update and render
        # defines properties that can be seen in the game system
        self.all_players = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_powerups = pg.sprite.Group()
        self.all_spikes = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_portals = pg.sprite.Group()
        self.all_bosses = pg.sprite.Group()
        self.all_bullets = pg.sprite.Group()
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
                if tile == 'S':
                    Spike(self, col, row)
                if tile == 'O':
                    Portal(self, col, row)
                if tile == 'B':
                    Boss(self, col, row)

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
                if self.score > self.highscore:
                    self.highscore = self.score
                    with open(path.join(self.dir, HS_FILE), 'w') as f:
                        f.write(str(self.score))
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
        ticks = pg.time.get_ticks()
        self.draw_text(self.screen, str(self.dt*1000), 24, WHITE, WIDTH / 24, HEIGHT / 24)
        self.draw_text(self.screen, "Total Coins: " + str(self.coins), 24, WHITE, WIDTH / 3, HEIGHT / 192)
        self.draw_text(self.screen, "Current Coins: " + str(self.player.level_coins), 24, WHITE, 2 * WIDTH / 3, HEIGHT / 192)
        self.draw_text(self.screen, "Timer: "+str(ticks/1000), 24, WHITE, WIDTH / 2, HEIGHT / 192)
        self.draw_text(self.screen, "Deaths: "+str(self.death_counter), 24, WHITE, WIDTH / 6, HEIGHT / 192)
        pg.display.flip()



# checks the file name and creates a game object based on the Game() class.
if __name__ == "__main__":
    g = Game()
    # create all game elements with the new method (not function)
    g.new()
    # run the game
    g.run()