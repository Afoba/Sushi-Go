import pygame



class Button():
    def __init__(self, pos, size, image):
        self.pos = pos
        self.size = size
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.clicked = False

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def check_click(self):
        mousepos = pygame.mouse.get_pos()
        action = False
        if self.rect.collidepoint(mousepos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        
            if pygame.mouse.get_pressed()[0] == 0:
                clicked = False

        return action

    def check_hover(self):
        mousepos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mousepos)

    def get_size(self):
        return self.size

        
        