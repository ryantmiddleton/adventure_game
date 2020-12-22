import pygame as pg
import random
from settings import *
from sprites import *

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

class Game:
  def __init__(self):
    # Initialize Game
    pg.mixer.init()
    pg.init()
    self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption(TITLE)
    self.clock = pg.time.Clock()
    self.running = True

  def new(self):
    # start a new game
    self.all_sprites = pg.sprite.Group()
    self.platforms = pg.sprite.Group()
    self.bullets = pg.sprite.Group()
    self.player = Player(self)
    self.all_sprites.add(self.player)
    for plat in MAP1_PLATFORM_LIST:
      p = Platform(*plat)
      self.all_sprites.add(p)
      self.platforms.add(p)
    self.run()
    

  def run(self):
    # Game loop
    self.playing = True
    while self.playing:
      self.clock.tick(FPS)
      self.events()
      self.update()
      self.draw()

  def update(self):
    # Game Loop - Update
    self.all_sprites.update()
    # platform detection if falling
    if self.player.vel.y > 0:
      hits = pg.sprite.spritecollide(self.player, self.platforms, False)
      if hits:
        self.player.pos.y = hits[0].rect.top
        self.player.vel.y = 0

  def events(self):
    # Game Loop - events
    keys = pg.key.get_pressed()
    for event in pg.event.get():
      # check for closing window
      if event.type == pg.QUIT:
        if self.playing:
          self.playing = False
        self.running = False
      if self.player.health == 0:
        self.playing = False
      
      if event.type == pg.KEYDOWN:
        if event.key == pg.K_UP:
          self.player.jump()

        if event.key == pg.K_SPACE:
          if keys[pg.K_d] and keys[pg.K_w]:
            facing = 3
          elif keys[pg.K_a] and keys[pg.K_w]:
            facing = -3
          elif keys[pg.K_w]:
            facing = 2
          elif keys[pg.K_d]:
            facing = 1
          elif self.player.left or keys[pg.K_a]:
            facing = -1        
          else:
            facing = 1
          b = Bullet(self.player.pos.x, self.player.pos.y, facing)
          self.all_sprites.add(b)
          self.bullets.add(b)

        



  def draw(self):
    #Game Loop - draw 
    self.screen.fill(BLACK)
    self.all_sprites.draw(self.screen)
    pg.draw.rect(self.screen, RED, (20, 20, (self.player.max_health*20), 5))
    pg.draw.rect(self.screen, GREEN, (20, 20, (self.player.health*20), 5))

    pg.display.flip()


  def show_start_screen(self):
    # game splash/start screen
    pass

  def show_go_screen(self):
    #game over/continue
    pass

    

g = Game()
g.show_start_screen()
while g.running:
  g.new()
  g.show_go_screen()

pg.quit()