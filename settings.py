# game options
TITLE = "Metoidvania"
WIDTH = 1400
HEIGHT = 720
FPS = 60
FONT_NAME = 'arial'

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.5

MAP1_PLATFORM_LIST = [
  # Ground
  (0, HEIGHT - 40, WIDTH, 40),
  (WIDTH/2 - 50, HEIGHT * 3/4, 100, 20),
  (125, HEIGHT - 350, 100, 20),
  (135, 300, 100, 30),
  (350, 400, 100, 20),
  (175, 100, 50, 20),
  (300, 300, 100, 20),
  (-400, 400, 150, 20)
]

MAP2_PLATFORM_LIST = [
  (0, HEIGHT - 40, WIDTH, 40),
  (WIDTH/2 - 50, HEIGHT * 3/4, 100, 20),
  (125, HEIGHT - 350, 100, 20),
  (350, 200, 100, 20),
  (175, 100, 50, 20),
  (155, 350, 100, 30),
]

MAP3_PLATFORM_LIST = [
  (0, HEIGHT - 40, WIDTH, 40),
  (WIDTH/2 - 50, HEIGHT * 3/4, 100, 20),
  (125, HEIGHT - 350, 100, 20),
  (350, 200, 100, 20),
  (175, 100, 50, 20)
]

MAP4_PLATFORM_LIST = [
  (0, HEIGHT - 40, WIDTH, 40),
  (WIDTH/2 - 50, HEIGHT * 3/4, 100, 20),
  (125, HEIGHT - 350, 100, 20),
  (350, 200, 100, 20),
  (175, 100, 50, 20)
]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

key_found = False