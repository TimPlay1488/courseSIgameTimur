import sys
import pygame as pg
import time
import random

pg.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
def_font = pg.font.Font(pg.font.get_default_font(), 30)
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

    ball_center = (ball.x + ball.width/2, ball.y + ball.height/2)
    platform_center = (platform.x + platform.width/2, platform.y + platform.height/2)
    text_surface = def_font.render('Some Text', False, (0,255,0))

    if ball.colliderect(platform):
      t = random.Random().random()/2
      collision_vector = (ball_center[0] - platform_center[0], ball_center[1] - platform_center[1])
      BALL_DIRECTION = pg.math.Vector2(collision_vector).normalize()

    if ball.colliderect(TOP_BORDER):
      BALL_DIRECTION = BALL_DIRECTION.reflect(pg.math.Vector2(0,1))

    if ball.colliderect(BOTTOM_BORDER):
      BALL_DIRECTION = BALL_DIRECTION.reflect(pg.math.Vector2(0,-1))

    if ball.colliderect(LEFT_BORDER):
      BALL_DIRECTION = BALL_DIRECTION.reflect(pg.math.Vector2(1,0))

    if ball.colliderect(RIGHT_BORDER):
      BALL_DIRECTION = BALL_DIRECTION.reflect(pg.math.Vector2(-1,0))        

    screen.blit(text_surface, (20,20))
    pg.display.flip()
    clock.tick(FPS)