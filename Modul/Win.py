from unittest.mock import Base
import pygame
from .Basy import BaseState

plrimg = {
    "P1": pygame.image.load("Modul/Assets/P1.png"),
    "P2": pygame.image.load("Modul/Assets/P2.png"),
    "P3": pygame.image.load("Modul/Assets/P3.png"),
    "P4": pygame.image.load("Modul/Assets/P4.png")
}

for name, obj in plrimg.items():
    obj.set_colorkey((255,0,255))

class Win(BaseState):
    def __init__(self):
        super(Win, self).__init__()
        self.next_state = "Menu"
        self.next_stage = "Menu"
        self.next_state = None
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.persist = {}
        self.clicked = pygame.mouse.get_pressed()[0] == 1
        self.background = pygame.image.load("Modul/Assets/Background.png")
        self.quit = False
        self.done = False
        self.gui = pygame.image.load("Modul/Assets/insgui.png")
        self.plrpoints = None
        self.placements = []
        self.plrs = [None, None, None, None]
        self.wintxt = None
        self.pointsoverall = []
        self.x, self.y = 0,0

    def create_text(self, size, position, text, surface):
        font = pygame.font.Font("Modul/Assets/ps2p.ttf", size)
        texti = font.render(text, True, (255,255,255))
        surface.blit(texti, position)

    def reset(self):
        self.clicked = pygame.mouse.get_pressed()[0] == 1
        self.placements = []
        self.pointsoverall = []
        for i, value in enumerate(self.plrpoints):
            self.placements.append((value, "P"+str(i+1)))
            self.pointsoverall.append(value)
        self.placements.sort(reverse=True)
        self.pointsoverall.sort(reverse=True)
        

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            self.done = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
    
    def update(self, dt, screen_size):
        self.x, self.y = screen_size
        self.background = pygame.transform.scale(self.background, (screen_size))
        self.gui = pygame.transform.scale(self.gui, (self.x-100, self.y-100))
        for name, val in plrimg.items():
            x = 150
            plrimg[name] = pygame.transform.scale(val, (x,x))


    def draw(self, surface):
        surface.blit(self.background, (0,0))
        for i in range(4):
            p = self.placements[i][1]
            img = plrimg[p]
            points = self.placements[i][0]
            placement = self.pointsoverall.index(points) + 1
            position = (self.x * .35, 30 + i * 165)
            surface.blit(img, position)
            t = ""
            if placement == 1:
                t = "1st"
            elif placement == 2:
                t = "2nd"
            elif placement == 3:
                t = "3rd"
            elif placement == 4:
                t = "4th"
            self.create_text(50, (self.x * .225, 50 + i * 165), t, surface)
            self.create_text(50, (self.x * .5, 50 + i * 165), (str(points) + " points"), surface)

