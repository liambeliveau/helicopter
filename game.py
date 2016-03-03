import random, pygame, sys
from pygame.locals import *
from math import sin, cos

WINDOW_WIDTH=1024
WINDOW_HEIGHT=768
gameState={}
screen=pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
HELI_SIZE=50
HELI_COLOR=(0,0,250)
TUNNEL_WIDTH=300
TUNNEL_COLOR=(50,0,50)
TUNNEL_COLOR_2=(70,0,70)
HELI_OFFSET=100
FPS=30

def reset():
    global gameState
    gameState={
        "distance":0,
        "height": WINDOW_HEIGHT / 2,
        "vertSpeed":0,
        "gameOver":False,
        "horizSpeed":4,
        "vertAccel":0.3
    }

def main():
    reset()
    pygame.init()
    pygame.mixer.init()
    global FPSClock, font, gameOverFont, flySound, deathSound
    FPSClock=pygame.time.Clock()
    font=pygame.font.Font('font.ttf',20)
    gameOverFont=pygame.font.Font('font.ttf',40)
    flySound=pygame.mixer.Sound("fwip.wav")
    deathSound=pygame.mixer.Sound("boom.wav")
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
            gameState["vertSpeed"]-=gameState["vertAccel"]
            if not pygame.mixer.get_busy():
                flySound.play()
        else:
            gameState["vertSpeed"]+=gameState["vertAccel"]
        gameState["height"]+=gameState["vertSpeed"]
        gameState["distance"]+=gameState["horizSpeed"]
        if getCollision():
            deathSound.play()
            gameState["gameOver"]=True
        gameState["horizSpeed"]+=0.01
        gameState["vertAccel"]+=0.0001
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
    #draw helicopter
    pygame.draw.rect(screen, HELI_COLOR, (HELI_OFFSET, gameState["height"] - HELI_SIZE / 2, HELI_SIZE, HELI_SIZE))
    score=font.render('Distance: '+str(gameState["distance"]), True, (200,200,200))
    screen.blit(score, (0,0))
    if gameState["gameOver"]:
        gameOver=gameOverFont.render('GAME OVER! Press enter to restart.', True, (200,200,200))
        screen.blit(gameOver,(50 ,WINDOW_HEIGHT/2-20))
    pygame.display.flip()

def getBarriers(distance):
    """returns position of ceiling and floor for given distance"""
    #fit tunnel to curve
    ceil = (190*sin(distance/300.0)*(cos(distance/1000.0))+200)
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