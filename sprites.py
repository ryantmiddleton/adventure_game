# Sprite classes for Metroidvania game
import pygame as pg
import math
from settings import *
from random import choice, randrange
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
    self.hasKey = False


    # Player Image and rectangle surface
    self.image = pg.transform.rotozoom(pg.image.load("imgs/idle outline.png").convert(),0,2)
    self.image.set_colorkey((255, 255, 255), RLEACCEL)
    self.rect = self.image.get_rect()
    self.rect.center = (WIDTH/2, HEIGHT/2)

    # Player coordinates and orientation
    self.pos = vec(WIDTH/2, HEIGHT/2)
    self.vel = vec(0, 0)
    self.acc = vec(0, 0)
    self.left = False
    self.level = 1

    self.health = PLAYER_HEALTH
    self.max_health = PLAYER_HEALTH

 

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
      self.jumping = True
      self.vel.y = -15
      self.game.jump_sound.play()

  def boss_jump(self):
    self.rect.y += 1
    hits = pg.sprite.spritecollide(self, self.game.platform_boss, False)
    self.rect.y -= 1
    if hits:  
      self.jumping = True
      self.vel.y = -15
      self.game.jump_sound.play()

  def ground_jump(self):
    self.rect.y += 1
    hits = pg.sprite.spritecollide(self, self.game.groundplatform, False)
    self.rect.y -= 1
    if hits:  
      self.jumping = True
      self.vel.y = -15
      self.game.jump_sound.play()

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
      self.rect.y = y-30
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
      self.rect.y = y-30
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

class Spider(pg.sprite.Sprite):
  def __init__(self, x, y, game):
    pg.sprite.Sprite.__init__(self)
    self.game = game
    self.spritesheet = self.game.spider_spritesheet
    self.size = self.spritesheet.image_sheet.get_size()
    self.frames = self.spritesheet.strip_from_sheet(self.spritesheet.image_sheet, (6,6), (8,6), (self.size[0]/12,self.size[1]/8))
    # Crop each selected image from the sheet and rotate, scale it
    for i in range(len(self.frames)):
      self.frames[i] = self.spritesheet.crop(self.frames[i],(10,20),(65,45))
      # self.frames[i] = pg.transform.flip(self.frames[i], True, False)
      self.frames[i] = pg.transform.rotozoom(self.frames[i], 0, 1)

    self.image_num = 0
    self.anima_speed = 6
    self.image = self.frames[self.image_num]

    #Initialize the spider position - self.rect.y = y, self.rect.x = x
    self.rect = self.image.get_rect(topleft=(x,y))
    # self.rect.y = y, self.rect.x = x
    # 0-right-facing/right, 90-up/legs right, 180-hanging/left, 270-down/leg left
    self.orient = 0
    self.dir = RIGHT

  def update(self):
    # Animate the spider's legs by cycling through each image
    if self.image_num < len(self.frames) and self.anima_speed == 0:
      self.image_num += 1
      if self.image_num == len(self.frames):
        self.image_num = 0
      self.anima_speed = 6
      self.image = pg.transform.rotate(self.frames[self.image_num], self.orient)
      self.image = self.image.convert_alpha()
      # print(self.orient)
    else:
      self.anima_speed -= 1
    
    # Check if spider is holding onto any platforms
    # cur_platform = pg.sprite.spritecollide(self, self.game.platforms, False)
    # if cur_platform:
    #   print(cur_platform[0].rect.x)
    #   print(cur_platform[0].rect.y)
    #   # Test if bottomright of spider is touching the platform
    #   if pg.Rect.collidepoint(cur_platform[0].rect, self.rect.bottomright):
    #     print("bottomright is touching: " + str(self.rect.bottomright))
    #   # Test if bottom left of spider is touching
    #   if pg.Rect.collidepoint(cur_platform[0].rect, self.rect.bottomleft):
    #     print("bottomleft is touching: " + str(self.rect.bottomleft))
    #   # Test if topright of Spider is touching the platform
    #   if pg.Rect.collidepoint(cur_platform[0].rect, self.rect.topright):
    #     print("topright is touching")
    #   # Test if topleft of spider is touching the platform
    #   if pg.Rect.collidepoint(cur_platform[0].rect, self.rect.topleft):
    #     print("topleft is touching")
    # else:
    #   # Fall 
    #   self.rect.y += 1
    
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
      self.rect.bottom -= 1
      hits = pg.sprite.spritecollide (self, self.game.platforms, False)
      self.rect.bottom += 1
      if hits:
        # print("isStanding")
        return True
      else:  
        return False

  def isHanging(self):
    self.rect.top += 1
    hits = pg.sprite.spritecollide (self, self.game.platforms, False)
    self.rect.top -= 1
    if hits:
      # print("hangin")
      # print(hits[0])
      # test_point = self.rect.bottomright
      # print(pg.Rect.collidepoint(hits[0].rect, test_point))
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
  def __init__(self, game, x, y):
    pg.sprite.Sprite.__init__(self)
    self.game = game
    self.image = self.game.platform_spritesheet.get_image(232, 1390, 95, 53)
    self.image.set_colorkey(BLACK)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    
class Platform(pg.sprite.Sprite):
  def __init__(self, spritesheet, x, y):

    pg.sprite.Sprite.__init__(self) 
    self.image = spritesheet.get_image(0, 288, 380, 94)
    self.image.set_colorkey(BLACK)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y

class Ground_Platform(pg.sprite.Sprite):
  def __init__(self, x, y, w, h):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.transform.rotozoom(pg.image.load("imgs/groundfloor.png").convert(),0,1)
    self.image.set_colorkey(BLACK)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y

    
class Platform_Boss(pg.sprite.Sprite):
  def __init__(self, spritesheet, x, y):
    pg.sprite.Sprite.__init__(self)
    self.image = spritesheet.get_image(0,96,380,94)
    self.image.set_colorkey(BLACK)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y   

class Spritesheet():
  def __init__(self, filename):
    self.image_sheet = pg.image.load(filename).convert_alpha()

  def get_image(self, x, y, width, height):
    image = pg.Surface((width, height))
    image.blit(self.image_sheet, (0,0), (x, y, width, height))
    image = pg.transform.scale(image, (width //2, height// 2))
    return image

  def strip_from_sheet(self, sheet, start, end, size):
    # Strips individual frames from a sprite sheet image given a start location,
    # sprite size, and number of columns and rows.
    frames = []
    for y in range(start[1],end[1]+1):
        for x in range(start[0],end[0]+1):
            location = (size[0]*x, size[1]*y)
            frames.append(sheet.subsurface(pg.Rect(location, size)))
    return frames

  def crop(self, image, start_pos, new_size):
    old_size = image.get_size()
    # start_pos = (old_size[0]-new_size[0], old_size[1]-new_size[1])
    cropped_image = pg.Surface(new_size, pg.SRCALPHA, 32)
    cropped_image.blit(image, (0,0), (start_pos[0], start_pos[1], old_size[0], old_size[1]))
    return cropped_image

class Door(pg.sprite.Sprite):
  def __init__(self, x, y, w, h):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.transform.rotozoom(pg.image.load("imgs/door.png").convert(),0,1)
    self.image.set_colorkey((255, 255, 255), RLEACCEL)
    self.rect = self.image.get_rect()
    self.rect.center = (WIDTH/2, HEIGHT/2)
    self.rect.x = x
    self.rect.y = y

class Key(pg.sprite.Sprite):
  def __init__(self, x, y, w, h):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.transform.rotozoom(pg.image.load("imgs/keyYellow.png").convert(),0,1)
    self.image.set_colorkey((255, 255, 255), RLEACCEL)
    self.rect = self.image.get_rect()
    self.rect.center = (WIDTH/2, HEIGHT/2)
    self.rect.x = x
    self.rect.y = y

class Boss(pg.sprite.Sprite):
  def __init__(self, game, x, y, w, h):
    pg.sprite.Sprite.__init__(self)
    self.game = game
    self.image = pg.transform.rotozoom(pg.image.load("imgs/boss.png").convert(),0,1)
    self.image.set_colorkey((255, 255, 255), RLEACCEL)
    self.rect = self.image.get_rect()
    self.rect.center = (WIDTH/2, HEIGHT/2)
    self.rect.x = x
    self.rect.y = y
    self.health = BOSS_HEALTH
    self.max_health = BOSS_HEALTH
    self.deadboss = False

class Heart(pg.sprite.Sprite):
  def __init__(self, game, x, y, w, h):
    pg.sprite.Sprite.__init__(self)
    self.game = game
    self.image = pg.transform.rotozoom(pg.image.load("imgs/heart.png").convert(),0,1)
    self.image.set_colorkey((255, 255, 255), RLEACCEL)
    self.rect = self.image.get_rect()
    self.rect.center = (WIDTH/2, HEIGHT/2)
    self.rect.x = x
    self.rect.y = y

class Explosion(pg.sprite.Sprite):
    def __init__(self, x, y, game):
      pg.sprite.Sprite.__init__(self)
      self.game = game
      self.spritesheet = self.game.explosion_spritesheet
      self.size = self.spritesheet.image_sheet.get_size()
      self.frames = self.spritesheet.strip_from_sheet(self.spritesheet.image_sheet , (0,0), (7,4), (self.size[0]/8,self.size[1]/8))
      # print("num pics = " + str(len(self.frames)))
      self.image = self.frames[0]
      self.rect = self.image.get_rect(topleft=(x,y))
      self.image_num = 0

    def update(self):
      # Animate the explosion by cycling through each image
      if self.image_num < len(self.frames)-1: 
        self.image_num += 1
        # print(self.image_num)
        self.image = self.frames[self.image_num]
      else:
        self.kill()

class Bat(pg.sprite.Sprite):
  def __init__(self, game):
    pg.sprite.Sprite.__init__(self)
    self.vel = vec(0, 0)
    self.game = game

    self.image_up = pg.image.load("imgs/bat-up.jpg")
    self.image_up = self.image_up.convert_alpha()
    self.image_up.set_colorkey(BLACK)
    self.image_mid = pg.image.load("imgs/bat-mid.jpg")
    self.image_mid = self.image_mid.convert_alpha()
    self.image_mid.set_colorkey(BLACK)
    self.image_down = pg.image.load("imgs/bat-down.jpg")
    self.image_down = self.image_down.convert_alpha()
    self.image_down.set_colorkey(BLACK)
    self.image = self.image_up
    
    self.rect = self.image.get_rect()
    # Randomly choose starting left or right
    self.rect.centerx = choice([-100, WIDTH + 100])
    # Randomly choose speed
    self.vel.x = randrange(1, 4)
    if self.rect.centerx > WIDTH:
      self.vel.x *= -1
    # Randomly spawn in top half of screen
    self.rect.y = randrange(HEIGHT / 2)
    self.vel.y = 0
    self.dy = 0.5

  def update(self):
    self.rect.x += self.vel.x
    self.vel.y += self.dy
    if self.vel.y > 3 or self.vel.y <-3:
      self.dy *= -1
    center = self.rect.center
    if self.dy < 0:
      self.image = self.image_up
    else:
      self.image = self.image_down
    self.rect = self.image.get_rect()
    self.rect.center = center
    self.rect.y += self.vel.y
    if self.rect.left > WIDTH + 100 or self.rect.right < -100:
      self.kill() 

class Coin(pg.sprite.Sprite):
  def __init__(self, spritesheet, x, y):
    pg.sprite.Sprite.__init__(self)
    self.image = spritesheet.get_image(244,1981,61,61)    
    self.image.set_colorkey(BLACK)
    self.rect = self.image.get_rect()
    self.rect.center = (WIDTH/2, HEIGHT/2)
    self.rect.x = x
    self.rect.y = y

class Small_Boss(pg.sprite.Sprite):
  def __init__(self, game, x, y, w, h):
    pg.sprite.Sprite.__init__(self)
    self.game = game
    self.image = pg.transform.rotozoom(pg.image.load("imgs/small_boss.png").convert(),0,1)
    self.image.set_colorkey((255, 255, 255), RLEACCEL)
    self.rect = self.image.get_rect()
    self.rect.center = (WIDTH/2, HEIGHT/2)
    self.rect.x = x
    self.rect.y = y
    self.rect.y = randrange(HEIGHT)
    self.rect.x = randrange(WIDTH)