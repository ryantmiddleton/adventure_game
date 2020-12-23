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
  K_w,
  K_a,
  K_s,
  K_d,
)

class Spirtesheet:
  def __init__(self, filename):
    self.spritesheet = pg.image.load(filename).convert()

  def get_image(self, x, y, width, height):
    image = pg.Surface((width, height))
    image.blit(self.spritesheet, (0,0), (x, y, width, height))
    image = pg.transform.scale(image, (width //2, height// 2))
    return image


class Player(pg.sprite.Sprite):
      def __init__(self, game):
    pg.sprite.Sprite.__init__(self)
    self.game = game
    # Player Image
    self.jumping = False
    self.image = pg.image.load("imgs/idle outline.png").convert()
    self.image.set_colorkey((255, 255, 255), RLEACCEL)
    self.rect = self.image.get_rect()
    self.rect.center = (WIDTH/2, HEIGHT/2)
    self.pos = vec(0, HEIGHT-40)
    self.vel = vec(0, 0)
    self.acc = vec(0, 0)
    self.level = 1
    self.left = False
    self.health = PLAYER_HEALTH
    self.max_health = PLAYER_HEALTH


  def jump_cut(self):
    if self.jumping:
      if self.vel.y < -3:
        self.vel.y = -3

  def jump(self):
    self.rect.y += 1
    hits = pg.sprite.spritecollide(self, self.game.platforms, False)
    self.rect.y -= 1
    if hits and not self.jumping:  
      self.jumping = True
      self.vel.y = -15
      self.game.jump_sound.play()

  def update(self):
    self.acc = vec(0, PLAYER_GRAV)
    keys = pg.key.get_pressed()
    # move left
    if keys[pg.K_LEFT]:
      self.image = pg.image.load("imgs/left_run.png").convert()
      self.image.set_colorkey((255, 255, 255), RLEACCEL)
      self.acc.x = -PLAYER_ACC
      self.left = True
    #move right
    if keys[pg.K_RIGHT]:
      self.image = pg.image.load("imgs/run_right.png").convert()
      self.image.set_colorkey((255, 255, 255), RLEACCEL)
      self.acc.x = PLAYER_ACC
      self.left = False
    if keys[pg.K_UP]:
      self.image = pg.image.load("imgs/jump outline.png").convert()
      self.image.set_colorkey((255, 255, 255), RLEACCEL)
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
      self.image = pg.image.load("img/bullet-up.png").convert()
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y-80
    elif facing == -1:
      self.image = pg.image.load("img/bullet-left.png").convert()
      self.rect = self.image.get_rect()
      self.rect.x = x-40
      self.rect.y = y-20
    elif facing == 3:
      self.image = pg.image.load("img/bullet-diag-right.png").convert()
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y-50
    elif facing == -3:
      self.image = pg.image.load("img/bullet-diag-left.png").convert()
      self.rect = self.image.get_rect()
      self.rect.x = x-20
      self.rect.y = y-50
    else:
      self.image = pg.image.load("img/bullet.png").convert()
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
  def __init__(self, game, x, y):
    pg.sprite.Sprite.__init__(self)
    self.game = game
    self.game.spritesheet.get_image(0, 288, 380, 94)
    self.image.set_colorkey(BLACK)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y  

class Spider(pg.sprite.Sprite):
  def __init__(self, x, y, game):
    pg.sprite.Sprite.__init__(self)
    self.game = game
    self.spider_sheet = pg.image.load("img/spiders.png").convert_alpha()
    self.size = self.spider_sheet.get_size()
    self.frames = strip_from_sheet(self.spider_sheet,(6,6),(8,6),(self.size[0]/12,self.size[1]/8))
    for i in range(len(self.frames)):
      self.frames[i] = crop(self.frames[i],(10,20),(65,45))
      # self.frames[i] = pg.transform.flip(self.frames[i], True, False)
      self.frames[i] = pg.transform.rotozoom(self.frames[i], 0, 1)
    self.image_num = 0
    self.anima_speed = 6
    self.image = self.frames[self.image_num]
    # self.rect.y = y, self.rect.x = x
    self.rect = self.image.get_rect(topleft=(x,y))

    # 0-right-facing/right, 90-up/legs right, 180-hanging/left, 270-down/leg left
    self.orient = 180
    self.dir = LEFT

  def update(self):
    # Animate the spider's legs by cycling through each image
    if self.image_num < len(self.frames) and self.anima_speed == 0:
      self.image_num += 1
      if self.image_num == len(self.frames):
        self.image_num = 0
      self.anima_speed = 6
      self.image = pg.transform.rotate(self.frames[self.image_num], self.orient)
      # print(self.orient)
    else:
      self.anima_speed -= 1
    
    # Move the spider
    if isHanging(self):
      if self.dir == LEFT:
        self.rect.x -= 1
      elif self.dir == RIGHT:
        self.rect.x += 1
      # print("hanging")

    elif isGripping_right(self):
      if self.dir == UP:
        self.rect.y -= 1
      if self.dir == DOWN:
        self.rect.y += 1
      # print("gripping right")
      
    elif isStanding(self):
      if self.dir == LEFT:
        self.rect.x -= 1
      elif self.dir == RIGHT:
        self.rect.x += 1
      # print("walking")

    elif isGripping_left(self):
      if self.dir == UP:
        self.rect.y -= 1
      if self.dir == DOWN:
        self.rect.y += 1
      # print("gripping left")

    else:
      # print("changing direction")
      if self.dir == LEFT:
        # print("rotating UP to 90")
        self.dir = UP
        self.orient = 90
        self.rect.y -= 1

      elif self.dir == UP:
        # print("rotating RIGHT to 0")
        self.dir = RIGHT
        self.orient = 0
        self.rect.x += 1

      elif self.dir == RIGHT:
        # print("rotating DOWN to 270")
        self.dir = DOWN
        self.orient = 270
        self.rect.y += 1

      elif self.dir == DOWN:
        # print("rotating RIGHT to 180")
        self.dir = LEFT
        self.orient = 180
        self.rect.x -= 1

class Acid(pg.sprite.Sprite):
  def __init__(self, x, y, w, h):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.Surface((w, h))
    self.image.fill(GREEN)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    
class Platform(pg.sprite.Sprite):
  def __init__(self, game, x, y):
    pg.sprite.Sprite.__init__(self)

    self.game = game
    images = [self.game.spritesheet.get_image(0, 288, 380, 94),
              # self.game.spritesheet.get_image(213, 1662, 201, 100)
    ]
    self.image = choice(images)
    self.image.set_colorkey(BLACK)
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
  
class Door1(pg.sprite.Sprite):
  def __init__(self, x, y, w, h):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.Surface((w, h))
    self.image.fill(RED)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y

class Door2(pg.sprite.Sprite):
  def __init__(self, x, y, w, h):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.Surface((w, h))
    self.image.fill(RED)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y

class Door3(pg.sprite.Sprite):
  def __init__(self, x, y, w, h):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.Surface((w, h))
    self.image.fill(RED)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y

class Key1(pg.sprite.Sprite):
  def __init__(self, x, y, w, h):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.Surface((w, h))
    self.image.fill(YELLOW)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
  
class Key2(pg.sprite.Sprite):
  def __init__(self, x, y, w, h):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.Surface((w, h))
    self.image.fill(YELLOW)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y

class Key3(pg.sprite.Sprite):
  def __init__(self, x, y, w, h):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.Surface((w, h))
    self.image.fill(YELLOW)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
