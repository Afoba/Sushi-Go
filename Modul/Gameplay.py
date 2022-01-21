from ast import Store
from tabnanny import check
import pygame
import random
import math

from Modul.Buttons import Button
from .Basy import BaseState
from .CalcMod import Mod as CalcMod

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
    "P1": pygame.image.load("Modul/Assets/P1.png"),
    "P2": pygame.image.load("Modul/Assets/P2.png"),
    "P3": pygame.image.load("Modul/Assets/P3.png"),
    "P4": pygame.image.load("Modul/Assets/P4.png"),
    "Inventory": pygame.image.load("Modul/Assets/Inventory.png"),
    "PlrTab": pygame.image.load("Modul/Assets/PlayerTab.png")
}

image["PlrTab"].set_alpha(50)

for name, val in image.items():
    val.set_colorkey((255,0,255))

class Gameplay(BaseState):
    
    def __init__(self):
        super(Gameplay, self).__init__()
        #self.game_occuring = True
        self.next_stage = "Win"
        self.tick = 0
        self.basedeck = CalcMod["GenerateDeck"]()
        self.deck = self.basedeck
        self.background = pygame.image.load("Modul/Assets/Background.png")
        self.round = 0
        self.clock = pygame.time.Clock()
        self.hands = [[],[],[],[]]
        self.points = [0,0,0,0]
        self.store = [[],[],[],[]]
        self.foodisplay = []
        self.state = "new"
        self.calculation = True
        self.canclick = True
        self.mainpos = None
        self.offsets = [(-150, -150),(0, -150),(150, -150),(-150, 0),(150, 0),(-150, 150),(0, 150),(150, 150)]
        self.localhand = None
        self.gamebuttons = [None,None,None,None,None,None,None,None]
        self.players = [None, None, None, None]
        self.scorelabels = [None, None, None, None]
        self.invpos = (75, 150)
        self.invsize = (500,500)
        self.inventory = Button(self.invpos,self.invsize, image["Inventory"])
        self.clicked = False
        self.checking = -1
        self.advance = 0
        self.inpos = None
        self.outposend = None
        self.outposstart = None
        self.surface = None

    def reset(self):
        self.game_occuring = True
        self.tick = 0
        self.basedeck = CalcMod["GenerateDeck"]()
        self.deck = self.basedeck
        self.background = pygame.image.load("Modul/Assets/Background.png")
        self.round = 0
        self.hands = [[],[],[],[]]
        self.points = [0,0,0,0]
        self.store = [[],[],[],[]]
        self.foodisplay = []
        self.state = "new"
        self.calculation = True
        self.canclick = True
        self.mainpos = None
        self.offsets = [(-150, -150),(0, -150),(150, -150),(-150, 0),(150, 0),(-150, 150),(0, 150),(150, 150)]
        self.localhand = None
        self.gamebuttons = [None,None,None,None,None,None,None,None]
        self.players = [None, None, None, None]
        self.scorelabels = [None, None, None, None]
        self.invpos = (75, 150)
        self.invsize = (500,500)
        self.inventory = Button(self.invpos,self.invsize, image["Inventory"])
        self.clicked = pygame.mouse.get_pressed()[0] == 1
        self.checking = -1
        self.advance = 0
        self.inpos = None
        self.outposend = None
        self.outposstart = None
        self.x, self.y = 1280, 720

    def maki_calc(self):
        makis = []
        for i in range(4):
            inv = self.store[i]
            makis.append(inv.count("Maki"))
        max1 = 0
        max2 = 0
        for i, value in enumerate(makis):
            if value > max1:
                max2 = max1
                max1 = value
        point4max = 6 // max([makis.count(max1),1])
        point4runner = 3 // max([makis.count(max2), 1])
        for i, value in enumerate(makis):
            inv = self.store[i]
            num = inv.count("Maki")
            if num == max:
                self.points[i] += point4max
            elif num == max2:
                self.points[i] += point4runner

    def pud_calc(self):
        puds = []
        for i in range(4):
            inv = self.store[i]
            puds.append(inv.count("Pudding"))
        maxi = max(puds)
        mini = min(puds)
        maxpoints = 6 // max([1,puds.count(maxi)])
        minpoints = 6 // max([1,puds.count(mini)])
        for i, value in enumerate(puds):
            inv = self.store[i]
            num = inv.count("Pudding")
            if num == maxi:
                self.points[i] += maxpoints
            elif num == mini:
                self.points[i] -= minpoints
            
    def clear_stores(self):
        for i, play in enumerate(self.store):
            newhand = []
            for food in play:
                if food == "Pudding":
                    newhand.append(food)
                else:
                    self.deck.append(food)
            self.store[i] = newhand

    def Transition(self, pickd):
        self.outposend = (self.x * 1.25, self.y/2)
        self.outposstart = (self.x * (-1.25), self.y/2)
        if pickd:
            while self.mainpos[0] < self.outposend[0]:
                self.clock.tick(60)
                self.mainpos = (self.mainpos[0] + 40, self.y/2)
                for i, food in enumerate(self.hands[0]):
                    if food != None:
                        self.gamebuttons[i] = Button((self.mainpos[0] + self.offsets[i][0] - 50, self.mainpos[1] + self.offsets[i][1]), (100,100), image[food])
                    else:
                        self.gamebuttons[i] = None
                self.surface.blit(self.background, (0,0))
                self.surface.blit(image["PlrTab"], (0,0))
                for but in self.gamebuttons:
                    if but != None:
                        but.draw(self.surface)

                for play in self.players:
                    if play != None:
                        play.draw(self.surface)

                for label, posi in self.scorelabels:
                    if label != None and posi != None:
                        self.surface.blit(label, posi)

                if self.checking > -1:
                    self.inventory.draw(self.surface)
                    for obj in self.foodisplay:
                        obj.draw(self.surface)
                pygame.display.update()
        else:
            self.inpos = (self.x/2 + 250, self.y/2)
            self.mainpos = self.outposstart
            while self.mainpos[0] < self.inpos[0]:
                self.clock.tick(60)
                self.mainpos = (self.mainpos[0] + 40, self.y/2)
                if self.mainpos[0] > self.inpos[0]:
                    self.mainpos = self.inpos
                for i, food in enumerate(self.hands[0]):
                    if food != None:
                        self.gamebuttons[i] = Button((self.mainpos[0] + self.offsets[i][0] - 50, self.mainpos[1] + self.offsets[i][1]), (100,100), image[food])
                    else:
                        self.gamebuttons[i] = None
                self.surface.blit(self.background, (0,0))
                self.surface.blit(image["PlrTab"], (0,0))
                for but in self.gamebuttons:
                    if but != None:
                        but.draw(self.surface)

                for play in self.players:
                    if play != None:
                        play.draw(self.surface)

                for label, posi in self.scorelabels:
                    if label != None and posi != None:
                        self.surface.blit(label, posi)

                if self.checking > -1:
                    self.inventory.draw(self.surface)
                    for obj in self.foodisplay:
                        obj.draw(self.surface)
                pygame.display.update()


    def create_hands(self):
        random.shuffle(self.deck)
        for i in range(4):
            toHand = self.deck[0:8]
            newDeck = self.deck[8::]
            self.hands[i] = toHand
            self.deck = newDeck

    def rotate_hands(self):
        newhand = [self.hands[3],self.hands[0],self.hands[1],self.hands[2]]
        self.hands = newhand
        self.Transition(False)

    def pick(self, plr, index):
        value = self.hands[plr][index]
        self.hands[plr][index] = None
        self.store[plr].append(value)

    def aipick(self, plr):
        Wasabi = False
        Tempura = 0
        Sashimi = 0
        Dumpling = 0
        Chosen = False
        for food in self.store[plr]:
            if food == "Wasabi":
                Wasabi = True
            elif "Nigiri" in food:
                Wasabi = False
            elif food == "Tempura":
                Tempura += 1
            elif food == "Sashimi":
                Sashimi += 1
            elif food == "Dumpling":
                Dumpling += 1
        newar = []
        for i, f in enumerate(self.hands[plr]):
            if f != None:
                newar.append(i)
                if (("Nigiri" in f) and Wasabi) or (Tempura % 2 > 0 and f == "Tempura") or (Sashimi % 3 > 0 and f == "Sashimi"):
                    self.pick(plr, i)
                    Chosen = True
                    break

        if Dumpling > 0 and "Dumpling" in self.hands[plr] and not Chosen:
            i = self.hands[plr].index("Dumpling")
            self.pick(plr, i)
            Chosen = True

        if "Wasabi" in self.hands[plr] and len(newar) < 3 and not Wasabi and not Chosen:
            i = self.hands[plr].index("Wasabi")
            self.pick(plr, i)
            Chosen = True

        if Dumpling < 3 and "Nigiri_Squid" in self.hands[plr] and not Chosen:
            i = self.hands[plr].index("Nigiri_Squid")
            self.pick(plr, i)
            Chosen = True

        if "Nigiri_Salmon" in self.hands[plr] and not Chosen:
            i = self.hands[plr].index("Nigiri_Salmon")
            self.pick(plr, i)
            Chosen = True

        if "Tempura" in self.hands[plr] and not Chosen:
            i = self.hands[plr].index("Tempura")
            self.pick(plr, i)
            Chosen = True

        if "Sashimi" in self.hands[plr] and not Chosen:
            i = self.hands[plr].index("Sashimi")
            self.pick(plr, i)
            Chosen = True

        if not Chosen:
            tochoose = random.randrange(0, len(newar))
            self.pick(plr, newar[tochoose])


    def create_text(self, size, position, text, index):
        font = pygame.font.Font("D:\ProjetoFP\Modul\Assets\ps2p.ttf", size)
        texti = font.render(text, True, (255,255,255))
        self.scorelabels[index] = (texti, position)
        
    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        for i, but in enumerate(self.gamebuttons):
            if but != None and self.canclick:
                if but.check_click() and not self.clicked:
                    self.clicked = True
                    self.pick(0, i)
                    for a in range(3):
                        self.aipick(a+1)
                    self.Transition(True)

                    self.rotate_hands()

                elif pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False
        self.checking = -1
        for i, plr in enumerate(self.players):
            if plr != None:
                if plr.check_hover():
                    self.checking = i

    def update(self, dt, screen_size):
        if self.state == "new" and self.round < 3:
            self.state = "play"
            self.round += 1
            self.create_hands()
            if self.round > 1:
                self.Transition(False)
        elif self.state == "new" and self.calculation:
            self.state = "end"
            self.calculation = False
            self.pud_calc()
            self.done = True
        if self.hands[0] == [None,None,None,None,None,None,None,None] and self.state != "new":
            self.state = "new"
            for i in range(0,4):
                points = CalcMod["PointCalculation"](self.store[i])
                self.points[i] += points
            self.maki_calc()
            self.clear_stores()
        x, y = screen_size
        self.tick += dt
        self.inpos = (x/2 + 250, y/2)
        self.outposend = (x * 1.5, y/2)
        self.outposstart = (x * (-.5), y/2)
        self.mainpos = self.inpos
        image["PlrTab"] = pygame.transform.scale(image["PlrTab"], (x, 100))

        if self.checking != -1:
            self.foodisplay = []
            inde = -1
            for food in self.store[self.checking]:
                if food != None:
                    inde += 1
                    posi = (self.invpos[0] + 40 + 125 * (inde // 8), self.invpos[1] + 15 + (inde % 8) * (50))
                    size = (100,100)
                    toAppend = Button(posi, size, image[food])
                    self.foodisplay.append(toAppend)
        
        for i, food in enumerate(self.hands[0]):
            if food != None:
                self.gamebuttons[i] = Button((self.mainpos[0] + self.offsets[i][0] - 50, self.mainpos[1] + self.offsets[i][1]), (100,100), image[food])
            else:
                self.gamebuttons[i] = None

        for i, obj in enumerate(self.players):
            self.players[i] = Button((x/32 + i * x/4, 15), (75,75), image["P" + str(i + 1)])
            self.create_text(50, (x/10 + i * x/4, 25), str(self.points[i]), i)

    def draw(self, surface):
        self.surface = surface
        if self.game_occuring:
            surface.blit(self.background, (0,0))
            surface.blit(image["PlrTab"], (0,0))
            for but in self.gamebuttons:
                if but != None:
                    but.draw(surface)

            for play in self.players:
                if play != None:
                    play.draw(surface)

            for label, posi in self.scorelabels:
                if label != None and posi != None:
                    surface.blit(label, posi)

            if self.checking > -1:
                self.inventory.draw(surface)
                for obj in self.foodisplay:
                    obj.draw(surface)
        





     



    