# Sprite classes for Metroidvania game
import pygame as pg
import math
from settings import *
import random
vec = pg.math.Vector2
pg.font.init()
font = pg.font.SysFont(None, 26)
from pygame.locals import (
  RLEACCEL,
  K_UP,
  K_DOWN,
  K_LEFT,
  K_RIGHT,
  K_ESCAPE,
  K_SPACE,
  KEYDOWN,
  QUIT,
)

class Player(pg.sprite.Sprite):
  def __init__(self, game):
    pg.sprite.Sprite.__init__(self)
    self.game = game
    # Player Image
    self.IDLE_IMAGE = pg.transform.rotozoom(pg.image.load("img/idle outline.gif").convert(), 0, 2)
    self.LEFT_IMAGE = pg.transform.rotozoom(pg.image.load("img/left_run.gif").convert(), 0, 2)
    self.RIGHT_IMAGE = pg.transform.rotozoom(pg.image.load("img/run outline.gif").convert(), 0, 2)

    self.image = self.IDLE_IMAGE
    self.image.set_colorkey((WHITE), RLEACCEL)
    self.rect = self.image.get_rect()
    self.rect.center = (WIDTH/2, HEIGHT/2)
    self.pos = vec(WIDTH/2, HEIGHT-40)
    self.vel = vec(0, 0)
    self.acc = vec(0, 0)
    self.right = True
    self.left = False

  def jump(self):
    if isStanding(self):
      self.vel.y = -15

  def update(self):
    self.acc = vec(0, PLAYER_GRAV)
    keys = pg.key.get_pressed()
    # move left
    if keys[K_LEFT]:
      self.image = self.LEFT_IMAGE
      self.image.set_colorkey((WHITE), RLEACCEL)
      self.acc.x = -PLAYER_ACC
      self.right = False
      self.left = True
    #move right
    if keys[K_RIGHT]:
      self.image = self.RIGHT_IMAGE
      self.image.set_colorkey((WHITE), RLEACCEL)
      self.acc.x = PLAYER_ACC
      self.right = True
      self.left = False

    # apply friction
    self.acc.x += self.vel.x * PLAYER_FRICTION

    # equations of motion
    self.vel += self.acc
    self.pos += self.vel + 0.5 * self.acc

    # collision detection
    if self.pos.x > WIDTH - self.rect.width/2:
      self.pos.x = WIDTH - self.rect.width/2
    if self.pos.x < 0 + self.rect.width/2:
      self.pos.x = 0 + self.rect.width/2

    self.rect.midbottom = self.pos

class Bullet(pg.sprite.Sprite):
  def __init__(self, x, y, facing):
    pg.sprite.Sprite.__init__(self)
    self.facing = facing
    if facing == -1:
      self.image = pg.image.load("img/bullet-left.png").convert()
      self.rect = self.image.get_rect()
      self.rect.x = x-40
      self.rect.y = y-40
    else:
      self.image = pg.image.load("img/bullet.png").convert()
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y-40
    self.image.set_colorkey((WHITE), RLEACCEL)
    self.vel = vec(0.5, 0)
    self.acc = vec(0, 0)

  def update(self):
    self.rect.x += (8*self.facing)
    if self.rect.left > WIDTH: 
      self.kill()
    elif self.rect.right < 0:
      self.kill()

class Spider(pg.sprite.Sprite):
  def __init__(self, x, y, game):
    pg.sprite.Sprite.__init__(self)
    self.game = game
    self.spider_sheet = pg.image.load("img/spiders.png").convert_alpha()
    self.size = self.spider_sheet.get_size()
    self.frames = strip_from_sheet(self.spider_sheet,(0,6),(2,6),(self.size[0]/12,self.size[1]/8))
    for i in range(len(self.frames)):
      self.frames[i] = crop(self.frames[i],(10,20),(65,45))
      self.frames[i] = pg.transform.rotozoom(self.frames[i], 180, 0.5)
    self.image_num = 0
    self.anima_speed = 6
    self.image = self.frames[self.image_num]
  
    # self.rect.y = y, self.rect.x = x
    self.rect = self.image.get_rect(topleft=(x,y))

    # 0-right-facing/right, 90-right-facing/down, 180-hanging/left, 270-right-facing/up
    self.orient = 180
    self.dir = 0

  def update(self):
    # Animate the spider's legs by cycling through each image
    if self.image_num < len(self.frames) and self.anima_speed == 0:
      self.image_num += 1
      if self.image_num == len(self.frames):
        self.image_num = 0
      self.anima_speed = 6
      self.image = self.frames[self.image_num]
    else:
      self.anima_speed -= 1
    
    # Move the spider
    if isHanging(self):
      if self.dir == LEFT:
        self.rect.x -= 1
      elif self.dir == RIGHT:
        self.rect.x += 1
      print("hanging")

    elif isGripping_right(self):
      if self.dir == UP:
        self.rect.y -= 1
      if self.dir == DOWN:
        self.rect.y += 1
      print("gripping right")
      
    # elif isStanding(self):
    #   if self.dir == LEFT:
    #     self.rect.x -= 1
    #   elif self.dir == RIGHT:
    #     self.rect.x += 1
    #   print("walking")

    # elif isGripping_left(self):
    #   if self.dir == UP:
    #     self.rect.y -= 1
    #   if self.dir == DOWN:
    #     self.rect.y += 1
    #   print("gripping left")

    else:
      print("changing direction")
      if self.dir == LEFT:
        print("rotating UP to 270")
        self.dir = UP
        self.orient = 270
        self.image = pg.transform.rotate(self.frames[self.image_num], self.orient)
        self.rect.y -= 1
      elif self.dir == UP:
        print("rotating RIGHT to 0")
        self.dir = RIGHT
        self.orient = 0
        self.image = pg.transform.rotate(self.frames[self.image_num], self.orient)
        self.rect.x += 1
      elif self.dir == RIGHT:
        print("rotating DOWN to 90")
        self.dir = DOWN
        self.orient = 90
        self.image = pg.transform.rotate(self.frames[self.image_num], self.orient)
        self.rect.y += 1
      elif self.dir == RIGHT:
        print("rotating RIGHT to 180")
        self.dir = RIGHT
        self.orient = 180
        self.image = pg.transform.rotate(self.frames[self.image_num], self.orient)
        self.rect.y += 1
      

class Platform(pg.sprite.Sprite):
  def __init__(self, x, y, w, h):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.Surface((w, h))
    self.image.fill(SILVER)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y      

def isStanding(sprite):
  sprite.rect.y += 1
  hits = pg.sprite.spritecollide (sprite, sprite.game.platforms, False)
  sprite.rect.y -= 1
  if hits:
    return True
  else:  
    return False

def isHanging(sprite):
  sprite.rect.y -= 1
  hits = pg.sprite.spritecollide (sprite, sprite.game.platforms, False)
  sprite.rect.y += 1
  if hits:
    return True
  else:  
    return False

def isGripping_right(sprite):
  sprite.rect.x += 1
  hits = pg.sprite.spritecollide (sprite, sprite.game.platforms, False)
  sprite.rect.x -= 1
  if hits:
    return True
  else:  
    return False
  
def isGripping_left(sprite):
  sprite.rect.x -= 1
  hits = pg.sprite.spritecollide (sprite, sprite.game.platforms, False)
  sprite.rect.x += 1
  if hits:
    return True
  else:  
    return False

def strip_from_sheet(sheet, start, end, size):
  # Strips individual frames from a sprite sheet given a start location,
  # sprite size, and number of columns and rows.
  frames = []
  for x in range(start[0],end[0]+1):
      for y in range(start[1],end[1]+1):
          location = (size[0]*x, size[1]*y)
          frames.append(sheet.subsurface(pg.Rect(location, size)))
  return frames

def crop(image, start_pos, new_size):
  old_size = image.get_size()
  # start_pos = (old_size[0]-new_size[0], old_size[1]-new_size[1])
  cropped_image = pg.Surface(new_size)
  cropped_image.blit(image, (0,0), (start_pos[0], start_pos[1], old_size[0], old_size[1]))
  return cropped_image