import pygame
import random
import time
from map import Map
from bullet import Bullet
from algorithms import SA


pygame.init()
win = pygame.display.set_mode((1500, 900))
pygame.display.set_caption('Tanks')


class Tank():
    def __init__(self, x, y, cellSize = 100, width = 100, height = 100, speed = 5, direction = 2, player = 2, error = 20):
        self.x = x * cellSize
        self.y = y * cellSize
        self.width = width
        self.height = height
        self.speed = speed
        self.direction = direction
        self.player = player
        self.kd = 0
        self.playerIm = []
        self.state = 0
        self.error = error
        if player == 1:
            self.playerIm =   [ pygame.image.load('Images/Player1.png'), pygame.image.load('Images/Player2.png'), 
                                pygame.image.load('Images/Player3.png'), pygame.image.load('Images/Player4.png')]
        else:
            self.playerIm =   [ pygame.image.load('Images/Enemy1.png'), pygame.image.load('Images/Enemy2.png'), 
                                pygame.image.load('Images/Enemy3.png'), pygame.image.load('Images/Enemy4.png')]

        
        
    def move(self):
        if self.direction == 0:
            self.moveUp()
        elif self.direction == 1:
            self.moveRight()
        elif self.direction == 2:
            self.moveDown()
        else:
            self.moveLeft()


    def moveLeft(self):
        self.direction = 3

        if self.x > 0 and map.checkObstacle(self.x-self.speed + self.error // 2, self.y + self.error // 2, self.width - self.error, self.height - self.error) == 0:
            self.x -= self.speed

            for tank in enemies:
                if not tank == self and checkEntityCollision(self, tank):
                    self.x += self.speed
                    return

            if not player == self and checkEntityCollision(self, player):
                    self.x += self.speed
                    return
            
            
            
        

    def moveRight(self):
        self.direction = 1

        if self.x < win.get_width() - self.width and map.checkObstacle(self.x + self.speed + self.error // 2, self.y + self.error // 2, self.width - self.error, self.height - self.error) == 0:
            self.x += self.speed
            for tank in enemies:
                if not tank == self and checkEntityCollision(self, tank):
                    self.x -= self.speed
                    return

            if not player == self and checkEntityCollision(self, player):
                    self.x -= self.speed
                    return
        

    def moveUp(self):
        self.direction = 0

        if self.y > 0 and map.checkObstacle(self.x + self.error // 2, self.y-self.speed + self.error // 2, self.width - self.error, self.height - self.error) == 0:
            self.y -= self.speed
            for tank in enemies:
                if not tank == self and checkEntityCollision(self, tank):
                    self.y += self.speed
                    return

            if not player == self and checkEntityCollision(self, player):
                self.y += self.speed
                return
            
        

    def moveDown(self):
        self.direction = 2

        if  self.y < win.get_height() - self.height and map.checkObstacle(self.x + self.error // 2, self.y + self.speed + self.error // 2, self.width - self.error, self.height - self.error) == 0:
            self.y += self.speed
            for tank in enemies:
                if not tank == self and checkEntityCollision(self, tank):
                    self.y -= self.speed
                    return
            if not player == self and checkEntityCollision(self, player):
                self.y -= self.speed
                return

                
            
        
        
    def draw(self, win):
        win.blit(self.playerIm[self.direction], (self.x + (map.cellSize - self.width) / 2, self.y + (map.cellSize - self.height) / 2))

    def shoot(self):
        if self.kd == 0:
            self.kd = 20
            return Bullet(self.x, self.y, self.direction, self.player)
        return None

    def recalcKd(self):
        if self.kd > 0:
            self.kd -= 1

def checkEntityCollision(entity1, entity2):
    if isIn(entity1, entity2.x, entity2.y) or isIn(entity1, entity2.x, entity2.y + entity2.height - 1):
        return True
    
    if isIn(entity1, entity2.x + entity2.width - 1, entity2.y) or isIn(entity1, entity2.x + entity2.width - 1, entity2.y + entity2.height - 1):
        return True

    return False
    
def isIn(t, x, y):
    if (x >= t.x and x < t.x + t.width) and (y >= t.y and y < t.y + t.height):
        return True
    return False
      
def drawWindow(allTime):
    win.fill((0, 0, 0))
    for row in range(9):
        for coll in range(15):
            win.blit(map.bg[map.terrain[row][coll]], (coll*map.cellSize, row*map.cellSize))

    colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]
    radius = [20, 15, 10]
    for i in range(3):
        for pair in SA.getHighlights()[i]:
            pygame.draw.circle(win, colors[i], (pair[0] * 100 + 50, pair[1] * 100 + 50), radius[i])

    f = pygame.font.SysFont("Arial", 60)
    if (SA.getAlgorithm() == 0):
        textTime = f.render("DFS time: " + str(allTime), True, (64, 0, 128))
    elif (SA.getAlgorithm() == 1):
        textTime = f.render("BFS time: " + str(allTime), True, (64, 0, 128))
    elif (SA.getAlgorithm() == 2):
        textTime = f.render("UCS time: " + str(allTime), True, (64, 0, 128))
    

    player.draw(win)
    
    for tank in enemies:
        tank.draw(win)
    
    for bullet in bullets:
        bullet.draw(win)

    for i in range(lives):
        win.blit(healthPoint, (1300 + 70 * i, 20))

    pygame.draw.rect(win, (255, 255, 255), (1000, 800, 500, 100))
    win.blit(textTime, (1050, 820))



    pygame.display.update()

def drawMenu():
    win.fill((0, 0, 0))
    win.blit(bgMenu, (0, 0))

    f = pygame.font.SysFont("Arial", 60)
    position = 700
    if whyYouInMenu == 0:
        text = f.render("MENU", (0, 255, 0), (64, 0, 128))
        position = 705
    if whyYouInMenu == 1:
        text = f.render("PAUSE", (0, 255, 0), (64, 0, 128))
        position = 700
    elif whyYouInMenu == 2:
        text = f.render("YOU LOSE", (0, 255, 0), (64, 0, 128))
        position = 645
    elif whyYouInMenu == 3:
        text = f.render("YOU WON", (0, 255, 0), (64, 0, 128))
        position = 670

    color = (0, 0, 255)

    text1 = f.render("Level 1", (0, 255, 0), color)
    text2 = f.render("Level 2", (0, 255, 0), color)
    text3 = f.render("Level 3", (0, 255, 0), color)
    text4 = f.render("Random Level", (0, 255, 0), color)

    if selectedLevel == 1:
        text1 = f.render("Level 1", (0, 255, 0), (255, 255, 255))
    elif selectedLevel == 2:
        text2 = f.render("Level 2", (0, 255, 0), (255, 255, 255))
    elif selectedLevel == 3:
        text3 = f.render("Level 3", (0, 255, 0), (255, 255, 255))
    elif selectedLevel == 4:
        text4 = f.render("Random Level", (0, 255, 0), (255, 255, 255))
    
    win.blit(text, (position, 235))
    win.blit(text1, (700, 330))
    win.blit(text2, (700, 430))
    win.blit(text3, (700, 530))
    win.blit(text4, (620, 625))

    pygame.display.update()

def setLevel(level):
    lives = 3
    bullets = []

    if level == 1:
        map = Map(open("level1.txt", "r"))
        player = Tank(1, 1, direction = 2, player = 1)
        enemies = [Tank(11, 0), Tank(5, 2), Tank(11,6)]#, Tank(13, 7)

    elif level == 2:
        map = Map(open("level2.txt", "r"))
        player = Tank(1, 3, direction = 2, player = 1)
        enemies = [ Tank(3, 1), Tank(3, 8), Tank(5, 2)] #, Tank(13, 1), Tank(11,2), Tank(13, 7)

    elif level == 3:
        map = Map(open("level3.txt", "r"))
        player = Tank(7, 4, direction = 1, player = 1)
        enemies = [ Tank(1, 1), Tank(13, 4), Tank(12, 5)] #, Tank(6, 7), Tank(4, 7), Tank(1,6), Tank(13, 1)
    
    elif level == 4:
        Map.generateMap()
        map = Map(open("level4.txt", "r"))
        enemies = []
        player = None
        usedPos = []
        tanks = 0
        while tanks < 4:
            x = random.randint(0, 14)
            y = random.randint(0, 8)

            if map.terrain[y][x] in [0, 1, 8] and not((x, y)  in usedPos):
                if tanks == 0:
                    player = Tank(x, y, direction = random.randint(0, 3), player = 1)
                    usedPos.append((x, y))
                else:
                    enemies.append(Tank(x, y, direction = random.randint(0, 3)))
                    usedPos.append((x, y))
                tanks += 1
                
                

    return lives, bullets, map, player, enemies
        
def processBullets(isMainMenu, whyYouInMenu, lives):
    for bullet in bullets:
            id = map.checkObstacle(bullet.x, bullet.y, bullet.width, bullet.height)
            if id == 1 or id == 2:
                
                if id == 2 and random.randint(0, 1) == 0:
                    map.destroyWall(bullet.x, bullet.y, bullet.width, bullet.height)

                bullets.pop(bullets.index(bullet))
            
            else:
                for tank in enemies:
                    if checkEntityCollision(tank, bullet) and tank.player != bullet.isShotByPlayer:
                        bullets.pop(bullets.index(bullet))
                        enemies.pop(enemies.index(tank))
                        break
                if checkEntityCollision(player, bullet) and player.player != bullet.isShotByPlayer:
                        bullets.pop(bullets.index(bullet))
                        lives -= 1
                        if lives <= 0:
                            isMainMenu = True
                            whyYouInMenu = 2
            bullet.move()
    
    return isMainMenu, whyYouInMenu, lives

def processTanks():
    for tank in enemies:
            tank.recalcKd()

            if random.randint(0, 100) == 0:
                tank.direction = random.randint(0, 3)
            elif random.randint(0, 50) == 0:
                tank.state = random.randint(0, 1)
                
            if tank.state == 1:
                tank.move()
            
            if random.randint(0, 50) == 0:
                t = tank.shoot()

                if not t == None:
                    bullets.append(t)

def isMarked(marked, x, y):
    if x < 0 or x > 14 or y < 0 or y > 8 or marked[y][x] == 1:
        return 1
    else:
        return 0



lives, bullets, map, player, enemies = setLevel(4)


run = True
isMainMenu = True
whyYouInMenu = 0
selectedLevel = 1
currentLevel = 1


clock = pygame.time.Clock()

healthPoint = pygame.image.load("Images/Heart.png")
bgMenu = pygame.image.load("Images/BgMenu.png")

while run:
    clock.tick(30)

    if isMainMenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and selectedLevel > 1:
                    selectedLevel -= 1
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and selectedLevel < 4:
                    selectedLevel += 1
                elif event.key == pygame.K_ESCAPE and whyYouInMenu == 1:
                    isMainMenu = False
                    selectedLevel = currentLevel
                elif (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                    isMainMenu = False
                    
                    if currentLevel != selectedLevel or whyYouInMenu in [2, 3]:
                        lives, bullets, map, player, enemies = setLevel(selectedLevel)
                        currentLevel = selectedLevel
        drawMenu()

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    t = player.shoot()
                    if not t == None:
                        bullets.append(t)
                if event.key == pygame.K_ESCAPE:
                    whyYouInMenu = 1
                    isMainMenu = True
                    continue
                if event.key == pygame.K_z:
                    SA.nextAlgorithm()


        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.moveLeft()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.moveRight() 
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            player.moveUp() 
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.moveDown()


        isMainMenu, whyYouInMenu, lives = processBullets(isMainMenu, whyYouInMenu, lives)
            
        player.recalcKd()

        processTanks()


        startTime = time.time()

        SA.search(enemies, map, player)
        
        allTime = time.time() - startTime


        if len(enemies) == 0:   
            isMainMenu = True
            whyYouInMenu = 3
        
        drawWindow(float("{:.1f}".format(allTime * 1000000)))
    



pygame.quit()