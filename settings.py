# game options
TITLE = "Metoidvania"
WIDTH = 1080
HEIGHT = 720
FPS = 60

FONT_NAME = 'bloddy.ttf'
HS_FILE = 'highscore.txt'

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.5
PLAYER_JUMP = 15
PLAYER_HEALTH = 25

HAS_KEY = False

# Enemy properties
SPIDER_SPRITESHEET = "spiders.png"
<<<<<<< HEAD
EXPLOSION_SPRITESHEET = "explosion_sheet.png"
=======
BOSS_ACC = 0.5
BOSS_GRAV = 0
BOSS_HEALTH = 25

>>>>>>> bac4a6b736115764e4998355e16d6938b371c52e
# Globals for tracking directions
LEFT = 0
UP = 1
RIGHT = 2
DOWN = 4

#Starting Platforsms
PLATFORM_HEIGHT = 20
PLATFORM_WIDTH = 100
PLATFORM_SPRITESHEET = "spritesheet_jumper.png"

# Starting platforms
MAP1_PLATFORM_LIST = [
  (WIDTH/2 - 50, HEIGHT * 3/4),
  (125, HEIGHT - 350),
  (350, 200),
  (175, 100)
]

MAP2_PLATFORM_LIST = [
  (0, 250),
  (WIDTH/2 - 50, HEIGHT * 3/4),
  (350, 200),
  (175, 100),
  (700, 100),
  (155, 400),
  (400, 400),
]

MAP3_PLATFORM_LIST = [
    (WIDTH/2 - 50, 400),
    
    (WIDTH/2 - 250, 600),
    (WIDTH/2 + 150, 400),
    
    (WIDTH/2 - 50, 300),
    
    (WIDTH/2 - 350, 250),
    (WIDTH/2 + 250, 250),

    (WIDTH/2 - 250, 100),
    (WIDTH/2 + 150, 100),

    (WIDTH/2 - 50, -50),

    (WIDTH/2 - 250, -200),
    (WIDTH/2 + 150, -200),
    
    (WIDTH/2 - 50, -350),
    
    (WIDTH/2 - 350, -500),
    (WIDTH/2 + 250, -500),

    (WIDTH/2 - 250, -650),
    (WIDTH/2 + 150, -650),
    
    (WIDTH/2 - 50, -700),

    (WIDTH/2 - 250, -850),
    (WIDTH/2 + 150, -850),
    
    (WIDTH/2 - 50, -1050),
    
    (WIDTH/2 - 350, -1200),
    (WIDTH/2 + 250, -1200),

    (WIDTH/2 - 250, -1350),
    (WIDTH/2 + 150, -1350),
]

MAP4_PLATFORM_LIST = [
  (1200, HEIGHT - 40),
  (1050, HEIGHT - 40),
  (900, HEIGHT - 40),
  (750, HEIGHT - 40),
  (600, HEIGHT - 40),
  (450, HEIGHT - 40),
  (300, HEIGHT - 40),  
  (150, HEIGHT - 40),
  (0, HEIGHT - 40),
  (-150, HEIGHT - 40),
  (0, HEIGHT * 3/4),
  (400, HEIGHT /2),
  (750, HEIGHT /2),
  (-400, HEIGHT * 3/4),
  (-200, HEIGHT -350),
  (-100, HEIGHT -500),
  (0, HEIGHT - 700),
]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GOLD = 	(255,215,0)
SILVER = (192,192,192)