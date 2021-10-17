import random
import pygame
from tank import Tank
from algorithms import SA
from usefulStuffs import*
from map import Map
from bullet import Bullet
from stupidEnemy import StupidEnemy
from smartEnemy import SmartEnemy
import copy


class Player(Tank):

    def __init__(self, x, y, healthpoint = 3):
        Tank.__init__(self, x, y, lives = healthpoint, player = 1)

        self.num = -1

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
      

    def processTank(self, bullets, win, map, enemies, algoritm):

        # self.processPlayerByAI(bullets, win, map, enemies)
        self.recalcKd()

        #self.num = Player.miniMax(self, enemies, map, bullets, win, 0, True, -1000000000, 1000000000)[1]

        if self.x % 100 == 0 and self.y % 100 == 0 or self.num < 4:
            self.num = Player.miniMax(algoritm, self, enemies, map, bullets, win, 0, True, -1000000000, 1000000000)[1]

        if not Player.playerTurn(self, bullets, self.num, win, map, enemies):
            self.processPlayerByAI(bullets, win, map, enemies)

        
    
    def miniMax(algoritm, player, enemies, map, bullets, win, depth, isPlayer, alpha, beta):   
        if player.health <= 0:
            return -1000000, 0
        elif len(enemies) == 0:
            return 1000000, 0
        elif depth == 4:
            return Player.evaluationFunction(player, enemies, map, bullets), 0


        c_enemies = [[t.x for t in enemies], [t.y for t in enemies], [t.kd for t in enemies], [t.standTime for t in enemies]]
        c_bullets = [Bullet(t.x, t.y, t.direction, t.isShotByPlayer, isItBulletCoord = True) for t in bullets]
        c_plX, c_plY, c_plHealth, c_plKD = player.x, player.y, player.health, player.kd
        c_mapTerr = copy.deepcopy(map.terrain)
        
        
        if isPlayer == True:
            bestVal = -1000000000

            u = True
            bestNum = 0
            for i in range(8):
                if u:
                    player.x, player.y, player.health, player.kd = c_plX, c_plY, c_plHealth, c_plKD
                    c_bullets = [Bullet(t.x, t.y, t.direction, t.isShotByPlayer, isItBulletCoord = True) for t in bullets]

                u = Player.playerTurn(player, c_bullets, i, win, map, enemies)
                if u:
                    val, num = Player.miniMax(algoritm, player, enemies, map, c_bullets, win, depth + 1, not isPlayer, alpha, beta)
                    if algoritm == "expectimax":
                        val // 4
                    if val > bestVal:
                        bestNum = i
                    bestVal = max(bestVal, val)
                    alpha = max(alpha, bestVal)
                    if beta <= alpha:
                        break
            
            map.terrain = c_mapTerr
            player.x, player.y, player.health, player.kd = c_plX, c_plY, c_plHealth, c_plKD
            for i in range(len(enemies)):
                enemies[i].x = c_enemies[0][i]
                enemies[i].y = c_enemies[1][i]
                enemies[i].kd = c_enemies[2][i]
                enemies[i].standTime = c_enemies[3][i]
                enemies[i].health = 1

            return bestVal, bestNum
        else:
            coll = []

            for i in range(20):
                Player.processBulletsForMinimax(c_bullets, map, enemies, player)
                #proc_plX, proc_plY, proc_plHealth, c_plKD = player.x, player.y, player.health, player.kd
                for tank in reversed(enemies):
                    if tank.getHealth() <= 0:
                        coll.append(tank)
                        enemies.pop(enemies.index(tank))
                
                player.recalcKd()
                player.move(win, map, enemies, player)
                # player.processTank(c_bullets, win, map, enemies)
                
                
                for tank in enemies:
                    tank.processTankForMinimax(c_bullets, win, map, enemies, player)



            bestVal =  1000000000
            val, num = Player.miniMax(algoritm, player, enemies, map, c_bullets, win, depth + 1, not isPlayer, alpha, beta)
            bestVal = min(bestVal, val)
            beta = min(beta, bestVal)
            if beta <= alpha:
                pass
                #return bestVal, 0

            map.terrain = c_mapTerr
            player.x, player.y, player.health, player.kd = c_plX, c_plY, c_plHealth, c_plKD
            
            for t in coll:
                enemies.append(t)

            for i in range(len(enemies)):
                enemies[i].x = c_enemies[0][i]
                enemies[i].y = c_enemies[1][i]
                enemies[i].kd = c_enemies[2][i]
                enemies[i].standTime = c_enemies[3][i]
                enemies[i].health = 1
            
            return bestVal, 0
    

    def processBulletsForMinimax(bullets, map, enemies, player):
        for bullet in reversed(bullets):
            bullet.move()
            id = map.checkObstacle(bullet.x, bullet.y, bullet.width, bullet.height)
            if id == 1 or id == 2:
                if id == 2:
                    map.destroyWall(bullet.x, bullet.y, bullet.width, bullet.height)
                bullets.pop(bullets.index(bullet))  
            else:
                for tank in enemies + [player]:
                    if checkEntityCollision(tank, bullet) and tank.player != bullet.isShotByPlayer:
                        bullets.pop(bullets.index(bullet))
                        tank.takeDamage(1)

            


    def playerTurn(tank, bullets, num, win, map, enemies):
        if num == 0:
            tank.direction = Direction.RIGHT
            t = tank.shoot()
            if t != None:
                bullets.append(t)
                return True
        elif num == 1:
            tank.direction = Direction.DOWN
            t = tank.shoot()
            if t != None:
                bullets.append(t)
                return True
        elif num == 2:
            tank.direction = Direction.LEFT
            t = tank.shoot()
            if t != None:
                bullets.append(t)
                return True
        elif num == 3:
            tank.direction = Direction.UP
            t = tank.shoot()
            if t != None:
                bullets.append(t)
                return True
        elif num == 4:
            return tank.moveRight(win, map, enemies, tank)
        elif num == 5:
            return tank.moveDown(win, map, enemies, tank)
        elif num == 6:
            return tank.moveLeft(map, enemies, tank)
        elif num == 7:
            return tank.moveUp(map, enemies, tank)
        return False
 

    def evaluationFunction(player, enemies, map, bullets):
        enemiesNum = 0
        for t in enemies:
            if t.health > 0:
                enemiesNum+=1

        k = 0
        if (map.checkObstacle(player.x + 100, player.y, player.width, player.height) == 0):
            k+=1
        if (map.checkObstacle(player.x, player.y + 100, player.width, player.height) == 0):
            k+=1
        if (map.checkObstacle(player.x - 100, player.y, player.width, player.height) == 0):
            k+=1
        if (map.checkObstacle(player.x, player.y - 100, player.width, player.height) == 0):
            k+=1

        l = 0
        for bullet in bullets:
            if bullet.isShotByPlayer != 1:
                d = (player.x - bullet.x)**2 + (player.y - bullet.y)**2
                if d < 50000:
                    l+= 1

        distToNearestEnemy = 10000000
        for t in enemies:
            if distToNearestEnemy < abs(player.x - t.x) + abs(player.y - t.y):
                distToNearestEnemy = abs(player.x - t.x) + abs(player.y - t.y)
        

        mark = 0
        mark += player.health * 60000
        mark -= enemiesNum * 100000
        mark -= player.kd * 1000
        mark += k * 10000
        mark -= l * 9000
        mark -= distToNearestEnemy * 2
        mark += random.randint(0, 100)
            

        return mark

