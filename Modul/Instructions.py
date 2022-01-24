import pygame
from .Basy import BaseState

image = {
    "Dumpling": pygame.image.load("Modul/Assets/Dumpling.png"),
    "Maki": pygame.image.load("Modul/Assets/Maki.png"),
    "Nigiri_Egg": pygame.image.load("Modul/Assets/Nigiri_Egg.png"),
    "Nigiri_Salmon": pygame.image.load("Modul/Assets/Nigiri_Salmon.png"),
    "Nigiri_Squid": pygame.image.load("Modul/Assets/Nigiri_Squid.png"),
    "Pudding": pygame.image.load("Modul/Assets/Pudding.png"),
    "Sashimi": pygame.image.load("Modul/Assets/Sashimi.png"),
    "Tempura": pygame.image.load("Modul/Assets/Tempura.png"),
    "Wasabi": pygame.image.load("Modul/Assets/Wasabi.png"),
    "Inventory": pygame.image.load("Modul/Assets/insgui.png")
}

labels = {
    "Dumpling": ["The more dumplings, ","the more points.", "Sequence: 1, 3, 5,", "10, 15"],
    "Maki": ["Each round, player","with more gains 6,", "follow-up gains 3."],
    "Nigiri_Egg": [" = 1 point.", "(Nigiri)"],
    "Nigiri_Salmon": [" = 2 points.", "(Nigiri)"],
    "Nigiri_Squid": [" = 3 points.", "(Nigiri)"],
    "Pudding": ["At the end of the", "game, player with" ,"more gains 6, with", "less loses 6."],
    "Sashimi": ["x3 = 10 points."],
    "Tempura": ["x2 = 5 points."],
    "Wasabi": ["Multiplies next", "Nigiri by 3."]
}

for name, obj in image.items():
    obj.set_colorkey((255,0,255))

class Instructions(BaseState):
    def __init__(self):
        super(Instructions, self).__init__()
        self.next_state = "Gameplay"
        self.next_stage = "Gameplay"
        self.page = 0
        self.quit = False
        self.done = False
        self.background = pygame.image.load("Modul/Assets/Background.png")
        self.gui = image["Inventory"]
        self.clicked = pygame.mouse.get_pressed()[0] == 1

    def create_text(self, size, position, text):
        font = pygame.font.Font("Modul/Assets/ps2p.ttf", size)
        texti = font.render(text, True, (255,255,255))
        return texti, position

    def reset(self):
        self.clicked = pygame.mouse.get_pressed()[0] == 1

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            self.done = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
    
    def update(self, dt, screen_size):
        x, y = screen_size
        self.background = pygame.transform.scale(self.background, (screen_size))
        self.gui = pygame.transform.scale(self.gui, (x-100, y-100))
        coreimgsize = (125,125)
        for name, obj in image.items():
            if name == "Inventory":
                continue
            image[name] = pygame.transform.scale(obj, coreimgsize)

    def draw(self, surface):
        surface.blit(self.background, (0,0))
        surface.blit(self.gui, (50,50))
        i = -1
        for name, obj in image.items():
            if name == "Inventory":
                continue
            i += 1
            if i <= 4:
                surface.blit(obj, (75, 50 + 120 * i))
                adder = 0
                if len(labels[name]) == 2:
                    adder = 30
                for a, stri in enumerate(labels[name]):
                    txt, position = self.create_text(20, (200, 100 + 120 * i + (a-1) * 25 + adder), stri)
                    surface.blit(txt, position)
            else:
                surface.blit(obj, (640, 75 + 120 * (i%5)))
                adder = 0
                if len(labels[name]) == 1:
                    adder = 25
                elif len(labels[name]) == 2:
                    adder = 20
                for a, stri in enumerate(labels[name]):
                    txt, position = self.create_text(20, (775, 125 + 120 * (i%5) + (a-1) * 25 + adder), stri)
                    surface.blit(txt, position)
