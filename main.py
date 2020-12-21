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
  KEYUP,
  QUIT,
)

class Game:
  def __init__(self):
    # Initialize Game
    pg.mixer.init()
    pg.init()
    pg.display.set_caption(TITLE)
    self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    self.clock = pg.time.Clock()
    self.font_name = pg.font.match_font(FONT_NAME)

  
  def new(self):
    # start a new game
    self.score = 0
    self.all_sprites = pg.sprite.Group()
    self.platforms = pg.sprite.Group()
    self.player = Player(self)
    self.all_sprites.add(self.player)
    # ground platform
    p1 = Platform(0, HEIGHT -40, WIDTH, 40)
    self.all_sprites.add(p1)
    self.platforms.add(p1)
    # continued ground
    p_1 = Platform(-100, HEIGHT -40, WIDTH, 40)
    self.all_sprites.add(p_1)
    self.platforms.add(p_1)
    # seperated ground
    p_2 = Platform(-350, HEIGHT * 3/4, 100, 40)
    self.all_sprites.add(p_2)
    self.platforms.add(p_2)
    p_3 = Platform(-650, HEIGHT -40, 200, 40)
    self.all_sprites.add(p_3)
    self.platforms.add(p_3)
    p_4 = Platform(-1150, HEIGHT -40, 200, 40)
    self.all_sprites.add(p_4)
    self.platforms.add(p_4)
    p_5 = Platform(-1550, HEIGHT -40, 200, 40)
    self.all_sprites.add(p_5)
    self.platforms.add(p_5)
    # raised platform
    p2 = Platform(WIDTH/2 - 50, HEIGHT * 3/4, 100, 40)
    self.all_sprites.add(p2)
    self.platforms.add(p2)
    # 2nd raised platform
    p3 = Platform(WIDTH/4 - 100, HEIGHT * 3/4, 100, 40)
    self.all_sprites.add(p3)
    self.platforms.add(p3)
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
    # if self.player.rect.left >= HEIGHT - 200:
    #         self.player.pos.x -= abs(self.player.vel.x)
    #         for plat in self.platforms:
    #             plat.rect.x -= abs(self.player.vel.x)
    if self.player.rect.right <= WIDTH / 2:
            self.player.pos.x += abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x += abs(self.player.vel.x)
                # if plat.rect.right >= WIDTH:
                  # plat.kill()
                self.score += 1

    if self.player.rect.bottom > HEIGHT:
      for sprite in self.all_sprites:
        sprite.rect.y -= max(self.player.vel.y, 10)
        if sprite.rect.bottom <0:
          sprite.kill()
        if len(self.platforms) ==0:
          self.playing= False

    while len(self.platforms) < 6:
      width = random.randrange(50, 100)
      p = Platform(random.randrange(0, WIDTH-width),
                random.randrange(-75, -30),
                width, 20)
      self.platforms.add(p)
      self.all_sprites.add(p)

  def events(self):
    # Game Loop - events
      for event in pg.event.get():
        # check for closing window
        if event.type == pg.QUIT:
          if self.playing:
            self.playing = False
            self.run = False
        if event.type == pg.KEYDOWN:
          if event.key == pg.K_UP:
            self.player.jump()

  def draw(self):
    #Game Loop - draw 
    self.screen.fill(BLACK)
    self.all_sprites.draw(self.screen)
    self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15) 
    pg.display.flip()


  def show_start_screen(self):
    # game splash/start screen
    self.screen.fill(BLACK)
    self.draw_text(TITLE, 48, WHITE, WIDTH /2, HEIGHT / 4)
    self.draw_text("Right and Left Arrow to move, Up Arrow to jump", 22, WHITE, WIDTH / 2, HEIGHT /2)
    self.draw_text("Press a key to play", 22, WHITE, WIDTH /2, HEIGHT * 3/4)
    pg.display.flip()
    self.wait_for_key()

  def show_go_screen(self):
    #game over/continue
    pass

  def wait_for_key(self):
    waiting = True
    while waiting:
      self.clock.tick(FPS)
      for event in pg.event.get():
        if event.type == pg.QUIT:
          waiting = False
          self.running = False
        if event.type == pg.KEYUP:
          waiting = False


  def draw_text(self, text, size, color, x, y):
    font = pg.font.Font(self.font_name, size)
    text_surface = font.render(text, True, color)
    text_rect= text_surface.get_rect()
    text_rect.midtop = (x,y)
    self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.run:
  g.new()
  g.show_go_screen()

pg.quit()