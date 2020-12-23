import pygame as pg
import random
from settings import *
from sprites import *
from os import path


from pygame.locals import (
  RLEACCEL,
  K_UP,
  K_DOWN,
  K_LEFT,
  K_RIGHT,
  K_ESCAPE,
  K_SPACE,
  KEYDOWN,
  KEYUP,
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
    pg.display.set_caption(TITLE)
    self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    self.clock = pg.time.Clock()
    self.running = True
    self.font_name = pg.font.match_font(FONT_NAME)
    self.load_data()
    
    
  def load_data(self):
    self.dir = path.dirname(__file__)
    img_dir = path.join(self.dir, 'imgs')
    with open(path.join(self.dir, HS_FILE), 'w') as f:
      try:
        self.highscore = int(f.read())
      except:
        self.highscore = 0
    self.spritesheet = Spirtesheet(path.join(img_dir, SPRITESHEET))
    self.snd_dir = path.join(self.dir, 'snd')
    self.bg_dir = path.join(self.dir, 'bg')
    self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'jump_snd.wav'))
    self.shoot_sound = pg.mixer.Sound(path.join(self.snd_dir, 'shoot.wav'))


  def new(self):
    # start a new game
    self.score = 0
    self.all_sprites = pg.sprite.Group()
    self.platforms = pg.sprite.Group()
    self.bullets = pg.sprite.Group()
    self.door1 = pg.sprite.Group()
    self.door2 = pg.sprite.Group()
    self.door3 = pg.sprite.Group()
    self.key1 = pg.sprite.Group()
    self.key2 = pg.sprite.Group()
    self.key3 = pg.sprite.Group()
    self.player = Player(self)
    self.all_sprites.add(self.player)
    


    self.acid = pg.sprite.Group()
    self.player = Player(self)
    self.all_sprites.add(self.player)
    for plat in MAP1_PLATFORM_LIST:
      p = Platform(*plat)
      self.all_sprites.add(p)
      self.platforms.add(p)
    acid = Acid(500, HEIGHT - 40, 100, 30)
    self.all_sprites.add(acid)
    self.acid.add(acid)  

    pg.mixer.music.load(path.join(self.snd_dir, 'background_music.ogg'))
    
    # self.all_sprites.add(acid)
    # self.acid.add(acid)  
    self.run()
    
    

  def run(self):
    # Game loop
    pg.mixer.music.play(loops=-1)
    self.playing = True
    self.load_level()
    while self.playing:
      self.clock.tick(FPS)
      self.events()
      self.update()
      self.draw()
    pg.mixer.music.fadeout(500)

  def update(self):
    # Game Loop - Update
    self.all_sprites.update()
    # platform detection if falling
    if self.player.vel.y > 0:
      hits = pg.sprite.spritecollide(self.player, self.platforms, False)
      if hits:
        self.player.pos.y = hits[0].rect.top
        self.player.vel.y = 0
    # Key detection for Key 1
    key1_hit = pg.sprite.spritecollide(self.player, self.key1, True)
    if key1_hit:
      door_hit = True
    # Door detection for Door 1
    door_hit = pg.sprite.spritecollide(self.player, self.door1, False)
    if door_hit:
        while self.player.level < 50:
          self.player.level += 1
        print('success')
        print(self.player.level)

        self.load_level()

    # Add wall blocking Level 1
    if self.player.level == 50:
      if self.player.pos.x > 340:
        wall_1 = Platform(500, 0, 20, 720)
        self.all_sprites.add(wall_1)
        self.platforms.add(wall_1)
          
    # Door detection for Door 2
    door_hit2 = pg.sprite.spritecollide(self.player, self.door2, False)
    if door_hit2:
        while self.player.level < 100:
          self.player.level += 1
        print('success')
        print(self.player.level)
        self.load_level()
    # Door detection for Door 3
    door_hit3 = pg.sprite.spritecollide(self.player, self.door3, False)
    if door_hit3:
        while self.player.level < 150:
          self.player.level += 1
        print('success')
        print(self.player.level)
        self.load_level()    

    # Side scrolling
    if self.player.rect.right <= WIDTH / 3:
      self.player.pos.x += abs(self.player.vel.x)
      for plat in self.platforms:
        plat.rect.x += abs(self.player.vel.x)
      for door in self.door1:
        door.rect.x += abs(self.player.vel.x)
      for door in self.door2:
            door.rect.x += abs(self.player.vel.x)
      for door in self.door3:
            door.rect.x += abs(self.player.vel.x)
      for key in self.key1:
        key.rect.x += abs(self.player.vel.x)
      for key in self.key2:
        key.rect.x += abs(self.player.vel.x)
      for key in self.key3:
        key.rect.x += abs(self.player.vel.x)
          # if plat.rect.right >= WIDTH:
            # plat.kill()
      self.score += 1

      if self.player.pos.y < hits[0].rect.bottom:
        self.player.pos.y = hits[0].rect.top
        self.player.vel.y = 0
        self.player.jumping = False
    if self.player.rect.right <= WIDTH / 2:
            self.player.pos.x += abs(self.player.vel.x)
            # self.acid.pos.x += abs(self.player.vel.x)
            for plat in self.platforms:
                  plat.rect.x += abs(self.player.vel.x)
                  self.score += 1
    elif self.player.rect.left >= WIDTH * .75:
            self.player.pos.x -= abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x -= abs(self.player.vel.x)
                # self.score += 1

    if self.player.rect.bottom > HEIGHT:
      for sprite in self.all_sprites:
        sprite.rect.y -= max(self.player.vel.y, 10)
        if sprite.rect.bottom <0:
          sprite.kill()
        if len(self.platforms) ==0:
          self.playing= False

  def events(self):
    # Game Loop - events
      keys = pg.key.get_pressed()
      for event in pg.event.get():
      # check for closing window
        if event.type == pg.QUIT:
          self.running = False
          if self.playing:
            self.playing = False
          
        
        if event.type == pg.KEYDOWN:
          if event.key == pg.K_UP:
            self.player.jump()
            
        if event.type == pg.KEYUP:
          if event.key == pg.K_UP:
            self.player.jump_cut()

          if event.key == pg.K_SPACE:
            if keys[pg.K_d] and keys[pg.K_w]:
              facing = 3
              self.shoot_sound.play()
            elif keys[pg.K_a] and keys[pg.K_w]:
              facing = -3
              self.shoot_sound.play()
            elif keys[pg.K_w]:
              facing = 2
              self.shoot_sound.play()
            elif keys[pg.K_d]:
              facing = 1
              self.shoot_sound.play()
            elif self.player.left or keys[pg.K_a]:
              facing = -1    
              self.shoot_sound.play()    
            else:
              facing = 1
              self.shoot_sound.play()
            b = Bullet(self.player.pos.x, self.player.pos.y, facing)
            self.all_sprites.add(b)
            self.bullets.add(b)

    acid_hit = pg.sprite.spritecollide(self.player, self.acid, False)
    if acid_hit:
      self.player.health -= 1
    if self.player.health < self.player.max_health:
      self.player.health += .01
    if self.player.health <= 0:
      self.playing = False

  def events(self):
    # Game Loop - events
    keys = pg.key.get_pressed()
    for event in pg.event.get():
      # check for closing window
      if event.type == pg.QUIT:
        if self.playing:
          self.playing = False
        self.running = False
      



  def draw(self):
    #Game Loop - draw 
    self.back_image = pg.image.load('bg/plx-4.png')
    self.back_image = pg.transform.scale(self.back_image, (1400, 720))
    self.back_rect = self.back_image.get_rect()
    self.screen.fill(BLACK)

    self.screen.blit(self.back_image, self.back_rect.move(0,0))
    self.all_sprites.draw(self.screen)
    pg.draw.rect(self.screen, RED, (20, 20, (self.player.max_health*20), 5))
    pg.draw.rect(self.screen, GREEN, (20, 20, (self.player.health*20), 5))

    self.screen.blit(self.player.image, self.player.rect)
    self.back_rect.move_ip(-2, 0)
    if self.back_rect.right == 0:
      self.back_rect.x =0
    self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15) 

    pg.display.flip()

  def load_level(self):
  # Load Level 1
    if self.player.level == 1:
      # Level 1 Platforms
      for plat in MAP1_PLATFORM_LIST:
        p = Platform(*plat)
        self.all_sprites.add(p)
        self.platforms.add(p)
      # Level 1 Door  
      d1 = Door1(200, 250, 30, 50)
      self.all_sprites.add(d1)
      self.door1.add(d1)
      # Level 1 Key
      key_rect = Key1(350, 200, 10, 10)
      self.all_sprites.add(key_rect)
      self.key1.add(key_rect)
  # Load Level 2
    if self.player.level == 50:
      # Level 2 Platforms
      for plat in MAP2_PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
      # Level 2 Door
      d2 = Door2(300, 250, 30, 50)
      self.all_sprites.add(d2)
      self.door2.add(d2)
      # Level 2 Key
      k2 = Key2(350, 200, 10, 10)
      self.all_sprites.add(k2)
      self.key2.add(k2)
  # Load Level 3 
    if self.player.level == 100:
      # Level 3 Platforms
      for plat in MAP3_PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
      # Level 3 Door
      d3 = Door3(300, 250, 30, 50)
      self.all_sprites.add(d3)
      self.door3.add(d3)
      # Level 3 Key
      k3 = Key3(350, 200, 10, 10)
      self.all_sprites.add(k3)
      self.key3.add(k3)
  # Load Level 4
    if self.player.level == 150:
      # Level 4 Platforms
      for plat in MAP4_PLATFORM_LIST:
       p = Platform(*plat)
       self.all_sprites.add(p)
       self.platforms.add(p)
      

  def show_start_screen(self):
    # game splash/start screen
    self.screen.fill(BLACK)
    self.draw_text("Welcome to Metroidvania... Enter if you dare!", 48, BLUE, WIDTH /2, HEIGHT / 4)
    self.draw_text("Controls: Right and Left Arrow to move, Up Arrow to jump, Space Bar to shoot, AWSD for directional shooting", 22, WHITE, WIDTH / 2, HEIGHT /2)
    self.draw_text("You ready? Press a key to play", 22, WHITE, WIDTH /2, HEIGHT * 3/4)
    self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH /2, 15)
    pg.display.flip()
    self.wait_for_key()

  def show_go_screen(self):
    #game over/continue
    pg.mixer.music.load(path.join(self.snd_dir, 'end.ogg'))
    pg.mixer.music.play(loops = -1)
    self.screen.fill(BLACK)
    if self.score < 4000:
      self.draw_text("You are pretty bad at this! GAME OVER!!!", 48, RED, WIDTH /2, HEIGHT / 4)
    else:
      self.draw_text("I've seen better! GAME OVER!", 48, RED, WIDTH /2, HEIGHT / 4)
    self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT /2)
    self.draw_text("Press key to play again", 22, WHITE, WIDTH /2, HEIGHT * 3/4)
    if self.score > self.highscore:
      self.highscore = self.score
      self.draw_text("New High Score: " + str(self.highscore), 22, WHITE, WIDTH /2, HEIGHT/2 + 40)
      with open(path.join(self.dir, HS_FILE), 'w') as f:
        f.write(str(self.score))
    else: 
      self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH /2, HEIGHT/2 + 40)
    pg.display.flip()
    self.wait_for_key()
    pg.mixer.music.fadeout(500)

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