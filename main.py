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
  K_SPACE,
  K_LALT,
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
    self.font_name = pg.font.match_font(FONT_NAME)
    self.running = True
    self.playing = False
    self.font_name = pg.font.match_font(FONT_NAME)
    self.load_data()
    # Initialize the player
    self.player = Player(self)

  def load_data(self):
    self.dir = path.dirname(__file__)
    self.img_dir = path.join(self.dir, 'imgs')
    with open(path.join(self.dir, HS_FILE), 'w') as f:
      try:
        self.highscore = int(f.read())
      except:
        self.highscore = 0
    self.snd_dir = path.join(self.dir, 'snd')
    self.bg_dir = path.join(self.dir, 'bg')
    self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'jump_snd.wav'))
    self.shoot_sound = pg.mixer.Sound(path.join(self.snd_dir, 'shoot.wav'))


  def new(self):
    # start a new game
    # Initialize score to zero
    self.score = 0

    # Define Sprite Groups
    self.all_sprites = pg.sprite.Group()
    self.platforms = pg.sprite.Group()
    self.bullets = pg.sprite.Group()
    self.acid_pools = pg.sprite.Group()
    self.enemies = pg.sprite.Group()
    self.doors = pg.sprite.Group()
    self.keys = pg.sprite.Group()

    # Add player to sprite group
    self.all_sprites.add(self.player)
    
    # Load all platforms and enemies 
    # based on current player.level

    #LEVEL 1
    if self.player.level == 1:
      # Add Platforms
      for plat in MAP1_PLATFORM_LIST:
        p = Platform(plat[0], plat[1], 380, 94)
        self.all_sprites.add(p) 
        self.platforms.add(p)
      # Add Level 1 Door  
      d1 = Door(200, 250, 30, 50)
      # Position player right where the door is
      self.player.rect.x = 200
      self.player.rect.y = 250
      self.all_sprites.add(d1)
      self.doors.add(d1)
      # Add Level 1 Key
      k1 = Key(350, 200, 10, 10)
      self.all_sprites.add(k1)
      self.keys.add(k1)
      # Add Acid
      acid = Acid(500, HEIGHT - 40, 100, 30)
      self.all_sprites.add(acid)
      self.acid_pools.add(acid)  

    # LEVEL 2
    if self.player.level == 2:
      # Level 2 Platforms
      for plat in MAP2_PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
      # Level 2 Door
      d2 = Door(300, 250, 30, 50)
      self.all_sprites.add(d2)
      self.doors.add(d2)
      # Level 2 Key
      k2 = Key(350, 200, 10, 10)
      self.all_sprites.add(k2)
      self.keys.add(k2)

    # LEVEL 3
    if self.player.level == 3:
      # Add Platforms
      for platform in MAP3_PLATFORM_LIST:
        # create a new platform - could also use p=Platform(platform[0], platform[1])
        p = Platform(*platform)
        # Add enemies to each platform
        spider = Spider(p.rect.midbottom[0]-25, p.rect.midbottom[1], self)
        self.all_sprites.add(spider)
        self.enemies.add(spider)
        self.all_sprites.add(p)
        self.platforms.add(p)
      # spider = Spider(WIDTH/2, HEIGHT *3/4+20, self)
      # self.all_sprites.add(spider)
      # self.enemies.add(spider)
      # Level 3 Door
      d3 = Door(300, 250, 30, 50)
      self.all_sprites.add(d3)
      self.doors.add(d3)
      # Level 3 Key
      k3 = Key(350, 200, 10, 10)
      self.all_sprites.add(k3)
      self.keys.add(k3)

    # LEVEL 4
    if self.player.level == 150:
      # Level 4 Platforms
      for plat in MAP4_PLATFORM_LIST:
       p = Platform(*plat)
       self.all_sprites.add(p)
       self.platforms.add(p)

    # Load music to all levels
    pg.mixer.music.load(path.join(self.snd_dir, 'background_music.ogg'))
    self.run()
    
  def run(self):
    # Game loop
    pg.mixer.music.play(loops=-1)
    self.playing = True
    while self.playing:
      self.clock.tick(FPS)
      self.events()
      self.update()
      self.draw()
    pg.mixer.music.fadeout(500)

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

      # WHAT IS THIS CODE DOING??? DOES IT TEST IF PLAYER HITS THE BOTTOM OF A PLATFORM?
      # if self.player.pos.y < hits[0].rect.bottom:
      #   self.player.pos.y = hits[0].rect.top
      #   self.player.vel.y = 0
      #   self.player.jumping = False

    if self.player.level == 1 or self.player.level == 2:
      # Side Scrolling Logic
      if self.player.rect.right <= WIDTH / 4:
        for plat in self.platforms:
          plat.rect.x += abs(int(self.player.vel.x))
          self.score += 1
        for enemy in self.enemies:
          enemy.rect.x += abs(int(self.player.vel.x))
        for key in self.keys:
            key.rect.x += abs(int(self.player.vel.x))
        for door in self.doors:
            door.rect.x += abs(int(self.player.vel.x))
        for acid in self.acid_pools:
            acid.rect.x += abs(int(self.player.vel.x))
        self.player.pos.x += abs(self.player.vel.x)

      elif self.player.rect.left >= WIDTH * .75:
        self.player.pos.x -= abs(self.player.vel.x)
        for plat in self.platforms:
          plat.rect.x -= abs(self.player.vel.x)
          # self.score += 1
        for enemy in self.enemies:
            enemy.rect.x -= abs(int(self.player.vel.x))
        for key in self.keys:
            key.rect.x -= abs(int(self.player.vel.x))
        for door in self.doors:
            door.rect.x -= abs(int(self.player.vel.x))
        for acid in self.acid_pools:
            acid.rect.x -= abs(int(self.player.vel.x))
        self.player.pos.x += abs(self.player.vel.x)

    if self.player.level == 3:
          # Vertical Scrolling Logic
      # If player reaches the top 25% of the screen
      # scroll all sprites down (increase y coord)
      if abs(self.player.rect.top) <= HEIGHT/4:
        if not(self.player.isStanding()):
          for platform in self.platforms:
              platform.rect.y += abs(int(self.player.vel.y))
          for enemy in self.enemies:
              enemy.rect.y += abs(int(self.player.vel.y))
          for key in self.keys:
              key.rect.y += abs(int(self.player.vel.y))
          for door in self.doors:
              door.rect.y += abs(int(self.player.vel.y))
          for acid in self.acid_pools:
              acid.rect.y += abs(int(self.player.vel.y))
          self.player.pos.y += abs(self.player.vel.y)
      # If player reaches the bottom 25% of the screen
      # scroll all sprites up (decrease y coord)
      if abs(self.player.rect.top) >= HEIGHT * 0.75:
        if not(self.player.isStanding()):
          for platform in self.platforms:
              platform.rect.y -= abs(int(self.player.vel.y))
          for enemy in self.enemies:
              enemy.rect.y -= abs(int(self.player.vel.y))
          for key in self.keys:
              key.rect.y -= abs(int(self.player.vel.y))
          for door in self.doors:
              door.rect.y -= abs(int(self.player.vel.y))
          for acid in self.acid_pools:
              acid.rect.y -= abs(int(self.player.vel.y))
          self.player.pos.y -= abs(self.player.vel.y)

    # Player has fallen and died
    if self.player.rect.bottom > HEIGHT:
      for sprite in self.all_sprites:
        sprite.rect.y -= max(self.player.vel.y, 10)
        if sprite.rect.bottom <0:
          sprite.kill()
        if len(self.platforms) ==0:
          self.playing= False

    # Player Collision Detection
    # Key detection for any of the keys
    key_hit = pg.sprite.spritecollideany(self.player, self.keys)
    # If a player collides with a key, the key sprite is returned (not None)
    if key_hit != None:
      # remove the key from the screen
      key_hit.kill()
      #set key_hit to True because player has the key now
      self.player.hasKey = True
    # Door detection for any of the doors
    door_hit = pg.sprite.spritecollideany(self.player, self.doors)
    # If a player collides with a door and has already gotten the key, the door sprite is returned
    if door_hit != None and self.player.hasKey:
      # Go to the next level
      self.player.level += 1
      # Reset the key boolean for next level
      self.player.hasKey = False
      # print('success')
      # print(self.player.level)
      self.new()

    # Acid
    acid_hit = pg.sprite.spritecollide(self.player, self.acid_pools, False)
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
        if event.type == QUIT:
          if self.playing:
            self.playing = False
          self.running = False


        if event.type == KEYDOWN:
          #Check to see if the game is over/starting
          # Player 'hit any key' from show_start_screen() or show_go_screen() to restart the game
          if self.playing == False:
            self.playing = True
          elif self.playing == True:
            # invoke a jump when holding down the 'UP' arrow
            if event.key == K_UP:
              self.player.jump()
            elif keys[K_d] and keys[K_w]:
              b = Bullet(self.player.pos.x, self.player.pos.y, 3)
              self.all_sprites.add(b)
              self.bullets.add(b)
              self.shoot_sound.play()
            elif keys[K_a] and keys[K_w]:
              b = Bullet(self.player.pos.x, self.player.pos.y, -3)
              self.all_sprites.add(b)
              self.bullets.add(b)
              self.shoot_sound.play()
            elif keys[K_w]:
              b = Bullet(self.player.pos.x, self.player.pos.y, 2)
              self.all_sprites.add(b)
              self.bullets.add(b)
              self.shoot_sound.play()                
            elif keys[K_d]:
              b = Bullet(self.player.pos.x, self.player.pos.y, 1)
              self.all_sprites.add(b)
              self.bullets.add(b)
              self.shoot_sound.play()                    
            elif self.player.left or keys[K_a]:
              b = Bullet(self.player.pos.x, self.player.pos.y, -1)
              self.all_sprites.add(b)
              self.bullets.add(b)
              self.shoot_sound.play()    
            else:
              b = Bullet(self.player.pos.x, self.player.pos.y, 1)
              self.all_sprites.add(b)
              self.bullets.add(b)
              self.shoot_sound.play()  
            #invoke a 'shallow' jump 
          # when tapping the 'UP' arrow
          # if event.key == K_UP:
          #   self.player.jump_cut()


  def draw(self):
    #Game Loop - draw 
    self.back_image = pg.image.load('bg/plx-4.png')
    self.back_image = pg.transform.scale(self.back_image, (1400, 720))
    self.back_rect = self.back_image.get_rect()
    self.screen.fill(BLACK)

    self.screen.blit(self.back_image, self.back_rect.move(0,0))
    self.all_sprites.draw(self.screen)
    self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15) 
    pg.draw.rect(self.screen, RED, (20, 20, (self.player.max_health*20), 5))
    pg.draw.rect(self.screen, GREEN, (20, 20, (self.player.health*20), 5))
    self.screen.blit(self.player.image, self.player.rect)
    self.back_rect.move_ip(-2, 0)
    if self.back_rect.right == 0:
      self.back_rect.x =0
    self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15) 
    pg.display.flip()      

  def show_start_screen(self):
    # game splash/start screen
    self.screen.fill(BLACK)
    self.draw_text("Welcome to Metroidvania... Enter if you dare!", 48, BLUE, WIDTH /2, HEIGHT / 4)
    self.draw_text("Controls: Right and Left Arrow to move, Up Arrow to jump, Space Bar to shoot, AWSD for directional shooting", 22, WHITE, WIDTH / 2, HEIGHT /2)
    self.draw_text("You ready? Press a key to play", 22, WHITE, WIDTH /2, HEIGHT * 3/4)
    self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH /2, 15)
    pg.display.flip()
    # Wait for player to hit a key to start
    while self.playing == False and self.running == True:
      self.events()

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

    # Wait for player to hit a key to restart the game OR QUIT
    while self.playing == False and self.running == True:
      self.events()
    pg.mixer.music.fadeout(500)

  def draw_text(self, text, size, color, x, y):
    font = pg.font.Font(self.font_name, size)
    text_surface = font.render(text, True, color)
    text_rect= text_surface.get_rect()
    text_rect.midtop = (x,y)
    self.screen.blit(text_surface, text_rect)

    

g = Game()
g.show_start_screen()
while g.running:
  g.new()
  g.show_go_screen()

pg.quit()