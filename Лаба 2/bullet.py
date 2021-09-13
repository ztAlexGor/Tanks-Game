import pygame

class Bullet():
    def __init__(self, x, y, direction, player, speed = 10):

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


    def draw(self, win):
        win.blit(self.image[self.direction], (self.x, self.y))
