import pygame
import random
from map import Map
from stupidEnemy import StupidEnemy
from smartEnemy import SmartEnemy
from player import Player
from menu import Menu
from menu import Reasons
from algorithms import SA
from usefulStuffs import*
import csv
import os.path
import time


class Game():
    def __init__(self, win, maxLives = 3, defaultLevel = 4, stupidTanks = 2, smartTanks = 2, algorithm = 0):
        self.maxLives = maxLives
        self.win = win
        self.stupidTanks = stupidTanks
        self.smartTanks = smartTanks
        self.algorithm = algorithm
        # self.bullets = []
        # self.map = None
        # self.enemies = []
        # self.player = None
        # self.currentLevel = defaultLevel

        self.setLevel(defaultLevel, self.stupidTanks, self.smartTanks)

        self.menu = Menu(win)
        self.healthPointIm = pygame.image.load("Images/Heart.png")


    def start(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(30)

            if self.menu.isActive():
                t = self.menu.run(self.currentLevel)

                if t == -1:
                    run = False
                    continue
                elif t != 0:
                    self.setLevel(t, self.stupidTanks, self.smartTanks)
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.menu.open(Reasons.PAUSE)
                        elif event.key == pygame.K_z:
                            SA.nextAlgorithm()

                
                self.processBullets()
                self.processTanks()
                
                    
                if len(self.enemies) == 0:
                    Game.writeStatistic("game stat.csv", self.stupidTanks, self.smartTanks, self.algorithm, time.time() - self.startTime, True)
                    self.menu.open(Reasons.VICTORY)
                elif self.player.getHealth() == 0:
                    Game.writeStatistic("game stat.csv", self.stupidTanks, self.smartTanks, self.algorithm, time.time() - self.startTime, False)
                    self.menu.open(Reasons.DEFEAT)

                self.draw() # float("{:.1f}".format(allTime * 1000000))


    def setLevel(self, level, stupidTanks, smartTanks):
        self.currentLevel = level

        self.bullets = []

        if level == 1:
            self.map = Map(open("level1.txt", "r"))
            self.player= Player(1, 1, self.maxLives)
            self.enemies = [ StupidEnemy(11, 0), SmartEnemy(5, 2), SmartEnemy(11,6)]#, Enemy(13, 7)

        elif level == 2:
            self.map = Map(open("level2.txt", "r"))
            self.player= Player(1, 3, self.maxLives)
            self.enemies = [ StupidEnemy(3, 1), SmartEnemy(3, 8), SmartEnemy(5, 2)] #, Enemy(13, 1), Enemy(11,2), Enemy(13, 7)

        elif level == 3:
            self.map = Map(open("level3.txt", "r"))
            self.player= Player(7, 4, self.maxLives)
            self.enemies = [ StupidEnemy(1, 1), SmartEnemy(6, 7), SmartEnemy(12, 5)] #, Enemy(6, 7), Enemy(4, 7), Enemy(1,6), Enemy(13, 1)
        
        elif level == 4:
            Map.generateMap()
            self.map = Map(open("level4.txt", "r"))
            self.enemies = []
            usedPos = []
            tanks = 0
            while tanks < 1 + stupidTanks + smartTanks:
                x = random.randint(0, 14)
                y = random.randint(0, 8)

                if self.map.terrain[y][x] in [0, 1, 8] and not((x, y)  in usedPos):
                    if tanks == 0:
                        self.player= Player(x, y, self.maxLives)
                        usedPos.append((x, y))
                    elif tanks <= stupidTanks:
                        self.enemies.append(StupidEnemy(x, y))
                        usedPos.append((x, y))
                    else:
                        self.enemies.append(SmartEnemy(x, y))
                        usedPos.append((x, y))
                    tanks += 1
        
        self.startTime = time.time()


    def processTanks(self):
        
        for tank in self.enemies:
            if tank.getHealth() == 0:
                self.enemies.pop(self.enemies.index(tank))


        # player.processPlayer(bullets, win, map, enemies)
        self.player.processTank(self.bullets, self.win, self.map, self.enemies, self.algorithm)
        
        for tank in self.enemies:
            tank.processTank(self.bullets, self.win, self.map, self.enemies, self.player)


    def processBullets(self):
        k = len(self.bullets)
        for bullet in reversed(self.bullets):
            k -= 1
            id = self.map.checkObstacle(bullet.x, bullet.y, bullet.width, bullet.height)
            if id == 1 or id == 2:
                
                if id == 2:
                    self.map.destroyWall(bullet.x, bullet.y, bullet.width, bullet.height)

                self.bullets.pop(self.bullets.index(bullet))
            
            else:
                for tank in self.enemies + [self.player]:
                    if checkEntityCollision(tank, bullet) and tank.player != bullet.isShotByPlayer:
                        self.bullets.pop(self.bullets.index(bullet))
                        tank.takeDamage(1)
                        
                #         break
                # if checkEntityCollision(self.player, bullet) and self.player.player != bullet.isShotByPlayer:
                #         self.bullets.pop(self.bullets.index(bullet))
                #         self.lives -= 1
            bullet.move()


    def draw(self): # allTime
        self.win.fill((0, 0, 0))
        for row in range(9):
            for coll in range(15):
                self.win.blit(self.map.bg[self.map.terrain[row][coll]], (coll*self.map.cellSize, row*self.map.cellSize))

        # colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255), (0, 100, 122)]
        # radius = [23, 20, 17, 14, 11, 8, 5]

        # for pair in self.player.path:
        #     pygame.draw.circle(self.win, colors[0], (pair[0] * 100 + 50, pair[1] * 100 + 50), radius[0])

        # f = pygame.font.SysFont("Arial", 60)
        # if (SA.getAlgorithm() == 0):
        #     textTime = f.render("DFS time: " + str(allTime), True, (255, 255, 0))
        # elif (SA.getAlgorithm() == 1):
        #     textTime = f.render("BFS time: " + str(allTime), True, (255, 255, 0))
        # elif (SA.getAlgorithm() == 2):
        #     textTime = f.render("UCS time: " + str(allTime), True, (255, 255, 0))
        

        self.player.draw(self.win, self.map.cellSize)
        
        for tank in self.enemies:
            tank.draw(self.win, self.map.cellSize)
        
        for bullet in self.bullets:
            bullet.draw(self.win)

        for i in range(self.player.getHealth()):
            self.win.blit(self.healthPointIm, (1500 - 70 * (self.maxLives - i) - 40, 20))

        #pygame.draw.rect(win, (255, 255, 255), (1000, 800, 500, 100))
        # win.blit(textTime, (1050, 820))



        pygame.display.update()


    def writeStatistic(filename, numOfStupid, numOfSmart, algorithm, duration, isVictory):
        u = True
        if os.path.exists(filename):
            u = False

        with open(filename, 'a+', newline = '') as statFile:
            writer = csv.writer(statFile)
            if u:
                writer.writerows([['stupid','smart','algorithm','duration','victory']])
            writer.writerows([[str(numOfStupid), str(numOfSmart), str(algorithm), str(duration)[ : 6] + 's', str(isVictory)]])



