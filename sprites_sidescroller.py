# this file was created by Ethan Cheung

import pygame as pg
from pygame.sprite import Sprite
from settings import *
import random
import math

# vector - force and direction
# (x, y)
vec = pg.math.Vector2

class Player(Sprite):
    def __init__(self, game, x, y):
        # Links up self.groups and main through game.all_sprites
        self.groups = game.all_sprites, game.all_players
        # Initializes the sprite in the group of all the players
        Sprite.__init__(self, self.groups)
        self.game = game
        # the player is 32 pixels by 32 pixels
        self.image = pg.Surface((TILESIZE,TILESIZE))
        # the player's hitbox is the image size
        self.rect = self.image.get_rect()
        # the player is red
        self.image.fill(RED)
        self.pos = vec(x*TILESIZE, y*TILESIZE)
        # numbers in vel = slope, rise over run.
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.speed = 2
        # is the player in the process of jumping
        self.jumping = False
        # is the player in the process of double jumping
        self.double_jumping = False
        self.jump_power = 13
        self.double_jump_power = 11
        self.level_coins = 0

    def get_keys(self):
        # Load anything pressed on the keyboard into the variable "keys"
        # Checks if any of the keys pressed = A S W or D. If so, it makes the if True.
        # constantly listening to see if keys are pressed
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.jump()
        if keys[pg.K_SPACE]:
            self.double_jump()
        if keys[pg.K_a]:
            self.vel.x -= self.speed
        if keys[pg.K_d]:
            self.vel.x += self.speed


    def jump(self):
        # Technically, the player isn't on the platform, they are right above it, so this peeks to see if
        # there is a floor to jump off of
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        self.rect.y -= 2
        # If there is a floor and I'm not jumping, jump
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -self.jump_power
            print("B o i n g")
            self.game.jump_snd.play()

    
    def double_jump(self): 
        if self.double_jumping == False:
            self.vel.y = -self.double_jump_power
            self.double_jumping = True
            self.game.double_jump_snd.play()
        else:
            pass
    
    # constantly checking to see if it collides with a wall, and corrects it if it does.
    def collide_with_walls(self, dir):
        # moving left or right
        if dir == 'x':
            # colliding with walls, False means the walls don't die upon collision
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                # If you collide from the right, set your position to the place were upon hit, - the rectangle width
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                # If you collide from the right, set your position to the place were upon hit
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                # Remove your velocity
                self.vel.x = 0
                # move your hitbox to your position
                self.rect.x = self.pos.x
        # moving up or down
        # same as above, but vertical now
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    # upon hitting the ground, make yourself able to double jump and jump again
                    self.pos.y = hits[0].rect.top - self.rect.height
                    self.jumping = False
                    self.double_jumping = False
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Powerup":
                self.jump_power += 2
                self.double_jump_power += 4
                print("I hit a powerup  :D")
                self.game.powerup_snd.play()
            # upon hitting coin, gain coin
            if str(hits[0].__class__.__name__) == "Coin":
                print("$  $  $  $  $")
                self.level_coins += 1
                self.game.coin_snd.play()
            # upon hitting spike, delete player
            if str(hits[0].__class__.__name__) == "Spike":
                print("Collided with Spike")
                self.game.death_snd.play()
                self.game.death()
            
            # upon hitting mob, delete player
            if str(hits[0].__class__.__name__) == "Mob":
                print("Collided with Mob")
                self.game.death_snd.play()
                self.game.death()
            if str(hits[0].__class__.__name__) == "Portal":
                print("Collided with portal")
                self.game.next_level()

            if str(hits[0].__class__.__name__) == "Boss":
                print("collided with boss")
                self.game.death_snd.play()
                self.game.death()
            
            if str(hits[0].__class__.__name__) == "Bullet":
                print("Got Shot")
                self.game.death_snd.play()
                self.game.death()


    def update(self):
        # every tic, accelerate yourself downwards due to gravity
        self.acc = vec(0, GRAVITY)
        # check to see which keys are being pressed
        self.get_keys()

        # slowly reduce acceleration due to Friction
        self.acc.x += self.vel.x * FRICTION
        # acceleration in any direction will affect the velocity in that direction
        self.vel += self.acc

        # If your velocity is low enough, just set it to zero, because friction would just reduce it
        # to near zero without actually getting there
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0

        # some physics equation, not entirely accurate without calculus
        self.pos += self.vel + 0.5 * self.acc

        # self.x += self.vx * self.game.dt
        # self.y += self.vy * self.game.dt

        # Check if collided with these things, and what to do about them
        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)
        self.collide_with_stuff(self.game.all_spikes, False)
        self.collide_with_stuff(self.game.all_mobs, False)
        self.collide_with_stuff(self.game.all_portals, False)
        self.collide_with_stuff(self.game.all_bosses, False)
        self.collide_with_stuff(self.game.all_bullets, False)

        # check for x position then correct it. Check for y position then correct it. Order is critical
        self.rect.x = self.pos.x
        self.collide_with_walls('x')

        self.rect.y = self.pos.y
        self.collide_with_walls('y')

        global player_pos_x, player_pos_y
        player_pos_x = self.pos.x
        player_pos_y = self.pos.y

class Mob(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_mobs
        # initialize yourself in all of your groups
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.rect = self.image.get_rect()
        # mob is green
        self.image.fill(GREEN)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 10
    def update(self):
        # change your position based on the speed number
        self.rect.x += self.speed
        # if your right hits the width of the screen - 1 tile, turn around. Same with left side

        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits:
            if self.rect.right > 0:
                self.speed *= -1
            if self.rect.left < 0:
                self.speed *= -1
            
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Powerup(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coin(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Spike(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_spikes
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Portal(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_portals
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Bullet(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_bullets
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.bullet_speed = 10

        self.rect.x = x + TILESIZE
        self.rect.y = y + TILESIZE
        self.opposite = player_pos_y/TILESIZE - self.rect.y/TILESIZE
        self.adjacent = self.rect.x/TILESIZE - player_pos_x/TILESIZE
        self.angle = math.atan(self.opposite / self.adjacent)
        if player_pos_x > self.rect.x:
            self.speed_x = -self.bullet_speed*math.cos(self.angle)
            self.speed_y = -self.bullet_speed*math.sin(self.angle)
        else:
            self.speed_x = self.bullet_speed*math.cos(self.angle)
            self.speed_y = self.bullet_speed*math.sin(self.angle)


    def update(self):
        self.rect.x -= self.speed_x
        self.rect.y += self.speed_y

        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits:
            self.kill()


class Boss(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_bosses
        # initialize yourself in all of your groups
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE * 3, TILESIZE * 3))
        self.rect = self.image.get_rect()
        # Boss is green
        self.image.fill(GREEN)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        print("Boss Created")
        self.attack_timer = 0
        self.speed = 5
        global boss_position
        boss_position = vec(x*TILESIZE, y*TILESIZE)


    def update(self):
        self.attack_timer += 1
        if self.attack_timer == 30:
            Bullet(self.game, self.rect.x, self.rect.y)
            self.attack_timer = 0

        # change your position based on the speed number
        self.rect.x += self.speed
        # if your right hits the width of the screen - 1 tile, turn around. Same with left side

        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits:
            if self.rect.right > 0:
                self.speed *= -1
            if self.rect.left < 0:
                self.speed *= -1