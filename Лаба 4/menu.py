import pygame
from enum import Enum


class Reasons(Enum):
    MENU = 0
    PAUSE = 1
    VICTORY = 2
    DEFEAT = 3



class Menu():
    def __init__(self, win, whyYouInMenu = Reasons.MENU):
        self.win = win
        self.isMenu = True
        self.whyYouInMenu = whyYouInMenu

        self.bgMenuIm = pygame.image.load("Images/BgMenu.png")


    def run(self, currLevel):
        self.selectedLevel = currLevel

        while self.isMenu:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                    return -1
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        self.selectedLevel -= 1
                        if self.selectedLevel == 0:
                            self.selectedLevel = 4                        
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        self.selectedLevel += 1
                        if self.selectedLevel == 5:
                            self.selectedLevel = 1
                    elif event.key == pygame.K_ESCAPE and self.whyYouInMenu == Reasons.PAUSE:
                        self.close()
                        return 0
                    elif (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                        self.close()
                        
                        if currLevel != self.selectedLevel or self.whyYouInMenu in [Reasons.VICTORY, Reasons.DEFEAT]:
                            return self.selectedLevel
                        else:
                            return 0
            

    def setWhyYouInMenu(self, reason):
        self.whyYouInMenu = reason


    def setIsMenu(self, state):
        self.isMenu = state


    def isActive(self):
        return self.isMenu


    def open(self, reason):
        self.isMenu = True
        self.whyYouInMenu = reason


    def close(self):
        self.isMenu = False


    def draw(self):
        self.win.fill((0, 0, 0))
        self.win.blit(self.bgMenuIm, (0, 0))

        f = pygame.font.SysFont("Arial", 60)
        position = 700
        if self.whyYouInMenu == Reasons.MENU:
            text = f.render("MENU", (0, 255, 0), (64, 0, 128))
            position = 705
        if self.whyYouInMenu == Reasons.PAUSE:
            text = f.render("PAUSE", (0, 255, 0), (64, 0, 128))
            position = 700
        elif self.whyYouInMenu == Reasons.VICTORY:
            text = f.render("YOU WON", (0, 255, 0), (64, 0, 128))
            position = 670
        elif self.whyYouInMenu == Reasons.DEFEAT:
            text = f.render("YOU LOSE", (0, 255, 0), (64, 0, 128))
            position = 645

        color = (0, 0, 255)

        text1 = f.render("Level 1", (0, 255, 0), color)
        text2 = f.render("Level 2", (0, 255, 0), color)
        text3 = f.render("Level 3", (0, 255, 0), color)
        text4 = f.render("Random Level", (0, 255, 0), color)

        if self.selectedLevel == 1:
            text1 = f.render("Level 1", (0, 255, 0), (255, 255, 255))
        elif self.selectedLevel == 2:
            text2 = f.render("Level 2", (0, 255, 0), (255, 255, 255))
        elif self.selectedLevel == 3:
            text3 = f.render("Level 3", (0, 255, 0), (255, 255, 255))
        elif self.selectedLevel == 4:
            text4 = f.render("Random Level", (0, 255, 0), (255, 255, 255))
        
        self.win.blit(text, (position, 235))
        self.win.blit(text1, (700, 330))
        self.win.blit(text2, (700, 430))
        self.win.blit(text3, (700, 530))
        self.win.blit(text4, (620, 625))

        pygame.display.update()