import pygame
from game import Game

pygame.init()
win = pygame.display.set_mode((1500, 900))
pygame.display.set_caption('Tanks')

game = Game(win, maxLives = 5, stupidTanks = 2, smartTanks = 1, algorithm = 'expectimax') #minimax
game.start()

pygame.quit()