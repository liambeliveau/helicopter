import random, pygame, sys
from pygame.locals import *
from math import sin, cos, tan

WINDOW_WIDTH=1024
WINDOW_HEIGHT=768
gameState={}
screen=pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
TUNNEL_WIDTH=300.0
TUNNEL_COLOR=(0,200,0)
TUNNEL_COLOR_2=(0,0,200)
HELI_OFFSET=100
FPS=30

def reset():
    global gameState
    gameState={
        "distance":0,
        "height": WINDOW_HEIGHT / 2,
        "horizSpeed":10,
    }

def main():
    reset()
    pygame.init()
    pygame.mixer.init()
    global FPSClock
    FPSClock=pygame.time.Clock()
    pygame.display.set_caption("Helicopter Visualization")
    runGame()

def runGame():
    shouldContinue = True
    while shouldContinue:
        shouldContinue = update()
        draw()

def update():
    """steps forward in game logic"""
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_RETURN:
                    reset()
    gameState["distance"]+=gameState["horizSpeed"]
    FPSClock.tick(FPS)
    return True

def draw():
    """draws game to screen"""
    screen.fill((0,0,0))
    for position in range(WINDOW_WIDTH/5):
        position*=5
        ceil,floor=getBarriers(position+gameState["distance"])
        if position%2.0==0: #every other rect
            #draw ceiling
            pygame.draw.rect(screen, TUNNEL_COLOR, (position, 0, 5, ceil))
            #draw floor
            pygame.draw.rect(screen, TUNNEL_COLOR, (position, floor, 5, WINDOW_HEIGHT-floor))
        else:
            #draw ceiling (color 2)
            pygame.draw.rect(screen, TUNNEL_COLOR_2, (position, 0, 5, ceil))
            #draw floor (color 2
            pygame.draw.rect(screen, TUNNEL_COLOR_2, (position, floor, 5, WINDOW_HEIGHT-floor))
    pygame.display.flip()

def getBarriers(distance):
    """returns position of ceiling and floor for given distance"""
    #fit tunnel to curve
    ceil = (190*cos(distance/300.0)*(sin(distance/1000.0))+200)
    return ceil, ceil+TUNNEL_WIDTH

main()