# Sprite classes for Metroidvania game
import pygame as pg
import math
from settings import *
import random
from os import path

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


class Player(pg.sprite.Sprite):
  def __init__(self, game):
    pg.sprite.Sprite.__init__(self)
    self.game = game
    self.jumping = False

    # Player Image and rectangle surface
    self.image = pg.transform.rotozoom(pg.image.load("imgs/idle outline.png").convert(),0,2)
    self.image.set_colorkey((255, 255, 255), RLEACCEL)
    self.rect = self.image.get_rect()
    self.rect.center = (WIDTH/2, HEIGHT/2)

    # Player coordinates and orientation
    self.pos = vec(0, HEIGHT-40)
    self.vel = vec(0, 0)
    self.acc = vec(0, 0)
    self.left = False
    self.level = 3

    self.health = PLAYER_HEALTH
    self.max_health = PLAYER_HEALTH

 # def jump(self):
  #   self.rect.y += 1
  #   hits = pg.sprite.spritecollide(self, self.game.platforms, False)
  #   self.rect.y -= 1
  #   if hits and not self.jumping:  
  #     self.jumping = True
  #     self.vel.y = -PLAYER_JUMP
  #     self.game.jump_sound.play()

  def update(self):
    self.acc = vec(0, PLAYER_GRAV)
    keys = pg.key.get_pressed()

    # update to left running player image
    if keys[K_LEFT]:
      self.image = pg.transform.rotozoom(pg.image.load("imgs/left_run.png").convert(), 0, 2)
      self.image.set_colorkey((255, 255, 255), RLEACCEL)
      self.acc.x = -PLAYER_ACC
      self.left = True

    #update to right running player image 
    if keys[K_RIGHT]:
      self.image = pg.transform.rotozoom(pg.image.load("imgs/run_right.png").convert(), 0, 2)
      self.image.set_colorkey((255, 255, 255), RLEACCEL)
      self.acc.x = PLAYER_ACC
      self.left = False

    # update to jumping player image
    if keys[K_UP]:
      self.image = pg.transform.rotozoom(pg.image.load("imgs/jump outline.png").convert(), 0, 2)
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
  
  def jump_cut(self):
    if self.jumping:
      if self.vel.y < -3:
        self.vel.y = -3

  def jump(self):
    self.rect.y += 1
    hits = pg.sprite.spritecollide(self, self.game.platforms, False)
    self.rect.y -= 1
    if hits:  
      self.vel.y = -PLAYER_JUMP

  def isStanding(self):
    self.rect.y += 1
    hits = pg.sprite.spritecollide (self, self.game.platforms, False)
    self.rect.y -= 1
    if hits:
      return True
    else:  
      return False
 

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
    self.spider_sheet = Spritesheet(SPIDER_SPRITESHEET)
    self.size = self.spider_sheet.image_page.get_size()
    self.frames = self.spider_sheet.strip_from_sheet(self.spider_sheet.image_page, (6,6), (8,6), (self.size[0]/12,self.size[1]/8))
    # Crop each selected image from the sheet and rotate, scale it
    for i in range(len(self.frames)):
      self.frames[i] = self.spider_sheet.crop(self.frames[i],(10,20),(65,45))
      # self.frames[i] = pg.transform.flip(self.frames[i], True, False)
      self.frames[i] = pg.transform.rotozoom(self.frames[i], 0, 1)

    self.image_num = 0
    self.anima_speed = 6
    self.image = self.frames[self.image_num]

    #Initialize the spider position - self.rect.y = y, self.rect.x = x
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
    if self.isHanging():
      if self.dir == LEFT:
        self.rect.x -= 1
      elif self.dir == RIGHT:
        self.rect.x += 1
      # print("hanging")

    elif self.isGripping_right():
      if self.dir == UP:
        self.rect.y -= 1
      if self.dir == DOWN:
        self.rect.y += 1
      # print("gripping right")
      
    elif self.isStanding():
      if self.dir == LEFT:
        self.rect.x -= 1
      elif self.dir == RIGHT:
        self.rect.x += 1
      # print("walking")

    elif self.isGripping_left():
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
  
  def isStanding(self):
      self.rect.y += 1
      hits = pg.sprite.spritecollide (self, self.game.platforms, False)
      self.rect.y -= 1
      if hits:
        return True
      else:  
        return False

  def isHanging(self):
    self.rect.y -= 1
    hits = pg.sprite.spritecollide (self, self.game.platforms, False)
    self.rect.y += 1
    if hits:
      return True
    else:  
      return False

  def isGripping_right(self):
    self.rect.x += 1
    hits = pg.sprite.spritecollide (self, self.game.platforms, False)
    self.rect.x -= 1
    if hits:
      return True
    else:  
      return False
    
  def isGripping_left(self):
    self.rect.x -= 1
    hits = pg.sprite.spritecollide (self, self.game.platforms, False)
    self.rect.x += 1
    if hits:
      return True
    else:  
      return False

class Acid(pg.sprite.Sprite):
  def __init__(self, x, y, w, h):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.Surface((w, h))
    self.image.fill(GREEN)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    
class Platform(pg.sprite.Sprite):
  def __init__(self, x, y, w, h):
    pg.sprite.Sprite.__init__(self)
    # self.spritesheet = Spritesheet(PLATFORM_SPRITESHEET)
    # images = [
    #   self.spritesheet.get_image(0, 288, w, h),
    # ]
    # self.image = random.choice(images)
    # self.image.set_colorkey(BLACK)
    self.image = pg.Surface((w, h))
    self.image.fill(SILVER)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y   

class Spritesheet:
  def __init__(self, strFilename):
    self.dir = path.dirname(__file__)
    self.img_dir = path.join(self.dir, 'imgs')
    filename = path.join(self.img_dir, strFilename)
    self.image_page = pg.image.load(filename).convert()

  def get_image(self, x, y, width, height):
    image = pg.Surface((width, height))
    image.blit(self.image_page, (0,0), (x, y, width, height))
    image = pg.transform.scale(image, (width //2, height// 2))
    return image

  def strip_from_sheet(self, sheet, start, end, size):
    # Strips individual frames from a sprite sheet image given a start location,
    # sprite size, and number of columns and rows.
    frames = []
    for x in range(start[0],end[0]+1):
        for y in range(start[1],end[1]+1):
            location = (size[0]*x, size[1]*y)
            frames.append(sheet.subsurface(pg.Rect(location, size)))
    return frames

  def crop(self, image, start_pos, new_size):
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
