# game options
TITLE = "Metoidvania"
WIDTH = 1400
HEIGHT = 720
FPS = 60
FONT_NAME = 'bloddy.ttf'
HS_FILE = 'highscore.txt'
SPRITESHEET = "spritesheet_jumper.png"

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.5

MAP1_PLATFORM_LIST = [
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
  (WIDTH/2 - 50, HEIGHT * 3/4),
  (0, HEIGHT * 3/4),
  (500, HEIGHT /2),
  (750, HEIGHT /2),
  (-400, HEIGHT * 3/4),
  (-200, HEIGHT -350),
  (-100, HEIGHT -500),
  (0, HEIGHT - 700),
]

MAP2_PLATFORM_LIST = [
  (0, HEIGHT - 40),
  (WIDTH/2 - 50, HEIGHT * 3/4),
  (125, HEIGHT - 350),
  (350, 200),
  (175, 100)
]

# MAP3_PLATFORM_LIST = [
#   (0, HEIGHT - 40, WIDTH, 40),
#   (WIDTH/2 - 50, HEIGHT * 3/4, 100, 20),
#   (125, HEIGHT - 350, 100, 20),
#   (350, 200, 100, 20),
#   (175, 100, 50, 20)
# ]

# MAP4_PLATFORM_LIST = [
#   (0, HEIGHT - 40, WIDTH, 40),
#   (WIDTH/2 - 50, HEIGHT * 3/4, 100, 20),
#   (125, HEIGHT - 350, 100, 20),
#   (350, 200, 100, 20),
#   (175, 100, 50, 20)
# ]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)