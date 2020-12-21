# Sprite classes for Metroidvania game
import pygame as pg
from settings import *
vec = pg.math.Vector2

from pygame.locals import (
  RLEACCEL,
  K_UP,
  K_DOWN,
  K_LEFT,
  K_RIGHT,
  K_SPACE,
  K_ESCAPE,
  KEYDOWN,
  QUIT,
)


class Player(pg.sprite.Sprite):
  def __init__(self, game):
    pg.sprite.Sprite.__init__(self)
    self.game = game
    self.image = pg.Surface((30, 40))
    self.image.fill(YELLOW)
    self.rect = self.image.get_rect()
    self.rect.center = (WIDTH/2, HEIGHT/2)
    self.pos = vec(WIDTH/2, HEIGHT/2 + 50)
    self.vel = vec(0, 0)
    self.acc = vec(0, 0)

  def jump(self):
    # only jump if standing on a platform
    # check the pixel below the player
    self.rect.y += 1
    # see if the player collides with a platform
    hits = pg.sprite.spritecollide(self, self.game.platforms, False)
    # move the player back to previous position
    self.rect.y -= 1
    if hits:
      self.vel.y = -15

  def update(self):
    self.acc = vec(0, PLAYER_GRAVITY)
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
      self.acc.x = -PLAYER_ACC
    if keys[pg.K_RIGHT]:
      self.acc.x = PLAYER_ACC
    # if keys[pg.K_UP]:
    #       self.acc.y = -PLAYER_ACC
    # if keys[pg.K_DOWN]:
    #   self.acc.y = PLAYER_ACC

    # Apply friction
    self.acc.x += self.vel.x * PLAYER_FRICTION
    # Equation of motion
    self.vel += self.acc
    self.pos += self.vel + 0.5 * self.acc

    # Position player in the center of the screen
    self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
  def __init__(self, x, y, w, h):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.Surface((w,h))
    self.image.fill(SILVER)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y