import pygame, sys, time, random, winsound
from pygame.locals import *

#initializing pygame and the clock and the mixer(?)
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
mainClock = pygame.time.Clock()

#constants
SIZE = 20
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
FPS = 60
G = 0.3
F = 0.9
J = 6
S = 5
MAXS = 9
epsilon = 0.1

#keys
keys = pygame.key.get_pressed()

#initializing window
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)

#caption of the window
pygame.display.set_caption('Running_window')

#One font
basicFont = pygame.font.SysFont("Comic Sans MS", 60)

#some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (127,127,127)

#classes

class Character :

    def __init__(self, x, y):

        self.dx = 0 #Speed of the character
        self.dy = 0

        self.image = pygame.image.load("game/persoRight.bmp").convert() #load the character image
        self.image.set_colorkey(GREY)  #set the transparent color = grey

        self.rect = self.image.get_rect() #create the rectangle associated with the character
        self.rect.left = x
        self.rect.bottom = y
        self.win = True
        self.coins = 0
        self.coinSound = pygame.mixer.Sound('sounds/coin.wav')
        self.allCoins = False
        
        self.dead = False
        self.deadSound = pygame.mixer.Sound('sounds/dead.wav')
        self.touchGround = True
        self.lives = 5
        
        self.imageLives = pygame.image.load("game/lives.bmp").convert()
        self.imageLives.set_colorkey(GREY)
        
        self.imageCoins = pygame.image.load("game/coin.bmp").convert()
        self.imageCoins.set_colorkey(GREY)
        
        self.imageCross = pygame.image.load("game/x.bmp").convert()
        self.imageCross.set_colorkey(GREY)
        
        self.imageNumberOfCoins = pygame.image.load("game/2.bmp").convert()
        self.imageNumberOfCoins.set_colorkey(GREY)
        
        self.jumpSound = pygame.mixer.Sound('sounds/jump.wav')

    def move(self, collisionList) :

        #moves the character after calling all the methods which concerns the moving
        self.grav()
        #self.friction()
        
        self.rect.x += self.dx
        self.collisionX(collisionList)
        
        
        self.rect.y += self.dy
        self.collisionY(collisionList)

        if self.dead :
            self.lives += -1
        

    def moveRight(self):

        #moves the character to the Right and changes the character image accordingly
        
        self.dx = S

    def moveLeft(self):
        
        #moves the character to the Left and changes the character image accordingly
        self.dx = -S

    def jump(self, collisionList):

        #checks for ground and make the character jump or not accordingly
        self.rect.y += 1
        if self.rect.bottom >= WINDOWHEIGHT : #bottom ground
            self.rect.bottom = WINDOWHEIGHT - 1 #Because the collision(self) makes self.y = 580 if self.y >= 580
            self.dy = -J #jump speed
            self.jumpSound.play()
        else :
            for c in collisionList :
                if c[1] == 't':
                    if c[0].rect.colliderect(self.rect) :
                        self.rect.bottom = c[0].rect.top - 1
                        self.dy = -J
                        self.jumpSound.play()
        self.rect.y -=1

    def stop(self):

        #stops the character from moving sideways
        char.dx = 0

    def grav(self) :

        #applies gravity on the character
        self.dy += G

        if self.dy <= -MAXS :
            self.dy = -MAXS
        elif self.dy >= MAXS :
            self.dy = MAXS

        if self.rect.bottom >= WINDOWHEIGHT and self.dy >= 0:
            self.dy = 0
            self.rect.bottom = WINDOWHEIGHT

    def friction(self) :
        
        #Applies friction to the character. Doesn't really work as intended
        self.dy = self.dy*F
        self.dx = self.dx*F

    def collisionX(self, level) :
        
        for c in level.collisionList :
            if c[0].rect.colliderect(self.rect) :
                if c[1] == 't':
                    if self.dx > 0 :
                        self.rect.right = c[0].rect.left   
                    elif self.dx < 0 :
                        self.rect.left = c[0].rect.right
                if c[1] == 'd':
                    if self.allCoins :
                        self.win = True
                if c[1] == 'm' :
                    c[0].sound.play()
                    self.dy = -1.5*J
                if c[1] == 'c' :
                    self.coinSound.play()
                    level.collisionList.remove(c)
                    self.addCoin(level.numberOfCoins)
                if c[1] == 's' :
                    self.dead = True
                    char.deadSound.play()
                

        if self.rect.left <= 0 :
            self.rect.left = 0
        elif self.rect.right >= WINDOWWIDTH:
            self.rect.right = WINDOWWIDTH
                    
                    
                
        
    def collisionY(self, level) :
                
        #check for collision and modifies the speend and the position accordingly
        for c in level.collisionList :
            if c[0].rect.colliderect(self.rect) :
                if c[1] == 't':
                    if self.dy > 0 :
                        self.rect.bottom = c[0].rect.top 
                        self.dy = 0
                    if self.dy < 0 :
                        self.rect.top = c[0].rect.bottom
                        self.dy = 0
                if c[1] == 'd':
                    if self.allCoins :
                        self.win = True
                if c[1] == 'm' :
                    self.dy = -1.5*J
                    c[0].sound.play()
                if c[1] == 'c' :
                    self.coinSound.play()
                    level.collisionList.remove(c)
                    self.addCoin(level.numberOfCoins)
                if c[1] == 's' :
                    self.dead = True
                    char.deadSound.play()

    def draw(self, collisionList) :
        if self.touchGround :
            if self.dx > 0 :
                self.image = pygame.image.load("game/persoRight.bmp")
                self.image.set_colorkey(GREY)
            elif self.dx < 0 :
                self.image = pygame.image.load("game/persoLeft.bmp")
                self.image.set_colorkey(GREY)

        
        
        for i in range(self.lives - 1) :
            windowSurface.blit(self.imageLives, ((i+2)*SIZE, 1.5*SIZE))

        windowSurface.blit(self.imageCoins, (2*SIZE, SIZE*3))
        windowSurface.blit(self.imageCross, (3*SIZE, SIZE*3))
        windowSurface.blit(self.imageNumberOfCoins, (4*SIZE, SIZE*3))
            
        windowSurface.blit(self.image, self.rect) #blit the character onto the surface

    def addCoin(self, numberOfCoins) :
        self.coins += 1
        if self.coins == numberOfCoins :
            self.allCoins = True
            self.coins = 0


class Stuff :

    def __init__(self, X, Y, stuffName) :

        self.X = X
        self.Y = Y 
        self.stuffName = stuffName
        self.image = pygame.image.load('game/' + self.stuffName + ".bmp")
        self.image.set_colorkey(GREY)  #set the transparent color = grey
        self.rect = self.image.get_rect() #create the rectangle associated with the platform
        self.rect.left = SIZE*(self.X) 
        self.rect.bottom = SIZE*(self.Y+1)

    def draw(self) :
        
        windowSurface.blit(self.image, self.rect)


class Platform(Stuff) :

    def __init__(self, X, Y) :

        Stuff.__init__(self, X, Y, "platform")
        

class Door(Stuff) :

    def __init__(self, X, Y) :

        Stuff.__init__(self, X, Y, "door1")

    def draw(self) :
        
        windowSurface.blit(self.image, self.rect)
        self.image = pygame.image.load('game/' + self.stuffName + ".bmp")

class Jumper(Stuff) :

    def __init__(self, X, Y) :

        Stuff.__init__(self, X, Y, "jumper")
        self.sound = pygame.mixer.Sound('sounds/jumper.wav')
        

class Coin(Stuff) :

    def __init__(self, X, Y) :

        Stuff.__init__(self, X, Y, "coin")

class Background(Stuff):

    def __init__(self, X, Y) :

        Stuff.__init__(self, X, Y, "bg")

class Spikes(Stuff):

    def __init__(self, X, Y) :

        Stuff.__init__(self, X, Y, "spikes")        
    

class Level :

        def __init__(self,levelNumber):
                
                self.levelName = 'levels/level' + str(levelNumber) + '.txt'
                self.levelList = []
                self.collisionList = []
                self.numberOfCoins = 0

        def readMap(self):

                f = open(self.levelName, 'r')

                g = list(f)

                l = []
                for s in g :
                    l +=[list(s)]

                for i in range(len(l)-1) :
                    l[i].pop()
                return l

        def createLevelPlatformList(self):
                self.levelList = self.readMap()
                
                for j in range(len(self.levelList)):
                        for i in range(len(self.levelList[j])):
                                if self.levelList[j][i] == 't' :
                                        self.collisionList.append((Platform(i,j), 't'))
                                elif self.levelList[j][i] == 'd' :
                                        self.collisionList.append((Door(i,j), 'd'))
                                elif self.levelList[j][i] == 'm' :
                                        self.collisionList.append((Jumper(i,j), 'm'))
                                elif self.levelList[j][i] == 'c' :
                                        self.collisionList.append((Coin(i,j), 'c'))
                                        self.numberOfCoins += 1
                                elif self.levelList[j][i] == 's' :
                                        self.collisionList.append((Spikes(i,j), 's'))
            
        def set_LevelPlatformList(self):
                self.createLevelPlatformList()
        
currentLevel = 0

char = Character(20,500) #create a character

levelBackground = pygame.image.load('game/bg.bmp')
levelBackground.set_colorkey(GREY) #create the background surface
menuBackground = pygame.image.load('menu/bg.bmp')
menuBackground.set_colorkey(GREY)
victoryBackground = pygame.image.load('menu/victory.bmp')
victoryBackground.set_colorkey(GREY)
gameOverBackground = pygame.image.load('menu/gameOver.bmp')
gameOverBackground.set_colorkey(GREY)

inGame = False
inMenu = True
victory = False
gameOver = False
#main loop
while True:

        if inGame :
            for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYUP:
                            if event.key == K_LEFT and char.dx < 0:
                                char.stop()
                            if event.key == K_RIGHT and char.dx > 0:
                                char.stop()
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                                inGame = False
                                inMenu = True
                        if event.key == K_LEFT :
                            char.moveLeft()
                        if event.key == K_RIGHT :
                            char.moveRight()
                        if event.key == K_UP :
                            char.jump(level.collisionList)

            if char.win :
                if currentLevel < 5 :
                    currentLevel +=1
                    level = Level(currentLevel)
                    level.set_LevelPlatformList()
                    char.rect.bottom = 560
                    char.rect.left = 20
                    char.allCoins = False
                    char.win = False
                else :
                    victory = True
                    inGame = False
                    inMenu = False
            
            
            if char.allCoins :
                for c in level.collisionList :
                    if c[1] == 'd' :
                        c[0].stuffName = 'door2'

            if char.dead :
                pygame.time.wait(100)
                level = Level(currentLevel)
                level.set_LevelPlatformList()
                char.rect.bottom = 560
                char.rect.left = 20
                char.coins = 0
                char.allCoins = False
                char.dead = False

            if char.lives == 0 :
                currentLevel = 0
                char = Character(20,500)
                inGame = False
                inMenu = False
                gameOver = True
                victory = False

            windowSurface.blit(levelBackground, (0,0))
                
                    
            
            for plat in level.collisionList :
                plat[0].draw()
        
            char.draw(level.collisionList) #draw the character
            char.move(level)

        elif inMenu:
            for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN :
                        if event.key == K_ESCAPE :
                            pygame.quit()
                            sys.exit()
                        if event.key == K_SPACE :
                            inMenu = False
                            inGame = True
            windowSurface.blit(menuBackground, (0,0))

        elif victory:
            for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN :
                        if event.key == K_ESCAPE :
                            pygame.quit()
                            sys.exit()
                        if event.key == K_SPACE :
                            inMenu = True
                            inGame = False
                            victory = False
                            gameOver = False
                            currentLevel = 0
                            char = Character(20,500)
            windowSurface.blit(victoryBackground, (0,0))

        elif gameOver:
            for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN :
                        if event.key == K_ESCAPE :
                            pygame.quit()
                            sys.exit()
                        if event.key == K_SPACE :
                            inMenu = True
                            inGame = False
                            victory = False
                            gameOver = False
                            currentLevel = 0
                            char = Character(20,500)
            windowSurface.blit(gameOverBackground, (0,0))
        

            

            #update the screen
        pygame.display.flip()

            #make the clock tick
        mainClock.tick(FPS)
