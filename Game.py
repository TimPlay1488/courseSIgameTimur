import sys
import pygame as pg
import time
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
TOP_BORDER = pg.Rect(0,0,SCREEN_WIDTH,1)
BOTTOM_BORDER = pg.Rect(0,SCREEN_HEIGHT,SCREEN_WIDTH,1)
LEFT_BORDER = pg.Rect(0,0,1, SCREEN_HEIGHT)
RIGHT_BORDER = pg.Rect(SCREEN_WIDTH,0,1,SCREEN_HEIGHT)

PLATFORM_WIDTH = 200
PLATFORM_HEIGHT = 30
PLATFORM_X = (SCREEN_WIDTH - PLATFORM_WIDTH) // 2
PLATFORM_Y = int(SCREEN_HEIGHT * 0.8)
PLATFORM_SPEED = 3

BALL_WIDTH = 30
BALL_HEIGHT = 30
BALL_X = (SCREEN_WIDTH - PLATFORM_WIDTH) // 2
BALL_Y = 90
BALL_SPEED = 3
BALL_DIRECTION = pg.math.Vector2(1,1).normalize()

FPS = 120

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
    
    screen.fill(WHITE)

    platform = pg.Rect(PLATFORM_X, PLATFORM_Y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    pg.draw.rect(screen, BLACK, platform)

    ball = pg.Rect(BALL_X, BALL_Y, BALL_WIDTH, BALL_HEIGHT)
    pg.draw.rect(screen, BLACK, ball)

    if ball.colliderect(platform):
      t = random.Random().random()/2
      print(t)
      BALL_DIRECTION = BALL_DIRECTION.reflect(pg.math.Vector2(t,-1).normalize())

    if ball.colliderect(TOP_BORDER):
      BALL_DIRECTION = BALL_DIRECTION.reflect(pg.math.Vector2(0,1))

    if ball.colliderect(BOTTOM_BORDER):
      BALL_DIRECTION = BALL_DIRECTION.reflect(pg.math.Vector2(0,-1))

    if ball.colliderect(LEFT_BORDER):
      BALL_DIRECTION = BALL_DIRECTION.reflect(pg.math.Vector2(1,0))

    if ball.colliderect(RIGHT_BORDER):
      BALL_DIRECTION = BALL_DIRECTION.reflect(pg.math.Vector2(-1,0))        

    # if BALL_Y < 0:
    #     BALL_SPEED = -BALL_SPEED

    # if BALL_Y > 750:
    #     BALL_SPEED = -BALL_SPEED
    #     sys.exit()

    pg.display.flip()

    clock.tick(FPS)