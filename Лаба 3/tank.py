import pygame
from bullet import Bullet
from usefulFunc import*


class Tank():
    maxKD = 20

    def __init__(self, x, y, cellSize = 100, width = 100, height = 100, speed = 5, direction = Direction.DOWN, player = 2, error = 20):
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
        self.isMove = True
        self.standTime = 0
        
        if player == 1:
            self.playerIm =   { Direction.UP : pygame.image.load('Images/Player1.png'), Direction.RIGHT : pygame.image.load('Images/Player2.png'), 
                                Direction.DOWN : pygame.image.load('Images/Player3.png'), Direction.LEFT : pygame.image.load('Images/Player4.png')}
        else:
            self.playerIm =   { Direction.UP : pygame.image.load('Images/Enemy1.png'), Direction.RIGHT : pygame.image.load('Images/Enemy2.png'), 
                                Direction.DOWN : pygame.image.load('Images/Enemy3.png'), Direction.LEFT : pygame.image.load('Images/Enemy4.png')}


    def move(self, win, map, enemies, player):
        if self.direction == Direction.UP:
            self.moveUp(map, enemies, player)
        elif self.direction == Direction.RIGHT:
            self.moveRight(win, map, enemies, player)
        elif self.direction == Direction.DOWN:
            self.moveDown(win, map, enemies, player)
        else:
            self.moveLeft(map, enemies, player)


    def moveLeft(self, map, enemies, player):
        self.direction = Direction.LEFT

        if self.x > 0 and map.checkObstacle(self.x-self.speed + self.error // 2, self.y + self.error // 2, self.width - self.error, self.height - self.error) == 0:
            self.x -= self.speed

            for tank in enemies:
                if not tank == self and checkEntityCollision(self, tank):
                    self.x += self.speed
                    return

            if not player == self and checkEntityCollision(self, player):
                    self.x += self.speed
                    return


    def moveRight(self, win, map, enemies, player):
        self.direction = Direction.RIGHT

        if self.x < win.get_width() - self.width and map.checkObstacle(self.x + self.speed + self.error // 2, self.y + self.error // 2, self.width - self.error, self.height - self.error) == 0:
            self.x += self.speed
            for tank in enemies:
                if not tank == self and checkEntityCollision(self, tank):
                    self.x -= self.speed
                    return

            if not player == self and checkEntityCollision(self, player):
                    self.x -= self.speed
                    return


    def moveUp(self, map, enemies, player):
        self.direction = Direction.UP

        if self.y > 0 and map.checkObstacle(self.x + self.error // 2, self.y-self.speed + self.error // 2, self.width - self.error, self.height - self.error) == 0:
            self.y -= self.speed
            for tank in enemies:
                if not tank == self and checkEntityCollision(self, tank):
                    self.y += self.speed
                    return

            if not player == self and checkEntityCollision(self, player):
                self.y += self.speed
                return


    def moveDown(self, win, map, enemies, player):
        self.direction = Direction.DOWN

        if  self.y < win.get_height() - self.height and map.checkObstacle(self.x + self.error // 2, self.y + self.speed + self.error // 2, self.width - self.error, self.height - self.error) == 0:
            self.y += self.speed
            for tank in enemies:
                if not tank == self and checkEntityCollision(self, tank):
                    self.y -= self.speed
                    return
            if not player == self and checkEntityCollision(self, player):
                self.y -= self.speed
                return


    def draw(self, win, cellSize):
        win.blit(self.playerIm[self.direction], (self.x + (cellSize - self.width) / 2, self.y + (cellSize - self.height) / 2))


    def shoot(self):
        if self.kd == 0:
            self.kd = Tank.maxKD
            return Bullet(self.x, self.y, self.direction, self.player)
        return None


    def recalcKd(self):
        if self.kd > 0:
            self.kd -= 1