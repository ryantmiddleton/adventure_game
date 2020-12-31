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
    # Initialize Path directories
    self.dir = path.dirname(__file__)
    self.img_dir = path.join(self.dir, 'imgs')
    self.snd_dir = path.join(self.dir, 'snd')
    self.bg_dir = path.join(self.dir, 'bg')
    with open(path.join(self.dir, HS_FILE), 'w') as f:
      try:
        self.highscore = int(f.read())
      except:
        self.highscore = 0

    # Initialize Spritesheets
    self.platform_spritesheet = Spritesheet(path.join(self.img_dir, PLATFORM_SPRITESHEET))
    
    # Load Spider Images
    spider_spritesheet = Spritesheet(path.join(self.img_dir, SPIDER_SPRITESHEET))
    size = spider_spritesheet.image_sheet.get_size()
    self.spider_right_images = spider_spritesheet.strip_from_sheet(spider_spritesheet.image_sheet, (6,6), (8,6), (size[0]/12,size[1]/8))
    self.spider_left_images = spider_spritesheet.strip_from_sheet(spider_spritesheet.image_sheet, (6,5), (8,5), (size[0]/12,size[1]/8))
    # Crop each image from spritesheet
    for i in range (len(self.spider_right_images)):
      self.spider_right_images[i] = spider_spritesheet.crop(self.spider_right_images[i],(10,20),(65,45))
      self.spider_left_images[i] = spider_spritesheet.crop(self.spider_left_images[i],(10,20),(65,45))
      # Iniitialize a rotation and scale
      # self.spider_right_images[i] = pg.transform.rotozoom(self.spider_right_images[i], 0, 1)
      # self.spider_left_images[i] = pg.transform.rotozoom(self.spider_left_images[i], 0, 1)

    # Load Explosion Images
    explosion_spritesheet = Spritesheet(path.join(self.img_dir, EXPLOSION_SPRITESHEET))
    size = explosion_spritesheet.image_sheet.get_size()
    self.explosion_images = explosion_spritesheet.strip_from_sheet(explosion_spritesheet.image_sheet , (0,0), (7,4), (size[0]/8,size[1]/8))
    
    # Initialize Sounds
    self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'jump_snd.wav'))
    self.shoot_sound = pg.mixer.Sound(path.join(self.snd_dir, 'shoot.wav'))

  def new(self):
    # start a new game
    # Initialize score to zero
    self.score = 0

    # Define Sprite Groups
    self.all_sprites = pg.sprite.Group()
    self.groundplatform = pg.sprite.Group()
    self.platforms = pg.sprite.Group()
    self.platform_boss = pg.sprite.Group()
    self.bullets = pg.sprite.Group()
    self.acid_pools = pg.sprite.Group()
    self.enemies = pg.sprite.Group()
    self.doors = pg.sprite.Group()
    self.keys = pg.sprite.Group()
    self.boss = pg.sprite.Group()
    self.heart = pg.sprite.Group()
    self.coin = pg.sprite.Group()
    self.bat_timer = 0
    self.small_boss_timer = 0
    # Add player to sprite group
    self.all_sprites.add(self.player)
    # Load music to all levels

    pg.mixer.music.load(path.join(self.snd_dir, 'background_music.ogg'))
    self.load_level()
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
    if self.player.vel.y > 0:
      gp_hits = pg.sprite.spritecollide(self.player, self.groundplatform, False)
      if gp_hits:
        if self.player.pos.y < gp_hits[0].rect.bottom:
          self.player.pos.y = gp_hits[0].rect.top
          self.player.vel.y = 0
          self.player.jumping = False
      
      hits = pg.sprite.spritecollide(self.player, self.platforms, False)
      if hits:
        if self.player.pos.y < hits[0].rect.bottom:
          self.player.pos.y = hits[0].rect.top
          self.player.vel.y = 0
          self.player.jumping = False

      bp_hits = pg.sprite.spritecollide(self.player, self.platform_boss, False)
      if bp_hits:
        if self.player.pos.y < bp_hits[0].rect.bottom:
          self.player.pos.y = bp_hits[0].rect.top
          self.player.vel.y = 0
          self.player.jumping = False
    
    # Load enemies - bats
    if self.player.level == 2:
    # Spawn bats
      now = pg.time.get_ticks()
      if now - self.bat_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
        self.bat_timer = now
        bat = Bat(self)
        self.all_sprites.add(bat)
        self.enemies.add(bat)

    
    # Set scrolling variables 
    if self.player.level == 3:
      # Vertical (y) scrolling
      scroll_dir = 1
      scroll_dim = 3
      screen_dim = HEIGHT
    else:
      # Side (x) scrolling
      scroll_dir = 0
      scroll_dim = 2
      screen_dim = WIDTH

    # If player reaches the top/right 25% of the screen
    # scroll all sprites down (increase x/y coord)
    if self.player.rect[scroll_dir] + self.player.rect[scroll_dim] <= screen_dim / 4:
      for sprite in self.all_sprites:
        sprite.rect[scroll_dir] += abs(int(self.player.vel[scroll_dir]))
      self.player.pos[scroll_dir] += abs(int(self.player.vel[scroll_dir]))
    # If player reaches the bottom/left 25% of the screen
    # scroll all sprites up/right (decrease x/y coord)
    elif self.player.rect[scroll_dir] >= screen_dim * .75:
      for sprite in self.all_sprites:
            sprite.rect[scroll_dir] -= abs(int(self.player.vel[scroll_dir]))
      self.player.pos[scroll_dir] -= abs(int(self.player.vel[scroll_dir]))

    # Player has fallen and died
    if self.player.rect.bottom > HEIGHT:
      for sprite in self.all_sprites:
        sprite.rect.y -= max(self.player.vel.y, 10)
        if sprite.rect.bottom <0:
          sprite.kill()
        if len(self.platforms) ==0:
          self.playing= False

    bullet_platform_hit = pg.sprite.groupcollide(self.bullets, self.platforms, True, False)  

    # Player Collision Detection
    # Heart Collision Detection
    heart_hit = pg.sprite.spritecollideany(self.player, self.heart)
    if heart_hit:
      if self.player.health == 25:
        heart_hit.kill()
        print("Player Health Does Not Increase")
      if self.player.health == 24:
        heart_hit.kill()
        self.player.health += 1
        print("Player Health increases by 1")
      if self.player.health == 23:
        heart_hit.kill()
        self.player.health += 2
        print("Player Health increases by 2")
      if self.player.health == 22:
        heart_hit.kill()
        self.player.health += 3
        print("Player Health increases by 3")
      if self.player.health == 21:
        heart_hit.kill()
        self.player.health += 4
        print("Player Health increases by 4")
      if self.player.health == 20:
        heart_hit.kill()
        self.player.health += 5
        print("Player Health increases by 5")
      if self.player.health <= 19:
        heart_hit.kill()
        self.player.health += 5
        print("Player Health increases by 5")

    # Key collision detection for any of the keys
    key_hit = pg.sprite.spritecollideany(self.player, self.keys)
    # If a player collides with a key, the key sprite is returned (not None)
    if key_hit != None:
      # remove the key from the screen
      key_hit.kill()
      self.score += 5
      #set key_hit to True because player has the key now
      self.player.hasKey = True
    
    # Door collision detection for any of the doors
    door_hit = pg.sprite.spritecollideany(self.player, self.doors)
    # If a player collides with a door and has already gotten the key, the door sprite is returned
    if door_hit != None and self.player.hasKey:
      # Go to the next level
        self.player.level += 1
        self.score += 10
        # Reset the key boolean for next level
        self.player.hasKey = False
        # print('success')
        # print(self.player.level)
        # Kill all sprites from the board
        for plat in self.platforms:
          plat.kill()
        for gp in self.groundplatform:
          gp.kill()
        for boss_plat in self.platform_boss:
          boss_plat.kill()
        for door in self.doors:
          door.kill()
        for acid in self.acid_pools:
          acid.kill()
        for heart in self.heart:
          heart.kill()
        for spider in self.enemies:
          spider.kill()
        for coin in self.coin:
          coin.kill()
        # Load a new level
        self.load_level()
    

    shoot_boss = pg.sprite.groupcollide(self.bullets, self.boss, True, False)
    for boss in self.boss:
      if shoot_boss:
        boss.health -= 1
        if boss.vel.x < 0:
          boss.vel.x -= 2
        if boss.vel.x > 0:
          boss.vel.x += 2
      if boss.health <= 0:
        boss.deadboss = True
        self.score += 15
        for boss in self.boss:
          boss.kill()
        self.player.level += 1   
        self.load_level()
        print("You Have Won!")

    # Acid collision detection
    acid_hit = pg.sprite.spritecollide(self.player, self.acid_pools, False)
    if acid_hit:
      self.player.health -= 1
      self.score -= .5
      self.player.vel.y = -5
      if self.player.left == True:
        self.player.vel.x = 10
      else:
        self.player.vel.x = -10
    if self.player.health <= 0:
        self.playing = False

    # Coin Collision Detection
    coin_hit = pg.sprite.spritecollide(self.player, self.coin, False)
    if coin_hit:
      self.score += 1
      for coin in self.coin:
        coin.kill()

    #Bullet Collision Detection
    # If any bullets hit any enemies kill those bullets and enemies
    bullet_kill_list = pg.sprite.groupcollide(self.bullets, self.enemies, True, True)
    if bullet_kill_list:
      for bullet, enemy in bullet_kill_list.items():
        # print(enemy[0].rect)
        self.score += 5
        explosion = Explosion(enemy[0].rect.x, enemy[0].rect.y, self)
        self.all_sprites.add(explosion)

    # Check for player collision with boss enemey (only level 4)
    if self.player.level == 4:
      boss_hit = pg.sprite.spritecollide(self.player, self.boss, False)
      if boss_hit:
        self.player.health -= 1
        self.score -= .5
      if self.player.health <= 0:
        self.playing = False

    # Player collision with Spiders
    spider_hit = pg.sprite.spritecollide(self.player, self.enemies, False)
    if spider_hit:
      self.player.health -= 1
      self.score -= .5
      self.player.vel.y = -5
      if self.player.left == True:
        self.player.vel.x = 10
      else:
        self.player.vel.x = -10
    if self.player.health <= 0:
      self.playing = False

    if self.player.level == 4:    
      now = pg.time.get_ticks()
      if now - self.small_boss_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
        self.small_boss_timer = now
        small_boss = Small_Boss(self, WIDTH, HEIGHT, 10, 10)
        self.all_sprites.add(small_boss)
        self.enemies.add(small_boss)
      if self.score > 100:
        self.player.level += 1
        self.load_level()

  def load_level(self):
    # print ("Player level is " + str(self.player.level))
    #LEVEL 1
    if self.player.level == 1:
      self.player.pos = vec(WIDTH/2, HEIGHT/2)
      # Add Platforms
      gp = Ground_Platform(0, HEIGHT - 40, 2000, 96)
      self.all_sprites.add(gp)
      self.groundplatform.add(gp)
      for plat in MAP1_PLATFORM_LIST:
        p = Platform(self.platform_spritesheet, *plat)
        self.all_sprites.add(p) 
        self.platforms.add(p)
      # Add Level 1 Door  
      
      d = Door(WIDTH, HEIGHT - 135, 10, 20)
      self.all_sprites.add(d)
      self.doors.add(d)
      h = Heart(self, 250, 60, 10, 10)
      self.all_sprites.add(h)
      self.heart.add(h)
      # Add Level 1 Key
      k = Key(500, 175, 10, 10)
      self.all_sprites.add(k)
      self.keys.add(k)

      # Add Acid
      acid = Acid(self, 500, HEIGHT - 60)
      acid1 = Acid(self, 530, HEIGHT - 60)
      acid2 = Acid(self, 900, HEIGHT - 60)
      acid3 = Acid(self, 930, HEIGHT - 60)
      acid4 = Acid(self, 350, 180)
      self.all_sprites.add(acid)
      self.acid_pools.add(acid)
      self.all_sprites.add(acid1)
      self.acid_pools.add(acid1)
      self.all_sprites.add(acid2)
      self.acid_pools.add(acid2)
      self.all_sprites.add(acid3)
      self.acid_pools.add(acid3)
      self.all_sprites.add(acid4)
      self.acid_pools.add(acid4)

      coin = Coin(self.platform_spritesheet, 250, 20)
      self.all_sprites.add(coin)
      self.coin.add(coin)

    # LEVEL 2
    if self.player.level == 2:
      # Level 2 Platforms
      gp = Ground_Platform(-500, HEIGHT - 40, 2000, 96)
      self.all_sprites.add(gp)
      self.groundplatform.add(gp)
      for plat in MAP2_PLATFORM_LIST:
        p = Platform(self.platform_spritesheet, *plat)
        self.all_sprites.add(p)
        self.platforms.add(p)
      # Level 2 Door
      d = Door(WIDTH, HEIGHT - 135, 10, 20)
      self.all_sprites.add(d)
      self.doors.add(d)
      # Level 2 Key
      k = Key(-200, 75, 10, 10)
      self.all_sprites.add(k)
      self.keys.add(k)
      h = Heart(self, 775, 60, 10, 10)
      self.all_sprites.add(h)
      self.heart.add(h)
      # Level 2 Acid
      acid = Acid(self, 0, HEIGHT - 60)
      acid1 = Acid(self, 75, HEIGHT - 60)
      acid2 = Acid(self, 150, HEIGHT - 60)
      acid3 = Acid(self, 225, HEIGHT - 60)
      acid4 = Acid(self, 300, HEIGHT - 60)
      acid5 = Acid(self, 375, HEIGHT - 60)
      acid6 = Acid(self, 450, HEIGHT - 60)
      self.all_sprites.add(acid)
      self.acid_pools.add(acid)
      self.all_sprites.add(acid1)
      self.acid_pools.add(acid1)
      self.all_sprites.add(acid2)
      self.acid_pools.add(acid2)
      self.all_sprites.add(acid3)
      self.acid_pools.add(acid3)
      self.all_sprites.add(acid4)
      self.acid_pools.add(acid4)
      self.all_sprites.add(acid5)
      self.acid_pools.add(acid5)
      self.all_sprites.add(acid6)
      self.acid_pools.add(acid6)

    # LEVEL 3
    if self.player.level == 3:
      num_spiders = 10
      # Add Platforms
      gp = Ground_Platform(0, HEIGHT - 40, WIDTH, 96)
      self.all_sprites.add(gp)
      self.platforms.add(gp)
      for plat in MAP3_PLATFORM_LIST:
        p = Platform(self.platform_spritesheet, *plat)
        self.all_sprites.add(p)
        self.platforms.add(p)
        # Add enemies to each platform
        if num_spiders > 0:
          rand_num = randint(1,10)
          if rand_num <= 5:     
            spider = Spider(p.rect.midbottom[0]-25, p.rect.midbottom[1] - 1, self)
          else:
            spider = Spider(p.rect.midtop[0]-25, p.rect.midtop[1] - 50, self)
          self.all_sprites.add(spider)
          self.enemies.add(spider)
          num_spiders -= 1
      # for spider_pos in MAP3_SPIDERS_LIST:
      #   spider = Spider(*spider_pos, self)
      #   self.all_sprites.add(spider)
      #   self.enemies.add(spider)
      # Level 3 Door
      d = Door(300, -1445, 10, 20)
      self.all_sprites.add(d)
      self.doors.add(d)
      # Level 3 Key
      k = Key(950, 200, 10, 10)
      self.all_sprites.add(k)
      self.keys.add(k)

    # LEVEL 4
    if self.player.level == 4:
      temp = self.score
      print(temp)
      self.score = 0
      # Level 4 Platforms
      for plat in MAP4_PLATFORM_LIST:
       p = Platform_Boss(self.platform_spritesheet, *plat)
       self.all_sprites.add(p)
       self.platform_boss.add(p)
      h= Heart(self, -400, HEIGHT * .75 - 50, 10, 10)
      self.all_sprites.add(h)
      self.heart.add(h)
      acid5= Acid(self, -200, 350)
      self.all_sprites.add(acid5)
      self.acid_pools.add(acid5)
      

    if self.player.level == 5:
      for boss_plat in self.platform_boss:
          boss_plat.kill()
      for plat in MAP5_PLATFORM_LIST:
       p = Platform_Boss(self.platform_spritesheet, *plat)
       self.all_sprites.add(p)
       self.platform_boss.add(p)
      boss = Boss(self)
      self.all_sprites.add(boss)
      self.boss.add(boss)
      
    if self.player.level == 6:
      g.win_screen()

  def events(self):
    # Game Loop - events
      keys = pg.key.get_pressed()
      for event in pg.event.get():
        # check for closing window
        if event.type == pg.KEYDOWN and self.playing == False:
            # Start game if key pressed
            self.playing = True
            # self.player.level = 1
            self.player.health = 25
        else:
          if event.type == pg.KEYUP:
            if event.key == pg.K_UP:
              self.player.jump_cut()

          if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
              self.player.jump()
              self.player.boss_jump()
              self.player.ground_jump()

            if event.key == pg.K_SPACE:
              if keys[K_d] and keys[K_w]:
                    b = Bullet(self.player.pos.x, self.player.pos.y, 3)
                    self.all_sprites.add(b)
                    self.bullets.add(b)
                    self.shoot_sound.play()
              elif keys[K_a] and keys[K_w]:
                    b = Bullet(self.player.pos.x, self.player.pos.y, -3)
                    self.all_sprites.add(b)
                    self.bullets.add(b)
                    self.shoot_sound.play()
              elif keys[K_d] and keys[K_s]:
                    b = Bullet(self.player.pos.x, self.player.pos.y, 4)
                    self.all_sprites.add(b)
                    self.bullets.add(b)
                    self.shoot_sound.play()
              elif keys[K_a] and keys[K_s]:
                    b = Bullet(self.player.pos.x, self.player.pos.y, -4)
                    self.all_sprites.add(b)
                    self.bullets.add(b)
                    self.shoot_sound.play()
              elif keys[K_w]:
                    b = Bullet(self.player.pos.x, self.player.pos.y, 2)
                    self.all_sprites.add(b)
                    self.bullets.add(b)
                    self.shoot_sound.play()
              elif keys[K_s]:
                    b = Bullet(self.player.pos.x, self.player.pos.y, -2)
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

        if event.type == QUIT:
          if self.playing:
            self.playing = False
          self.running = False

  def draw(self):
    #Game Loop - draw 
    if self.player.level == 1 or self.player.level == 2 or self.player.level == 3:
      self.back_image = pg.image.load('bg/plx-4.png')
      self.back_image = pg.transform.scale(self.back_image, (1400, 720))
      self.back_rect = self.back_image.get_rect()
      self.screen.fill(BLACK)
      self.screen.blit(self.back_image, self.back_rect.move(0,0))
      self.all_sprites.draw(self.screen)
      self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, 35) 
      pg.draw.rect(self.screen, RED, (20, 20, (self.player.max_health*10), 5))
      pg.draw.rect(self.screen, GREEN, (20, 20, (self.player.health*10), 5))
      self.draw_text("Player Health: " + str(self.player.health) + "/25", 22, WHITE, 100, 35) 
      self.screen.blit(self.player.image, self.player.rect)
      self.back_rect.move_ip(-2, 0)
      if self.back_rect.right == 0:
        self.back_rect.x =0
      self.draw_text("Level " + str(self.player.level), 22, WHITE, WIDTH / 2, 15) 
    if self.player.level == 4:
      self.back_image = pg.image.load('bg/boss_level.jpg')
      self.back_image = pg.transform.scale(self.back_image, (1400, 720))
      self.back_rect = self.back_image.get_rect()
      self.screen.fill(BLACK)
      self.screen.blit(self.back_image, self.back_rect.move(0,0))
      self.all_sprites.draw(self.screen)
      self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, 35) 
      pg.draw.rect(self.screen, RED, (20, 20, (self.player.max_health*10), 5))
      pg.draw.rect(self.screen, GREEN, (20, 20, (self.player.health*10), 5))
      self.draw_text("Player Health: " + str(self.player.health) + "/25", 22, WHITE, 100, 35) 
      self.screen.blit(self.player.image, self.player.rect)
      if self.back_rect.right == 0:
        self.back_rect.x =0
      self.draw_text("Level " + str(self.player.level), 22, WHITE, WIDTH / 2, 15) 
    if self.player.level == 5:
      self.back_image = pg.image.load('bg/boss_level.jpg')
      self.back_image = pg.transform.scale(self.back_image, (1400, 720))
      self.back_rect = self.back_image.get_rect()
      self.screen.fill(BLACK)
      self.screen.blit(self.back_image, self.back_rect.move(0,0))
      self.all_sprites.draw(self.screen)
      # self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, 35) 
      pg.draw.rect(self.screen, RED, (20, 20, (self.player.max_health*10), 5))
      pg.draw.rect(self.screen, GREEN, (20, 20, (self.player.health*10), 5))
      self.draw_text("Player Health: " + str(self.player.health) + "/25", 22, WHITE, 100, 35) 
      for boss in self.boss:
        pg.draw.rect(self.screen, RED, (20, 60, (boss.max_health*10), 5))
        pg.draw.rect(self.screen, GREEN, (20, 60, (boss.health*10), 5))
        self.draw_text("Boss Health: " + str(boss.health) + "/10", 22, WHITE, 95, 75) 
      self.screen.blit(self.player.image, self.player.rect)
      # self.screen.blit(self.boss.image, self.boss.rect)
      self.back_rect.move_ip(-2, 0)
      if self.back_rect.right == 0:
        self.back_rect.x =0
      self.draw_text("Level " + str(self.player.level), 22, WHITE, WIDTH / 2, 15) 
    pg.display.flip()      

  def show_start_screen(self):
    # game splash/start screen
    pg.mixer.music.load(path.join(self.snd_dir, 'prologue.ogg'))
    pg.mixer.music.play(loops = -1)
    self.back_image = pg.image.load('bg/plx-4.png')
    self.back_image = pg.transform.scale(self.back_image, (1400, 720))
    self.back_rect = self.back_image.get_rect()
    self.screen.fill(BLACK)
    self.screen.blit(self.back_image, self.back_rect.move(0,0))
    self.draw_text("Welcome to Metroidvania... Enter if you dare!", 48, WHITE, WIDTH /2, 70)
    self.draw_text("Controls: Right and Left Arrow to move, Up Arrow to jump, Space Bar to shoot, AWSD for directional shooting", 25, WHITE, WIDTH / 2, HEIGHT * 7/8)
    self.draw_text("You ready? Press any key to play", 30, WHITE, WIDTH /2, HEIGHT * 10/11)
    self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH /2, 15)
    pg.display.flip()
    # Wait for player to hit a key to start
    while self.playing == False and self.running == True:
      self.events()
    pg.mixer.music.fadeout(1000)

  def win_screen(self):
    pg.mixer.music.load(path.join(self.snd_dir, 'win.ogg'))
    pg.mixer.music.play(loops = -1)
    self.screen.fill(BLACK)
    self.draw_text("Congrats! You have won!!!", 75, BLUE, WIDTH /2, HEIGHT / 2)
    # self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT /2)
    
    # if self.score > self.highscore:
    #   self.highscore = self.score
    #   self.draw_text("New High Score: " + str(self.highscore), 22, WHITE, WIDTH /2, HEIGHT/2 + 40)
    #   with open(path.join(self.dir, HS_FILE), 'w') as f:
    #     f.write(str(self.score))
    # else: 
    #   self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH /2, HEIGHT/2 + 40)
    pg.display.flip()
    # Wait for player to hit a key to restart game
    while self.playing == True and self.running == True:
      self.events()

  def show_go_screen(self):
    #game over/continue
    pg.mixer.music.load(path.join(self.snd_dir, 'end.ogg'))
    pg.mixer.music.play(loops = -1)
    self.screen.fill(BLACK)
    if self.score < 40:
      self.draw_text("You are pretty bad at this! GAME OVER!!!", 48, RED, WIDTH /2, HEIGHT / 4)
    else:
      self.draw_text("So Close! GAME OVER!", 48, RED, WIDTH /2, HEIGHT / 4)
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
  g.win_screen()
  g.show_go_screen()
  

pg.quit()