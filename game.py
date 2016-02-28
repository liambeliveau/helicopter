import random, pygame, sys
from pygame.locals import *
from math import sin

WINDOW_WIDTH=1024
WINDOW_HEIGHT=768
gameState={}
screen=pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
HELI_SIZE=50
VERT_ACCEL=0.3
HORIZ_SPEED=9
TUNNEL_WIDTH=300
TUNNEL_COLOR=(200,0,200)
HELI_OFFSET=100

def reset():
    global gameState
    gameState={
        "distance":0,
        "height": WINDOW_HEIGHT / 2,
        "vertSpeed":0,
        "gameOver":False
    }

def main():
    reset()
    pygame.init()
    global font
    global gameOverFont
    font=pygame.font.Font('font.ttf',20)
    gameOverFont=pygame.font.Font('font.ttf',40)
    pygame.display.set_caption("Helicopter")
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
                if event.key == pygame.K_RETURN and gameState["gameOver"]:
                    reset()
    if not gameState["gameOver"]:
        keyState=pygame.key.get_pressed()
        if keyState[K_SPACE]==True:
            gameState["vertSpeed"]-=VERT_ACCEL
        else:
            gameState["vertSpeed"]+=VERT_ACCEL
        gameState["height"]+=gameState["vertSpeed"]
        gameState["distance"]+=HORIZ_SPEED
        if getCollision():
            gameState["gameOver"]=True

    return True

def draw():
    """draws game to screen"""
    screen.fill((0,0,0))
    for position in range(WINDOW_WIDTH/5):
        position*=5
        ceil,floor=getBarriers(position+gameState["distance"])
        #draw ceiling
        pygame.draw.rect(screen, TUNNEL_COLOR, (position, 0, 5, ceil))
        #draw floor
        pygame.draw.rect(screen, TUNNEL_COLOR, (position, floor, 5, WINDOW_HEIGHT-floor))
    #draw helicopter
    pygame.draw.rect(screen, (0,0,250), (HELI_OFFSET, gameState["height"] - HELI_SIZE / 2, HELI_SIZE, HELI_SIZE))
    score=font.render('Distance: '+str(gameState["distance"]), True, (200,200,200))
    screen.blit(score, (0,0))
    if gameState["gameOver"]:
        gameOver=gameOverFont.render('GAME OVER! Press enter to restart.', True, (200,200,200))
        screen.blit(gameOver,(50 ,WINDOW_HEIGHT/2-20))
    pygame.display.flip()

def getBarriers(distance):
    """returns position of ceiling and floor for given distance"""
    #fit tunnel to curve
    ceil = 190*sin(distance/300.0)+200
    return ceil, ceil+TUNNEL_WIDTH

def getCollision():
    """returns true if helicopter is colliding with ceiling or floor"""
    #for each x-pixel in helicopter, test collision
    for xPixel in range(HELI_SIZE):
        ceil,floor=getBarriers(gameState["distance"]+HELI_OFFSET+xPixel)
        #check against ceiling
        if ceil>=gameState["height"]-(HELI_SIZE/2):
            return True
        #check against floor
        if floor<=gameState["height"]+(HELI_SIZE/2):
            return True
    return False

main()