import pygame
import math
from .Basy import BaseState
from .Buttons import Button

button_img = pygame.image.load("Modul/Assets/lucky_cookie.png")
button_img.set_colorkey((255,0,255))

class Menu(BaseState):
    def __init__(self):
        super(Menu, self).__init__()
        self.active_index = 0
        self.next_stage = "Instructions"
        self.title = None
        self.play = None
        self.playtext = None
        self.instructions = None
        self.clicked = pygame.mouse.get_pressed()[0] == 1
        self.background = pygame.image.load("Modul/Assets/Background.png")
        
    def reset(self):
        self.clicked = pygame.mouse.get_pressed()[0] == 1

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        if self.play != None:
            if self.play.check_hover and not self.clicked and pygame.mouse.get_pressed()[0] == 1:
                self.next_state = "Gameplay"
                self.done = True
            elif pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
    
    def update(self, dt, screen_size):
        x, y = screen_size
        titlefonti = pygame.font.Font("Modul/Assets/ps2p.ttf", math.floor(.08 * y))
        title = titlefonti.render("Sushi GO!", True, (0,0,0))
        titlepos = title.get_rect(center = (math.floor(x * .5), math.floor(y * .25)))
        self.title = [title, titlepos]

        playsize = (560,175)
        playpos = ((x/2 - playsize[0]/2), math.floor(y * .4))
        self.play = Button(playpos, playsize, button_img)
        playtext = titlefonti.render("Play", True, (0,0,0))
        playtextpos = title.get_rect(center = (math.floor(x / 2) + 150, 5 + math.floor(playpos[1] + playsize[1] / 2)))
        self.playtext = [playtext, playtextpos]
        

    def draw(self, surface):
        surface.fill((153, 204, 255))
        surface.blit(self.background, (0,0))
        surface.blit(self.title[0], self.title[1])
        self.play.draw(surface)
        surface.blit(self.playtext[0], self.playtext[1])

        
