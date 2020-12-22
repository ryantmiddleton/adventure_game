# Sprite classes for Metroidvania game
import pygame as pg
from settings import *
import random
vec = pg.math.Vector2

from pygame.locals import (
  RLEACCEL,
  K_UP,
  K_DOWN,
  K_LEFT,
  K_RIGHT,
  K_ESCAPE,
  KEYDOWN,
  QUIT,
  K_w,
  K_a,
  K_s,
  K_d,
)


class Player(pg.sprite.Sprite):
  def __init__(self, game):
    pg.sprite.Sprite.__init__(self)
    self.game = game
    # Player Image
    
    
    self.image = pg.image.load("imgs/idle outline.gif").convert()
    self.image.set_colorkey((255, 255, 255), RLEACCEL)
    self.rect = self.image.get_rect()
    self.rect.center = (WIDTH/2, HEIGHT/2)
    self.pos = vec(WIDTH/2, HEIGHT/2)
    self.vel = vec(0, 0)
    self.acc = vec(0, 0)

  def jump(self):
    self.rect.y += 1
    hits = pg.sprite.spritecollide(self, self.game.platforms, False)
    self.rect.y -= 1
    if hits:  
      self.vel.y = -15

  def update(self):
    self.acc = vec(0, PLAYER_GRAV)
    keys = pg.key.get_pressed()
    # move left
    if keys[pg.K_LEFT]:
      self.image = pg.image.load("imgs/left_run.gif").convert()
      self.image.set_colorkey((255, 255, 255), RLEACCEL)
      self.acc.x = -PLAYER_ACC
      self.left = True
    #move right
    if keys[pg.K_RIGHT]:
      self.image = pg.image.load("imgs/run outline.gif").convert()
      self.image.set_colorkey((255, 255, 255), RLEACCEL)
      self.acc.x = PLAYER_ACC
      self.left = False


    # apply friction
    self.acc.x += self.vel.x * PLAYER_FRICTION
    # equations of motion
    self.vel += self.acc
    self.pos += self.vel + 0.5 * self.acc
    # collision detection
    if self.pos.x > WIDTH -self.rect.width/2:
      self.pos.x = WIDTH - self.rect.width/2
    if self.pos.x < 0 + self.rect.width/2:
      self.pos.x = 0 + self.rect.width/2

    self.rect.midbottom = self.pos

class Bullet(pg.sprite.Sprite):
  def __init__(self, x, y, facing):
    pg.sprite.Sprite.__init__(self)
    self.facing = facing
    if facing == 2:
      self.image = pg.image.load("imgs/bullet-up.png").convert()
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y-80
    elif facing == -1:
      self.image = pg.image.load("imgs/bullet-left.png").convert()
      self.rect = self.image.get_rect()
      self.rect.x = x-40
      self.rect.y = y-20
    elif facing == 3:
      self.image = pg.image.load("imgs/bullet-diag-right.png").convert()
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y-50
    elif facing == -3:
      self.image = pg.image.load("imgs/bullet-diag-left.png").convert()
      self.rect = self.image.get_rect()
      self.rect.x = x-20
      self.rect.y = y-50
    else:
      self.image = pg.image.load("imgs/bullet.png").convert()
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y-20
    self.image.set_colorkey((WHITE), RLEACCEL)

  def update(self):
    if self.facing == 3:
      self.rect.y += -8
      self.rect.x += 8
    elif self.facing == -3:
      self.rect.y += -8
      self.rect.x += -8
    elif self.facing == 2:
      self.rect.y += -8

    else:
      self.rect.x += (8*self.facing)

    if self.rect.left > WIDTH: 
      self.kill()
    elif self.rect.right < 0:
      self.kill()

class Platform(pg.sprite.Sprite):
  def __init__(self, x, y, w, h):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.Surface((w, h))
    self.image.fill(GREEN)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y  

