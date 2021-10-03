import pygame
import random
from map import Map
from player import Player
from enemy import Enemy
from algorithms import SA
from usefulFunc import*


pygame.init()
win = pygame.display.set_mode((1500, 900))
pygame.display.set_caption('Tanks')


      
def drawWindow(): # allTime
    win.fill((0, 0, 0))
    for row in range(9):
        for coll in range(15):
            win.blit(map.bg[map.terrain[row][coll]], (coll*map.cellSize, row*map.cellSize))

    colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255), (0, 100, 122)]
    radius = [23, 20, 17, 14, 11, 8, 5]

    for pair in player.path:
        pygame.draw.circle(win, colors[0], (pair[0] * 100 + 50, pair[1] * 100 + 50), radius[0])

    # f = pygame.font.SysFont("Arial", 60)
    # if (SA.getAlgorithm() == 0):
    #     textTime = f.render("DFS time: " + str(allTime), True, (255, 255, 0))
    # elif (SA.getAlgorithm() == 1):
    #     textTime = f.render("BFS time: " + str(allTime), True, (255, 255, 0))
    # elif (SA.getAlgorithm() == 2):
    #     textTime = f.render("UCS time: " + str(allTime), True, (255, 255, 0))
    

    player.draw(win, map.cellSize)
    
    for tank in enemies:
        tank.draw(win, map.cellSize)
    
    for bullet in bullets:
        bullet.draw(win)

    for i in range(lives):
        win.blit(healthPoint, (1300 + 70 * i, 20))

    #pygame.draw.rect(win, (255, 255, 255), (1000, 800, 500, 100))
    # win.blit(textTime, (1050, 820))



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
        player = Player(1, 1)
        enemies = [Enemy(11, 0), Enemy(5, 2), Enemy(11,6)]#, Enemy(13, 7)

    elif level == 2:
        map = Map(open("level2.txt", "r"))
        player = Player(1, 3)
        enemies = [ Enemy(3, 1), Enemy(3, 8), Enemy(5, 2)] #, Enemy(13, 1), Enemy(11,2), Enemy(13, 7)

    elif level == 3:
        map = Map(open("level3.txt", "r"))
        player = Player(7, 4)
        enemies = [ Enemy(1, 1), Enemy(13, 4), Enemy(12, 5)] #, Enemy(6, 7), Enemy(4, 7), Enemy(1,6), Enemy(13, 1)
    
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
                    player = Player(x, y)
                    usedPos.append((x, y))
                else:
                    enemies.append(Enemy(x, y))
                    usedPos.append((x, y))
                tanks += 1
                
                

    return lives, bullets, map, player, enemies

def processBullets(isMainMenu, whyYouInMenu, lives):
    for bullet in bullets:
            id = map.checkObstacle(bullet.x, bullet.y, bullet.width, bullet.height)
            if id == 1 or id == 2:
                
                if id == 2 and random.randint(0, 4) != 0:
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
    # player.processPlayer(bullets, win, map, enemies)
    player.processPlayerByAI(bullets, win, map, enemies)
    
    for tank in enemies:
        tank.processTankByAI(bullets, win, map, enemies, player)


lives, bullets, map, player, enemies = setLevel(4)


run = True
isMainMenu = True
whyYouInMenu = 0
selectedLevel = 4
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
                if event.key == pygame.K_ESCAPE:
                    whyYouInMenu = 1
                    isMainMenu = True
                    continue
                if event.key == pygame.K_z:
                    SA.nextAlgorithm()

        
        processTanks()
        
        isMainMenu, whyYouInMenu, lives = processBullets(isMainMenu, whyYouInMenu, lives)
            
        

        if len(enemies) == 0:   
            isMainMenu = True
            whyYouInMenu = 3
        
        drawWindow() # float("{:.1f}".format(allTime * 1000000))
    



pygame.quit()