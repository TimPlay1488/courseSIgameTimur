import sys
import pygame as pg
import time
import random
import pygame.mixer as mixer

mixer.init()

pg.init()

WHITE = (0, 0, 0)
BLACK = (255, 255, 255)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800


def_font = pg.font.Font(pg.font.get_default_font(), 30)

TOP_BORDER = pg.Rect(0,0,SCREEN_WIDTH,1)
BOTTOM_BORDER = pg.Rect(0,SCREEN_HEIGHT,SCREEN_WIDTH,1)
LEFT_BORDER = pg.Rect(0,0,1, SCREEN_HEIGHT)
RIGHT_BORDER = pg.Rect(SCREEN_WIDTH,0,1,SCREEN_HEIGHT)

PLATFORM_WIDTH = 200
PLATFORM_HEIGHT = 30
BALL_WIDTH = 30
BALL_HEIGHT = 30
sound_obj = pg.mixer.Sound("est-probitie.mp3")
sound_over = pg.mixer.Sound("ne-probil.mp3")
sound_background = pg.mixer.Sound("kahoot-lobby-music_v7NLkTEl.ogg")

def game(screen, clock, assets):
  
  COUNTER = 0

  PLATFORM_X = (SCREEN_WIDTH - PLATFORM_WIDTH) // 2
  PLATFORM_Y = int(SCREEN_HEIGHT * 0.8)
  PLATFORM_SPEED = 3

  BALL_X = (SCREEN_WIDTH - PLATFORM_WIDTH) // 2
  BALL_Y = 90
  BALL_SPEED = 4
  BALL_DIRECTION = pg.math.Vector2(1,1).normalize()

  FPS = 120

  sound_background.play(1)

  while True:
      for i in pg.event.get():
          if i.type == pg.QUIT:
              sys.exit()

      keys = pg.key.get_pressed()

      
      if keys[pg.K_LEFT]:
          PLATFORM_X -= 3
          PLATFORM_X = max(0, PLATFORM_X)
      if keys[pg.K_RIGHT]:
          PLATFORM_X += 3
          PLATFORM_X = min(SCREEN_WIDTH - PLATFORM_WIDTH, PLATFORM_X)

      speed_vector = BALL_DIRECTION * BALL_SPEED
      BALL_Y += speed_vector.y
      BALL_X += speed_vector.x
      
      # screen.fill(WHITE)
      screen.blit(assets['background'],(0,0))


      platform = assets['panel'].get_rect()
      platform.x = PLATFORM_X
      platform.y = PLATFORM_Y
      #platform = pg.Rect(PLATFORM_X, PLATFORM_Y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
      #pg.draw.rect(screen, BLACK, platform)
      screen.blit(assets['panel'], platform)


      ball = assets['ball'].get_rect()
      ball.x = BALL_X
      ball.y = BALL_Y

      screen.blit(assets['ball'], ball)

      # ball = pg.Rect(BALL_X, BALL_Y, BALL_WIDTH, BALL_HEIGHT)
      # pg.draw.rect(screen, BLACK, ball)

      ball_center = (ball.x + ball.width/2, ball.y + ball.height/2)
      platform_center = (platform.x + platform.width/2, platform.y + platform.height/2)
      text_surface = def_font.render(str(COUNTER), False, (0,255,0))

      if ball.colliderect(platform):
        sound_obj.play()
        t = random.Random().random()/2
        collision_vector = (ball_center[0] - platform_center[0], ball_center[1] - platform_center[1])
        BALL_DIRECTION = pg.math.Vector2(collision_vector).normalize()
        COUNTER += 1

      if ball.colliderect(TOP_BORDER):
        BALL_DIRECTION = BALL_DIRECTION.reflect(pg.math.Vector2(0,1))

      if ball.colliderect(BOTTOM_BORDER):
        break

      if ball.colliderect(LEFT_BORDER):
        BALL_DIRECTION = BALL_DIRECTION.reflect(pg.math.Vector2(1,0))

      if ball.colliderect(RIGHT_BORDER):
        BALL_DIRECTION = BALL_DIRECTION.reflect(pg.math.Vector2(-1,0))  

      screen.blit(text_surface, (20,20))
      pg.display.flip()
      clock.tick(FPS)

if __name__ == '__main__':
  screen_out = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  assets = {
     'ball': pg.transform.scale(pg.image.load('ball.png').convert_alpha(), (BALL_WIDTH, BALL_HEIGHT)),
     'background': pg.transform.scale(pg.image.load('background.png').convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT)),
     'panel': pg.transform.scale(pg.image.load('panel.png').convert_alpha(), (PLATFORM_WIDTH, PLATFORM_HEIGHT)),
  }

  clock_out = pg.time.Clock()
  while True:
    game(screen_out, clock_out, assets)
    finish_text = def_font.render('Game Over', False, (0, 255, 0))
    screen_out.blit(finish_text, (SCREEN_WIDTH/2-30, SCREEN_HEIGHT/2))
    pg.display.flip()
    sound_over.play()
    while True:
      for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
      keys = pg.key.get_pressed()
      if keys[pg.K_r]:
        break