import pygame
from tank import Tank
from algorithms import SA
from usefulFunc import*
#from map import Map

class Player(Tank):

    def __init__(self, x, y):
        Tank.__init__(self, x, y, player = 1)

        self.goal = None
        self.path = []


    def processPlayer(self, bullets, win, map, enemies):
        self.recalcKd()

        # startTime = time.time()
        if (len(enemies) != 0):
            self.path = SA.search(enemies, map, self, enemies[0], SA.getAlgorithm())
        # allTime = time.time() - startTime

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.moveLeft(map, enemies, self)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.moveRight(win, map, enemies, self) 
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.moveUp(map, enemies, self) 
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.moveDown(win, map, enemies, self)
        
        if keys[pygame.K_SPACE]:
            t = self.shoot()
            if not t == None:
                bullets.append(t)


    def setGoal(self, enemies, map):

        while self.goal is None:
            self.goal = map.getRandomEmptyPoint()

            self.path = SA.search(enemies, map, self, Tank(self.goal[0], self.goal[1]), 3)

            if len(self.path) == 0:
                self.goal = None
        
        self.path = SA.search(enemies, map, self, Tank(self.goal[0], self.goal[1]), 3)
        

    def processShot(self, bullets, enemies, map):
        for tank in enemies:
            dir = checkShotPossibility(self, tank, map)

            if dir != Direction.NONE:
                self.isMove = False

                if self.direction != dir:
                    self.direction = dir
                    

                if self.standTime > 5:
                    t = self.shoot()
                    if not t == None:
                        bullets.append(t)
                
                return

        self.isMove = True







    def processPlayerByAI(self, bullets, win, map, enemies):
        self.recalcKd()

        if self.goal is not None and (self.goal[0] * 100 == self.x and self.goal[1] * 100 == self.y):
            self.goal = None
            return
        
        self.setGoal(enemies, map)

        self.processShot(bullets, enemies, map)

        if self.isMove:
            self.standTime = 0
            
            if len(self.path) == 0:
                return
            elif self.path[-1] != self.goal:
                self.path.pop()

            if self.y % 100 == 0 and self.x > self.path[-1][0] * 100:
                self.moveLeft(map, enemies, self)
            elif self.y % 100 == 0 and self.x < self.path[-1][0] * 100:
                self.moveRight(win, map, enemies, self) 
            elif self.x % 100 == 0 and self.y > self.path[-1][1] * 100:
                self.moveUp(map, enemies, self) 
            elif self.x % 100 == 0 and self.y < self.path[-1][1] * 100:
                self.moveDown(win, map, enemies, self)
        else:
            self.standTime += 1
        
        
        
        
    


    