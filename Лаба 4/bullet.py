import pygame
from usefulStuffs import*

class Bullet():
    def __init__(self, x, y, direction, player, speed = 10, isItBulletCoord = False):

        self.speed = speed
        self.direction = direction
        self.isShotByPlayer = player
        self.image = { Direction.UP : pygame.image.load('Images/Bullet1.png'), Direction.RIGHT : pygame.image.load('Images/Bullet2.png'), 
                       Direction.DOWN : pygame.image.load('Images/Bullet3.png'), Direction.LEFT : pygame.image.load('Images/Bullet4.png') }

        if self.direction in [Direction.UP, Direction.DOWN]:
            self.width = 12
            self.height = 32
        else:
            self.width = 32
            self.height = 12

        
        self.x = x
        self.y = y

        if not isItBulletCoord:
            self.x += (100 - self.width) // 2    # 100 - tank.width
            self.y += (100 - self.height) // 2    # 100 - tank.height
      

    def move(self):
        if self.direction == Direction.UP:
            self.y -= self.speed
        elif self.direction == Direction.RIGHT:
            self.x += self.speed
        elif self.direction == Direction.DOWN:
            self.y += self.speed
        else:
            self.x -= self.speed


    def draw(self, win):
        win.blit(self.image[self.direction], (self.x, self.y))
