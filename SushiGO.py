from Modul.Game import Game
from Modul.Menu import Menu
from Modul.Instructions import Instructions
from Modul.Gameplay import Gameplay
from Modul.Win import Win
import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption = "Sushi GO!"
icon = pygame.image.load("Modul/Assets/Maki.png")
icon.set_colorkey((255,0,255))
pygame.display.set_icon(icon)
states = {
    "Menu": Menu(),
    "Instructions": Instructions(),
    "Gameplay": Gameplay(),
    "Win": Win()
}

game = Game(screen, states, "Menu")
game.run()

pygame.quit()
sys.exit()

