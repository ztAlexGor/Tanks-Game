import pygame
import random

from pygame.constants import KEYDOWN

pygame.init()
win = pygame.display.set_mode((1500, 900))

pygame.display.set_caption('Tanks')



class Map():
    def __init__(self, mapWidth, mapHeight, cellSize, terrain):
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.cellSize = cellSize
        self.terrain = terrain
        self.bg =  [pygame.image.load('Images/Grass.png'), pygame.image.load('Images/Sand.png'), 
                    pygame.image.load('Images/Water6.png'), pygame.image.load('Images/Wall.png'), 
                    pygame.image.load('Images/BreakBlock1.jpg'), pygame.image.load('Images/BreakBlock2.jpg'),
                    pygame.image.load('Images/BreakBlock3.jpg'), pygame.image.load('Images/BreakBlock4.jpg'), 
                    pygame.image.load('Images/GrassWithDebris.png')]
    

        
    def checkObstacle(self, x, y, width, height): # 0 - empty, 1 - unbreak. wall, 2 - breakeable wall, 3 - water

        if x < 0 or x >= win.get_width() or y < 0 or y >= win.get_height():
            return 1


        row = y // self.cellSize
        coll = x // self.cellSize
        if row >= 0 and row < self.mapHeight and coll >= 0 and coll < self.mapWidth:
            if self.terrain[row][coll] == 3:
                return 1
            elif self.terrain[row][coll] in [4,5,6,7]: #break
                return 2
            elif self.terrain[row][coll] == 2:
                return 3


        row = (y + height - 1) // self.cellSize
        coll = x // self.cellSize

        if row >= 0 and row < self.mapHeight and coll >= 0 and coll < self.mapWidth:
            if self.terrain[row][coll] == 3:
                return 1
            elif self.terrain[row][coll] in [4,5,6,7]: #break
                return 2
            elif self.terrain[row][coll] == 2:
                return 3
        

        row = y // self.cellSize
        coll = (x + width - 1) // self.cellSize

        if row >= 0 and row < self.mapHeight and coll >= 0 and coll < self.mapWidth:
            if self.terrain[row][coll] == 3:
                return 1
            elif self.terrain[row][coll] in [4,5,6,7]: #break
                return 2
            elif self.terrain[row][coll] == 2:
                return 3


        row = (y + height - 1) // self.cellSize
        coll = (x + width - 1) // self.cellSize
        
        if row >= 0 and row < self.mapHeight and coll >= 0 and coll < self.mapWidth:
            if self.terrain[row][coll] == 3:
                return 1
            elif self.terrain[row][coll] in [4,5,6,7]: #break
                return 2
            elif self.terrain[row][coll] == 2:
                return 3
        
        return 0
    

    def destroyWall(self, x, y, width, height):
        col = x // self.cellSize
        row = y // self.cellSize
        if self.terrain[row][col] == 4:
            self.terrain[row][col] = random.randint(5,7)
            return
        elif self.terrain[row][col] in [5, 6, 7]:
            self.terrain[row][col] = 8
            return

        col = (x +  width) // self.cellSize
        row = y // self.cellSize
        if self.terrain[row][col] == 4:
            self.terrain[row][col] = random.randint(5,7)
            return
        elif self.terrain[row][col] in [5, 6, 7]:
            self.terrain[row][col] = 8
            return
        
        col = x // self.cellSize
        row = (y + height) // self.cellSize
        if self.terrain[row][col] == 4:
            self.terrain[row][col] = random.randint(5,7)
            return
        elif self.terrain[row][col] in [5, 6, 7]:
            self.terrain[row][col] = 8
            return

        col = (x +  width) // self.cellSize
        row = (y + height) // self.cellSize
        if self.terrain[row][col] == 4:
            self.terrain[row][col] = random.randint(5,7)
            return
        elif self.terrain[row][col] in [5, 6, 7]:
            self.terrain[row][col] = 8
            return

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

class Tank():
    def __init__(self, x, y, width = 100, height = 100, speed = 5, direction = 2, player = 2):
        self.x = x * map.cellSize
        self.y = y * map.cellSize
        self.width = width
        self.height = height
        self.speed = speed
        self.direction = direction
        self.player = player
        self.kd = 0
        self.playerIm = []
        self.state = 0
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

        if self.x > 0 and map.checkObstacle(self.x-self.speed, self.y, self.width, self.height) == 0:
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

        if self.x < win.get_width() - self.width and map.checkObstacle(self.x + self.speed, self.y, self.width, self.height) == 0:
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

        if self.y > 0 and map.checkObstacle(self.x, self.y-self.speed, self.width, self.height) == 0:
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

        if  self.y < win.get_height() - self.height and map.checkObstacle(self.x, self.y + self.speed, self.width, self.height) == 0:
            self.y += self.speed
            for tank in enemies:
                if not tank == self and checkEntityCollision(self, tank):
                    self.y -= self.speed
                    return
            if not player == self and checkEntityCollision(self, player):
                self.y -= self.speed
                return

                
            
        
        
    def draw(self):
        win.blit(self.playerIm[self.direction], (self.x + (map.cellSize - self.width) / 2, self.y + (map.cellSize - self.height) / 2))

    def shoot(self):
        if self.kd == 0:
            self.kd = 30
            return Bullet(self.x, self.y, 10, self.direction, self.player)
        return None

    def recalcKd(self):
        if self.kd > 0:
            self.kd -= 1
        
class Bullet():
    def __init__(self, x, y, speed, direction, player):

        self.speed = speed
        self.direction = direction
        self.isShotByPlayer = player
        self.image = [  pygame.image.load('Images/Bullet1.png'), pygame.image.load('Images/Bullet2.png'), 
                        pygame.image.load('Images/Bullet3.png'), pygame.image.load('Images/Bullet4.png')]

        if self.direction % 2 == 0:
            self.width = 12
            self.height = 32
        else:
            self.width = 32
            self.height = 12

        self.x = x + (100 - self.width) // 2    # 100 - tank.width
        self.y = y + (100 - self.height) // 2    # 100 - tank.height

        

    def move(self):
        if self.direction == 0:
            self.y -= self.speed
        elif self.direction == 1:
            self.x += self.speed
        elif self.direction == 2:
            self.y += self.speed
        else:
            self.x -= self.speed


    def draw(self):
        win.blit(self.image[self.direction], (self.x, self.y))

def drawWindow():
    win.fill((0, 0, 0))
    for row in range(9):
        for coll in range(15):
            win.blit(map.bg[map.terrain[row][coll]], (coll*map.cellSize, row*map.cellSize))

    player.draw()
    
    for tank in enemies:
        tank.draw()
    
    for bullet in bullets:
        bullet.draw()

    for i in range(lives):
        win.blit(healthPoint, (1300 + 70 * i, 20))
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
        text = f.render("YOU WIN", (0, 255, 0), (64, 0, 128))
        position = 670

    color = (0, 0, 255)

    text1 = f.render("Level 1", (0, 255, 0), color)
    text2 = f.render("Level 2", (0, 255, 0), color)
    text3 = f.render("Level 3", (0, 255, 0), color)

    if selectedLevel == 1:
        text1 = f.render("Level 1", (0, 255, 0), (255, 255, 255))
    elif selectedLevel == 2:
        text2 = f.render("Level 2", (0, 255, 0), (255, 255, 255))
    else:
        text3 = f.render("Level 3", (0, 255, 0), (255, 255, 255))
    
    win.blit(text, (position, 235))
    win.blit(text1, (700, 330))
    win.blit(text2, (700, 430))
    win.blit(text3, (700, 530))

    pygame.display.update()

def setLevel(level):
    global lives
    global bullets
    global map
    global player
    global enemies

    lives = 3
    bullets = []
    if level == 1:
        map = Map(15, 9, 100, [ [0,0,3,0,0,0,0,0,8,6,0,0,0,1,1],
                                [0,0,3,0,0,0,0,0,4,5,0,0,1,1,1],
                                [0,0,3,1,0,0,0,4,6,4,0,0,1,2,2],
                                [2,0,2,1,0,0,0,4,4,4,0,1,1,2,2],
                                [2,0,2,0,0,0,0,0,0,0,0,1,2,2,2],
                                [0,0,0,0,0,1,0,0,5,0,0,1,2,2,2],
                                [0,0,0,0,0,0,4,4,3,0,0,1,1,1,1],
                                [0,0,0,0,0,5,4,3,3,0,0,0,1,1,1],    
                                [0,0,0,0,0,7,5,3,3,0,0,0,0,0,1]])

        player = Tank(1, 1, direction = 2, player = 1)
        enemies = [Tank(11, 0), Tank(5, 2), Tank(11,6), Tank(13, 7)]
    
    elif level == 2:
        map = Map(15, 9, 100, [ [0,0,1,0,0,0,0,0,6,4,4,0,0,0,0],
                                [7,6,5,1,1,2,0,0,0,5,0,0,0,0,0],
                                [0,0,3,2,1,0,0,0,1,1,0,0,4,0,0],
                                [0,0,3,2,1,0,0,1,1,1,0,4,4,4,0],
                                [0,0,3,1,1,0,0,0,0,0,0,0,4,4,4],
                                [0,0,4,0,0,4,6,0,0,0,0,0,4,0,0],
                                [0,0,0,0,0,5,6,0,0,4,3,0,0,0,0],
                                [4,4,4,0,0,5,5,0,0,0,3,4,0,0,7],    
                                [4,4,4,0,0,4,7,0,0,0,3,4,0,0,6]])

        player = Tank(1, 3, direction = 2, player = 1)
        enemies = [ Tank(3, 1), Tank(3, 8), Tank(5, 2), Tank(13, 1), Tank(11,2), Tank(13, 7)]
    
    else:
        map = Map(15, 9, 100, [ [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
                                [3,0,0,6,0,0,0,0,0,0,0,0,0,0,3],
                                [3,7,5,4,0,4,4,4,4,4,0,4,5,4,3],
                                [3,0,0,6,0,4,3,2,3,4,2,0,0,0,3],
                                [3,0,0,5,0,0,1,1,2,4,2,0,0,0,3],
                                [3,0,0,6,0,4,3,2,3,4,2,0,0,0,3],
                                [3,0,0,7,0,4,4,4,4,4,4,5,3,3,3],
                                [3,0,0,4,0,0,0,0,0,0,0,0,0,0,3],    
                                [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]])

        player = Tank(7, 4, direction = 1, player = 1)
        enemies = [ Tank(1, 1), Tank(13, 4), Tank(12, 5), Tank(6, 7), Tank(4, 7), Tank(1,6), Tank(13, 1)]
        


map = Map(15, 9, 100, [ [0,0,3,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,3,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,3,1,0,0,0,0,0,1,0,0,0,2,0],
                        [2,0,2,1,0,0,0,0,0,1,0,0,0,2,0],
                        [2,0,2,0,0,0,0,0,0,0,0,0,2,2,4],
                        [0,0,0,0,0,1,0,0,0,0,0,0,2,0,5],
                        [0,0,0,0,0,0,4,4,3,0,0,0,0,0,5],
                        [0,0,0,0,0,5,4,0,3,0,0,0,0,0,7],    
                        [0,0,0,0,0,5,5,0,0,0,0,0,0,0,6]])

player = Tank(1, 1, direction = 2, player = 1)
enemies = [ Tank(7, 7), Tank(3, 8), Tank(5, 1), Tank(5, 2), Tank(11,2), Tank(13, 7)]
lives = 3
bullets = []
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
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and selectedLevel < 3:
                    selectedLevel += 1
                elif event.key == pygame.K_ESCAPE and whyYouInMenu == 1:
                    isMainMenu = False
                    selectedLevel = currentLevel
                elif (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                    isMainMenu = False
                    
                    if currentLevel != selectedLevel:
                        setLevel(selectedLevel)
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

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.moveLeft()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.moveRight() 
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            player.moveUp() 
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.moveDown()


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
            
        player.recalcKd()

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
        
        if len(enemies) == 0:
            isMainMenu = True
            whyYouInMenu = 3
        
        drawWindow()
    



pygame.quit()