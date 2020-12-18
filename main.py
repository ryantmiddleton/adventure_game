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
  KEYDOWN,
  QUIT,
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
    self.player = Player()
    self.all_sprites.add(self.player)
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
    pass

  def events(self):
    # Game Loop - events
      for event in pg.event.get():
        # check for closing window
        if event.type == pg.QUIT:
          if self.playing:
            self.playing = False
          self.running = False

  def draw(self):
    #Game Loop - draw 
    self.screen.fill(BLACK)
    self.all_sprites.draw(self.screen)
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