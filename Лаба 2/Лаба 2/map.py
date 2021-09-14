import pygame
import random

class Map():
    def __init__(self, file, mapWidth = 15, mapHeight = 9, cellSize= 100):
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.cellSize = cellSize

        self.terrain = []
        for line in file: # read rest of lines
            self.terrain.append([int(x) for x in line.split()])

        self.bg =  [pygame.image.load('Images/Grass.png'), pygame.image.load('Images/Sand.png'), 
                    pygame.image.load('Images/Water6.png'), pygame.image.load('Images/Wall.png'), 
                    pygame.image.load('Images/BreakBlock1.jpg'), pygame.image.load('Images/BreakBlock2.jpg'),
                    pygame.image.load('Images/BreakBlock3.jpg'), pygame.image.load('Images/BreakBlock4.jpg'), 
                    pygame.image.load('Images/GrassWithDebris.png')]
    

        
    def checkObstacle(self, x, y, width, height): # 0 - empty, 1 - unbreak. wall, 2 - breakeable wall, 3 - water

        if x < 0 or x >= 1500 or y < 0 or y >= 900:
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

    
    def generateMap(x = 15, y = 9):
        f = open("level4.txt", "w")
        for i in range(y):
            for j in range(x):
                rand = random.randint(0, 99)
                if rand < 55:
                    f.write('0')
                elif rand < 70:
                    f.write('1')
                elif rand < 73:
                    f.write('2')
                elif rand < 78:
                    f.write('3')    
                elif rand < 85:
                    f.write('4')
                elif rand < 89:
                    f.write('5')
                elif rand < 93:
                    f.write('6')
                elif rand < 97:
                    f.write('7')
                elif rand < 100:
                    f.write('8')
                
                
                f.write(" ")
            f.write("\n")

        f.close()
