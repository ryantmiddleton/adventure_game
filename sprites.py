# Sprite classes for Metroidvania game
import pygame as pg
import math
from settings import *
import settings
from random import choice, randrange, randint
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
    self.frames = game.idle_images
    self.frames_left = game.idle_images_left    
    self.run_frames = game.run_images
    self.run_frames_left = game.run_images_left
    self.image = self.frames[0]
    # self.image = pg.transform.rotozoom(pg.image.load("imgs/idle outline.png").convert_alpha(),0,2)
    # self.image.set_colorkey((255, 255, 255), RLEACCEL)
    self.rect = self.image.get_rect()
    self.rect.center = (WIDTH/2, HEIGHT/2)

    # Player coordinates and orientation
    self.pos = vec(WIDTH/2, HEIGHT/2)
    self.vel = vec(0, 0)
    self.acc = vec(0, 0)
    self.left = False
    self.level = 3

    self.health = PLAYER_HEALTH
    self.max_health = PLAYER_HEALTH

    self.image_num = 0
    self.run_num = 0
    self.anima_speed = 3
    self.image = self.frames[self.image_num]
    self.orient = 0
 

  def update(self):
    self.acc = vec(0, PLAYER_GRAV)
    keys = pg.key.get_pressed()

    # update to left running player image
    if keys[K_LEFT]:
      # self.image = pg.transform.rotozoom(pg.image.load("imgs/left_run.png").convert_alpha(), 0, 2)
      # self.image = self.run_frames_left[self.run_num]
      # self.image.set_colorkey((255, 255, 255), RLEACCEL)
      self.acc.x = -PLAYER_ACC
      self.left = True

    #Run left animation
      if self.run_num < len(self.run_frames_left) and self.anima_speed == 0:
        self.run_num += 1
        if self.run_num == len(self.run_frames_left):
          self.run_num = 0
        self.anima_speed = 2
        self.image = self.run_frames_left[self.run_num]
      else:
        self.anima_speed -= 1

    #update to right running player image 
    if keys[K_RIGHT]:
      # self.image = pg.transform.rotozoom(pg.image.load("imgs/run_right.png").convert_alpha(), 0, 2)
      # self.image = self.run_frames[self.run_num]
      # self.image.set_colorkey((255, 255, 255), RLEACCEL)
      self.acc.x = PLAYER_ACC
      self.left = False

      #Run right animation
      if self.run_num < len(self.run_frames) and self.anima_speed == 0:
        self.run_num += 1
        if self.run_num == len(self.run_frames):
          self.run_num = 0
        self.anima_speed = 2
        self.image = self.run_frames[self.run_num]
      else:
        self.anima_speed -= 1

    # update to jumping player image
    if keys[K_UP]:
      if self.left == False:
        self.image = pg.transform.rotozoom(pg.transform.flip(pg.image.load("imgs/jump outline.png"), True, False).convert_alpha(), 0, 2)
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
      else:  
        self.image = pg.transform.rotozoom(pg.image.load("imgs/jump outline.png").convert_alpha(), 0, 2)
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

    #Idle animimation
    if self.left == True:
      if self.vel.x >= -4 and self.vel.y >= -1 and self.vel.y <=1:
        if self.image_num < len(self.frames_left) and self.anima_speed == 0:
          self.image_num += 1
          if self.image_num == len(self.frames_left):
            self.image_num = 0
          self.anima_speed = 3
          self.image = pg.transform.rotate(self.frames_left[self.image_num], self.orient)
          self.image.set_colorkey(WHITE, RLEACCEL)
        else:
          self.anima_speed -= 1
    else:
      if self.vel.x <= 4 and self.vel.y >= -1 and self.vel.y <=1:
        if self.image_num < len(self.frames) and self.anima_speed == 0:
          self.image_num += 1
          if self.image_num == len(self.frames):
            self.image_num = 0
          self.anima_speed = 3
          self.image = pg.transform.rotate(self.frames[self.image_num], self.orient)
        else:
          self.anima_speed -= 1
  
    
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
    #Shoot Up
    if facing == 2:
      self.image = pg.transform.rotate(pg.image.load("img/bullet.png"), 90).convert()
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y-80
    #Shoot Down
    elif facing == -2:
      self.image = pg.transform.rotate(pg.image.load("img/bullet.png"), 270).convert()
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y
    #Shoot Left  
    elif facing == -1:
      self.image = pg.transform.flip(pg.image.load("img/bullet.png"), 180, 0).convert()
      self.rect = self.image.get_rect()
      self.rect.x = x-40
      self.rect.y = y-30
    #Shoot Shoot Up Right
    elif facing == 3:
      self.image = pg.transform.rotate(pg.image.load("img/bullet.png"), 45).convert()
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y-50
    #Shoot Up Left
    elif facing == -3:
      self.image = pg.transform.rotate(pg.image.load("img/bullet.png"), 135).convert()
      self.rect = self.image.get_rect()
      self.rect.x = x-20
      self.rect.y = y-50
    #Shoot Down Right
    elif facing == 4:
      self.image = pg.transform.rotate(pg.image.load("img/bullet.png"), 315).convert()
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y-50
    #Shoot Down left
    elif facing == -4:
      self.image = pg.transform.rotate(pg.image.load("img/bullet.png"), 225).convert()
      self.rect = self.image.get_rect()
      self.rect.x = x-20
      self.rect.y = y-50
    #Shoot Right
    else:
      self.image = pg.image.load("img/bullet.png").convert()
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y-30
    self.image.set_colorkey((BLACK), RLEACCEL)

  def update(self):
    if self.facing == 3:
      self.rect.y -= 20
      self.rect.x += 20
    elif self.facing == -3:
      self.rect.y -= 20
      self.rect.x -= 20
    elif self.facing == 2:
      self.rect.y -= 20
    elif self.facing == -2:
      self.rect.y += 20
    elif self.facing == 4:
      self.rect.y += 20
      self.rect.x += 20
    elif self.facing == -4:
      self.rect.y += 20
      self.rect.x -= 20
    else:
      self.rect.x += (20*self.facing)
    if self.rect.left > WIDTH: 
      self.kill()
    elif self.rect.right < 0:
      self.kill()

class Spider(pg.sprite.Sprite):
  def __init__(self, x, y, game):
    pg.sprite.Sprite.__init__(self)
    self.game = game

    # Initilaize random start
    rand_num = randint(1,10)
    if rand_num <= 5:
      self.frames = self.game.spider_left_images
      self.dir = LEFT
    else:
      self.frames = self.game.spider_right_images
      self.dir = RIGHT

    self.vel = 1
    self.image_num = 0
    self.anima_speed = 6
    self.image = self.frames[self.image_num]

    #Initialize the spider position - self.rect.y = y, self.rect.x = x
    self.rect = self.image.get_rect(topleft=(x,y))
    self.orient = 0

  def update(self):
    # Check if spider is holding onto any platforms
    collided_platforms = pg.sprite.spritecollide(self, self.game.platforms, False)
    if collided_platforms:
      # print("platform topleft: " + str(collided_platforms[0].rect.topleft))
      # print("platform bottomleft: " + str(collided_platforms[0].rect.bottomleft))
      # print(self.rect.bottom)

      contact_points = {
        "BL": False,
        "BR": False,
        "TL": False,
        "TR": False,
        "MT": False,
        "MB": False,
        "ML": False,
        "MR": False
      }
      # Loop through each platform the spider is touching
      # And see which points of the spider are touching
      for platform in collided_platforms:
        # print("platform bottomright: " + str(platform.rect.bottomright))
        # print("platform topleft: " + str(platform.rect.topleft))
        # If Spider is falling and has collided with a platform
        if self.vel > 1 and self.rect.bottom > platform.rect.top + 1:
          self.rect.bottom = platform.rect.top + 1
          if self.dir == LEFT:
            self.frames = self.game.spider_left_images
          else:
            self.frames = self.game.spider_right_images
          self.image = pg.transform.rotate(self.frames[0], 0)
          # print("spider bottom: " + str(self.rect.bottom))
          self.vel = 1
        # Test if bottomright of spider is touching any platforms
        if pg.Rect.collidepoint(platform.rect, self.rect.bottomright):
          # print("bottomright is touching: " + str(self.rect.bottomright))
          contact_points["BR"] = True
        # Test if bottom left of spider is touching any platforms
        if pg.Rect.collidepoint(platform.rect, self.rect.bottomleft):
          # print("bottomleft is touching: " + str(self.rect.bottomleft))
          contact_points["BL"] = True
        # Test if topright of spider is touching any platforms
        if pg.Rect.collidepoint(platform.rect, self.rect.topright):
          # print("topright is touching: " + str(self.rect.topright))
          contact_points["TR"] = True
        # Test if topleft of spider is touching any platforms
        if pg.Rect.collidepoint(platform.rect, self.rect.topleft):
          # print("topleft is touching: " + str(self.rect.topleft))
          contact_points["TL"] = True
        # Test if midtop of spider is touching any platforms
        if pg.Rect.collidepoint(platform.rect, self.rect.midtop):
          # print("midtop is touching: " + str(self.rect.midtop))
          contact_points["MT"] = True
        # Test if midbottom of spider is touching any platforms
        if pg.Rect.collidepoint(platform.rect, self.rect.midbottom):
          # print("midbottom is touching: " + str(self.rect.midbottom))
          contact_points["MB"] = True
        # Test if midleft of spider is touching any platforms
        if pg.Rect.collidepoint(platform.rect, self.rect.midleft):
          # print("midleft is touching: " + str(self.rect.midleft))
          contact_points["ML"] = True
        # Test if midright of spider is touching any platforms
        if pg.Rect.collidepoint(platform.rect, self.rect.midright):
          # print("midright is touching: " + str(self.rect.midright))
          contact_points["MR"] = True

        # Advance the spider based on orientation
        if self.isHanging(contact_points):
          self.orient = 180
          # If Spider is above player check if spider wants to drop
          if self.game.player.rect.y > self.rect.y:
            # Drop off the platform
            rand_num = randint(1,5000)
            if rand_num <= 5:
              # print(rand_num)
              self.rect.top += 1
              self.orient = 0
          # Move the Spider based on current direction
          if self.dir == LEFT:
            self.frames = self.game.spider_right_images
            self.rect.x -= 1
            # print("hanging left")
          elif self.dir == RIGHT:
            self.frames = self.game.spider_left_images
            self.rect.x += 1
            # print("hangin right")
          # If Spider has reached the edge of the platform decide if it wants to switch direction
          if self.rect.topright[0] == platform.rect.bottomright[0] or self.rect.topleft[0] == platform.rect.bottomleft[0]:
            if randint(1,10) <= 5:
              if self.dir == RIGHT:
                self.frames = self.game.spider_left_images
                # print("switching left")
                self.dir = LEFT
            else:
              if self.dir == LEFT:
                self.frames = self.game.spider_right_images
                # print ("switching right")
                self.dir = RIGHT

        elif self.isWalking(contact_points):
          self.orient = 0
          if self.dir == LEFT:
            self.frames = self.game.spider_left_images
            self.rect.x -= 1
            # print("walking left")
          elif self.dir == RIGHT:
            self.frames = self.game.spider_right_images
            self.rect.x += 1
            # print("walking right")
          # If Spider has reached the edge of the platform decide if it wants to switch direction
          if self.rect.bottomright[0] == platform.rect.topright[0] or self.rect.bottomleft[0] == platform.rect.topleft[0]:
            if randint(1,10) <= 5:
              self.frames = self.game.spider_left_images
              self.dir = LEFT
            else:
              self.frames = self.game.spider_right_images
              self.dir = RIGHT

        elif self.isGripping_right(contact_points):
          self.orient = 90
          if self.dir == UP:
            self.frames = self.game.spider_right_images
            self.rect.y -= 1
            # print("gripping right UP")
          if self.dir == DOWN:
            self.frames = self.game.spider_left_images
            self.rect.y += 1
            # print("gripping right DOWN")

        elif self.isGripping_left(contact_points):
          self.orient = 270
          if self.dir == UP:
            self.frames = self.game.spider_left_images
            self.rect.y -= 1
            # print("gripping left UP")
          if self.dir == DOWN:
            self.frames = self.game.spider_right_images
            self.rect.y += 1
            # print("gripping left DOWN")

        else:
          if self.dir == LEFT:
            # print("spider topmiddle coords: " + str(self.rect.midtop))
            # print("spider bottommiddle coords: " + str(self.rect.midbottom))
            if contact_points["MB"] or contact_points["MT"]:
              self.rect.x -= 1
            elif contact_points["TR"]:
              # print("rotating UP to 90")
              self.orient = 90
              self.rect.midright = platform.rect.bottomleft
              self.rect.right += 1
              self.dir = UP
              self.frames = self.game.spider_right_images
              # print("spider middleright coords: " + str(self.rect.midright))
            elif contact_points["BR"]:
              # print("rotating DOWN to 90")
              self.orient = 90
              self.rect.midright = platform.rect.topleft
              self.rect.right += 1
              self.dir = DOWN
              self.frames = self.game.spider_left_images
            else:
              self.rect.x -= 1

          elif self.dir == UP:
            # print("spider middleleft coords: " + str(self.rect.midleft))
            # print("spider middleright coords: " + str(self.rect.midright))
            if contact_points["ML"] or contact_points["MR"]:
              self.rect.y -= 1
            elif contact_points["BR"]:
              # print("rotating RIGHT to 0")
              self.orient = 0
              self.rect.midbottom = platform.rect.topleft
              self.rect.bottom += 1
              self.dir = RIGHT
              self.frames = self.game.spider_right_images
              # print("spider midbottom coords: " + str(self.rect.midbottom))
            elif contact_points["BL"]:
              # print("rotating LEFT to 0")
              self.orient = 0
              self.rect.midbottom = platform.rect.topright
              self.rect.bottom += 1
              self.dir = LEFT
              self.frames = self.game.spider_left_images
              # print("spider midbottom coords: " + str(self.rect.midbottom))
            else:
              self.rect.y -= 1

          elif self.dir == RIGHT:
            if contact_points["MB"] or contact_points["MT"]:
              self.rect.x += 1
            elif contact_points["BL"]:
              # print("rotating DOWN to 270")
              self.orient = 270
              # adjust the position 
              self.rect.midleft = platform.rect.topright
              self.rect.left -= 1
              self.dir = DOWN
              self.frames = self.game.spider_right_images
              # print("spider midleft coords: " + str(self.rect.midleft))
            elif contact_points["TL"]:
              # print("rotating UP to 270")
              self.orient = 270
              # adjust the position 
              self.rect.midleft = platform.rect.bottomright
              self.rect.left -= 1
              self.dir = UP
              self.frames = self.game.spider_left_images
              # print("spider midleft coords: " + str(self.rect.midleft))
            else:
              self.rect.x += 1

          elif self.dir == DOWN:
            # print("spider midright coords: " + str(self.rect.midright))
            if contact_points["ML"] or contact_points["MR"]:
              self.rect.y += 1
            elif contact_points["TL"]:
              # print("rotating RIGHT to 180")
              self.orient = 180
              # adjust the x position of the spider to accomodate for the rest of the body
              self.rect.midtop = platform.rect.bottomright
              self.rect.top -= 1
              self.dir = LEFT
              self.frames = self.game.spider_right_images
              # print("spider midtop coords: " + str(self.rect.midtop))
            elif contact_points["TR"]:
              # print("rotating LEFT to 180")
              self.orient = 180
              # adjust the x position of the spider to accomodate for the rest of the body
              self.rect.midtop = platform.rect.bottomleft
              self.rect.top -= 1
              self.dir = RIGHT
              self.frames = self.game.spider_left_images
              # print("spider midtop coords: " + str(self.rect.midtop))
            else:
              self.rect.y += 1   
            
    else:
      # Fall 
      # print("Falling")
      self.vel += self.vel/9.8
      self.rect.y += self.vel
      self.orient = 0
      rand_num = randint(1,10)
      self.frames = self.game.spider_drop_images
      # if rand_num <= 5:
      #   self.frames = self.game.spider_left_images
      #   self.dir = LEFT
      # else:
      #   self.frames = self.game.spider_right_images
      #   self.dir = RIGHT
  
    # Animate the spider's legs by cycling through each image
    if self.image_num < len(self.frames) and self.anima_speed == 0:
      self.image_num += 1
      if self.image_num == len(self.frames):
        self.image_num = 0
      self.anima_speed = 6
      self.image = pg.transform.rotate(self.frames[self.image_num], self.orient)
    else:
      self.anima_speed -= 1

  def isWalking(self, points):
    return points["BL"] and points["BR"]  and (points["TL"] == False and points["TR"] == False)

  def isHanging(self, points):
    return points["TL"] and points["TR"]  and (points["BL"] == False and points["BR"] == False)

  def isGripping_right(self, points):
    return points["TR"] and points["BR"]  and (points["BL"] == False and points["TL"] == False)
    
  def isGripping_left(self, points):
    return points["TL"] and points["BL"]  and (points["TR"] == False and points["BR"] == False)

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
    self.image = pg.image.load("imgs/groundfloor.png").convert_alpha()
    self.image = pg.transform.scale(self.image, (w, h))
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
            # sprite_img = pg.Surface.copy(sheet.subsurface(pg.Rect(location, size)))
            # frames.append(sprite_img)
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
    self.image = pg.transform.rotozoom(pg.image.load("imgs/door.png").convert_alpha(),0,1)
    self.image.set_colorkey((255, 255, 255), RLEACCEL)
    self.rect = self.image.get_rect()
    self.rect.center = (WIDTH/2, HEIGHT/2)
    self.rect.x = x
    self.rect.y = y

class Key(pg.sprite.Sprite):
  def __init__(self, x, y, w, h):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.transform.rotozoom(pg.image.load("imgs/keyYellow.png").convert_alpha(),0,1)
    self.image.set_colorkey((255, 255, 255), RLEACCEL)
    self.rect = self.image.get_rect()
    self.rect.center = (WIDTH/2, HEIGHT/2)
    self.rect.x = x
    self.rect.y = y

class Heart(pg.sprite.Sprite):
  def __init__(self, game, x, y, w, h):
    pg.sprite.Sprite.__init__(self)
    self.game = game
    self.image = pg.transform.rotozoom(pg.image.load("imgs/heart.png").convert_alpha(),0,1)
    self.image.set_colorkey((255, 255, 255), RLEACCEL)
    self.rect = self.image.get_rect()
    self.rect.center = (WIDTH/2, HEIGHT/2)
    self.rect.x = x
    self.rect.y = y
    
class Explosion(pg.sprite.Sprite):
    def __init__(self, x, y, game):
      pg.sprite.Sprite.__init__(self)
      self.game = game
      self.frames = game.explosion_images
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

class Boss(pg.sprite.Sprite):
  def __init__(self, game):
    pg.sprite.Sprite.__init__(self)
    self.game = game
    self.vel = vec(0, 0)
    self.left_image = pg.transform.rotozoom(pg.image.load("imgs/boss.png").convert_alpha(),0,1)
    self.right_image = pg.transform.rotozoom(pg.image.load("imgs/boss_left.png").convert_alpha(),0,1)
    self.image = self.left_image
    self.image.set_colorkey((255, 255, 255), RLEACCEL)
    self.rect = self.image.get_rect()
    self.health = BOSS_HEALTH
    self.max_health = BOSS_HEALTH
    self.deadboss = False
    self.rect.centerx = choice([-100, WIDTH + 100])
    self.vel.x = randrange(3, 4)
    if self.rect.centerx > WIDTH:
      self.vel.x *= -1
    self.rect.y = randrange(HEIGHT - 200)
    self.vel.y = 0
    self.dy = 0.5

  def update(self):
    self.rect.x += self.vel.x
    self.vel.y += self.dy
    if self.vel.y > 3 or self.vel.y <-3:
      self.dy *= -1
    center = self.rect.center
    if self.dy < 0:
      if self.vel.x < 0:
        self.image = self.right_image
      else:
        self.image = self.left_image
    else:
      if self.vel.x < 0:
        self.image = self.right_image
      else:
        self.image = self.left_image
    self.rect = self.image.get_rect()
    self.rect.center = center
    self.rect.y += self.vel.y
    if self.rect.left > WIDTH + 100 or self.rect.right < -100:
      # Randomly choose starting left or right
      self.rect.centerx = choice([-100, WIDTH + 100])
      # Randomly choose speed
      self.vel.x = randrange(5, 6)
      if self.rect.centerx > WIDTH:
        self.vel.x *= -1
      # Randomly spawn in top half of screen
      self.rect.y = randrange(HEIGHT / 2)
      self.vel.y = 0
      self.dy = 0.5
      
class Bat(pg.sprite.Sprite):
  def __init__(self, game):
    pg.sprite.Sprite.__init__(self)
    self.vel = vec(0, 0)
    self.game = game

    scale_size = 2
    # Load and Scale the up_left image
    self.image_up_left = pg.image.load("imgs/bat-up.png")
    self.image_up_left = pg.transform.rotozoom(self.image_up_left, 0, scale_size)
    self.image_up_left = self.image_up_left.convert_alpha()

    # Scale the down_left image
    self.image_down_left = pg.image.load("imgs/bat-down.png")
    self.image_down_left = pg.transform.rotozoom(self.image_down_left, 0, scale_size)
    self.image_down_left = self.image_down_left.convert_alpha()

    self.image_up_right = pg.transform.flip(self.image_up_left, True, False)
    self.image_down_right = pg.transform.flip(self.image_down_left, True, False)
    self.image = self.image_up_right
    
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
      if self.vel.x < 0:
        self.image = self.image_up_right
      else:
        self.image = self.image_up_left
    else:
      if self.vel.x < 0:
        self.image = self.image_down_right
      else:
        self.image = self.image_down_left
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
    self.image = pg.transform.rotozoom(pg.image.load("imgs/small_boss.png").convert_alpha(),0,1)
    self.image.set_colorkey((255, 255, 255), RLEACCEL)
    self.rect = self.image.get_rect()
    self.rect.center = (WIDTH/2, HEIGHT/2)
    self.rect.x = x
    self.rect.y = y
    self.rect.y = randrange(HEIGHT)
    self.rect.x = randrange(WIDTH)