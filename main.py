# this file was created by Ethan Cheung

# import all necessary modules and libraries
import pygame as pg

from settings import *
from sprites import *
from random import randint

# created a game class to instantiate later
# it will have all the neccessary parts to run the game
class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Ethan's Game")
        self.clock = pg.time.Clock()
        self.running = True
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self, 50,50)
        # instantiated a mob
        self.mob = Mob(self, 100,100)
        for i in range(6):
            Mob(self, i*randint(0, 200), i * randint (0, 200))
        for i in range(6):
            Wall(self, i*TILESIZE,128)
    
    def run(self):
        while self.running: 
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    
        # input
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                
        # process
    def update(self):
        self.all_sprites.update()

        # output
        print(self.player.rect.colliderect(self.mob))
        pass

        # output
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()




if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()