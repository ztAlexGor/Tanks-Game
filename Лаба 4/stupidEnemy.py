# import pygame
import random
from tank import Tank
from algorithms import SA
from usefulStuffs import*
#from map import Map

class StupidEnemy(Tank):

    def __init__(self, x, y):
        Tank.__init__(self, x, y, player = 2)
        

    def processShot(self, bullets, player, map):
        dir = checkShotPossibility(self, player, map)

        if dir != Direction.NONE:
            self.isMove = False

            if self.direction != dir:
                self.direction = dir
                

            if self.standTime > random.randint(5, 50):
                t = self.shoot()
                if not t == None:
                    bullets.append(t)
            
            return


        if random.randint(0, 100) == 0:
            t = self.shoot()

            if not t == None:
                bullets.append(t)

        self.isMove = True


    def randomProcessing(self, bullets, win, map, enemies, player):
        self.recalcKd()
        self.processShot(bullets, player, map)

        if self.isMove:
            if random.randint(0, 100) == 0:
                r = random.randint(1, 4)
                if r == 1:
                    self.direction = Direction.UP
                elif r == 2:
                    self.direction = Direction.RIGHT
                elif r == 3:
                    self.direction = Direction.DOWN
                elif r == 4:
                    self.direction = Direction.LEFT 
            if random.randint(0, 50) == 0:
                self.state = random.randint(0, 1)
            
            if self.state == 1:
                self.move(win, map, enemies, player)
        else:
            self.standTime += 1


    def processTank(self, bullets, win, map, enemies, player):
        self.randomProcessing(bullets, win, map, enemies, player)
        

    def processTankForMinimax(self, bullets, win, map, enemies, player):
        self.recalcKd()
        self.processShot(bullets, player, map)
    


    