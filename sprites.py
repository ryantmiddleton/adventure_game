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

class Acid(pg.sprite.Sprite):
  def __init__(self, x, y, w, h):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.Surface((w, h))
    self.image.fill(GREEN)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y

