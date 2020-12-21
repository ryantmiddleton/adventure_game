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
  K_SPACE,
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
    self.platforms = pg.sprite.Group()
    self.player = Player(self)
    self.all_sprites.add(self.player)
    for platform in PLATFORM_LIST:
      # create a new platform - could also use p=Platform(*platform)
      p = Platform(platform[0], platform[1], platform[2], platform[3])
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
    # Check if the player hits a platform, only if falling
    if self.player.vel.y > 0:
      hits = pg.sprite.spritecollide(self.player, self.platforms, False)
      # if the player's feet hits a platform
      if hits:
            # set the player's y position to the top (y) of the platform
            self.player.pos.y = hits[0].rect.top
            # stop the player by seting velocity to 0
            self.player.vel.y = 0;
    # If player reaches the top 25% 
    # scroll all platforms down (increase y coord)
    if self.player.rect.top <= HEIGHT/4:
        self.player.pos.y += abs(self.player.vel.y)
        for platform in self.platforms:
            platform.rect.y += abs(self.player.vel.y)
    # If player reaches the bottom 25% 
    # scroll all platforms up (decrease y coord)
    if self.player.rect.bottom >= HEIGHT * 0.75:
        self.player.pos.y -= abs(self.player.vel.y)
        for platform in self.platforms:
            platform.rect.y -= abs(self.player.vel.y)


  def events(self):
    # Game Loop - events
      for event in pg.event.get():
        # check for closing window
        if event.type == pg.QUIT:
          if self.playing:
            self.playing = False
          self.running = False
        if event.type == KEYDOWN:
          if event.key == K_SPACE:
            self.player.jump()

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

  def draw_map3(self):
    map3 = pg.Surface((1080, 2160))
    # self.scroll_val += 1;
    platform_width = 175
    platform_height = 25
    # top of map
    pg.draw.rect(map3, SILVER, (0,0,20, 2160))
    # right side of map
    pg.draw.rect(map3, SILVER, (WIDTH - 20,0,20, 2160))
    pg.draw.rect(map3, SILVER, (0,0,WIDTH, 20))
    pg.draw.rect(map3,SILVER,(WIDTH/2 - platform_width/2, 360 + self.player.image.get_height()/2,platform_width,platform_height))
    pg.draw.rect(map3,GOLD,(120,120,175,25))
    self.screen.blit(map3, (0, 0))


g = Game()
g.show_start_screen()
while g.running:
  g.new()
  g.show_go_screen()

pg.quit()